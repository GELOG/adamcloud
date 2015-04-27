__author__ = 'flangelier'

import sys
import re
import paramiko
import getpass

adamcloud_base_path = 'https://raw.githubusercontent.com/GELOG/adamcloud/master/'
hadoop_host_volume_path = '/hdfs-data'
hadoop_image = 'gelog/hadoop'
hadoop_image_tag = '2.3.0'
spark_image = 'gelog/spark'
spark_image_tag = '1.2-bin-hadoop2.3'
sudo_passwords = {}


def is_valid_hostname(hosts):
    failed = []
    for host in hosts:
        # Validating only IPv4 because we need to add the IP in the containers hosts file
        if not re.compile('^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$').match(host):
            failed.append(host)
            continue
        # if len(host) > 255:
        #     return False
        # if host[-1] == ".":
        #     host = host[:-1]  # strip exactly one dot from the right, if present
        # allowed = re.compile("(?!-)[A-Z\d-]{1,63}(?<!-)$", re.IGNORECASE)
        # return all(allowed.match(x) for x in hostname.split("."))

    if len(failed) > 0:
        print "There aren't valid IPv4", failed
        return False
    return True


def execute_over_ssh(host, command):
    print 'host: %s cmd: %s' % (host, command)
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host)
        chan = ssh.get_transport().open_session()
        if 'sudo' in command:
            chan.get_pty()
            chan.exec_command(command)
            received = chan.recv(1024)
            # If the password entered is bad, it will loop until the end of time...
            while '[sudo] password for adamcloud:' in received:
                password = sudo_passwords.get(host, None)
                if password is None:
                    print received
                    password = getpass.getpass()
                    sudo_passwords[host] = password
                stdin = chan.makefile('wb', -1)
                stdin.write(password + '\n')
                received = chan.recv(1024)
        else:
            chan.exec_command(command)
            received = chan.recv(1024)

        print(received)

        ssh.close()
    except paramiko.AuthenticationException as e:
        help('Connection to %s failed, make sure you pushed your public key on that host!' % host)
        return False
    return True


def hdfs_configure(env, hosts):
    print 'Configuring hdfs for', hosts
    failed = []
    for host in hosts:
        command = 'sudo mkdir -p ' + hadoop_host_volume_path + '/conf'
        if not execute_over_ssh(host, command):
            failed.append(host)
            continue

        base_command = 'sudo wget https://raw.githubusercontent.com/GELOG/adamcloud/{0}/env/{1}/{2} -O ' \
                       + hadoop_host_volume_path + '/conf/{2}; '
        hadoop_tag = hadoop_image_tag

        if not execute_over_ssh(host, base_command.format(hadoop_tag, env, 'core-site.xml')):
            failed.append(host)
            continue
        if not execute_over_ssh(host, base_command.format(hadoop_tag, env, 'yarn-site.xml')):
            failed.append(host)
            continue
        if not execute_over_ssh(host, base_command.format(hadoop_tag, env, 'mapred-site.xml')):
            failed.append(host)
            continue
        if not execute_over_ssh(host, base_command.format(hadoop_tag, env, 'hdfs-site.xml')):
            failed.append(host)
            continue
    if len(failed) > 0:
        print 'Failed to configure hosts:', failed
        return False
    return True


def hdfs_format(env, host, alsoConfigure=True):
    print 'Formating HDFS on host', host

    if alsoConfigure and not hdfs_configure(env, [host]):
        return False

    command = 'docker run --rm -ti --name hdfs-setup -h hdfs-setup -v {}:/data {} {}'.format(hadoop_host_volume_path,
                                                                           hadoop_image + ':' + hadoop_image_tag,
                                                                           'hdfs namenode -format')
    if not execute_over_ssh(host, command):
        return False
    return True


def hdfs_run(env, namenode_host, secondarynamenode_host, datanodes_host):
    print 'hdfs run'
    print 'nn', namenode_host
    #-v /hdfs-data/log:/usr/local/hadoop/logs/

    command = 'docker run -d --name hdfs-namenode -h hdfs-namenode -p 9000:9000 -p 50070:50070 -v /adamcloud:/adamcloud -v {}:/data {} {}'.format(
        hadoop_host_volume_path,
        hadoop_image + ':' + hadoop_image_tag,
        'hdfs namenode'
    )
    #hdfs namenode
    if not execute_over_ssh(namenode_host, command):
        print 'Failed to setup namenode on', namenode_host
        return False

    print 'snn', secondarynamenode_host

    command = 'docker run -d --name hdfs-secondarynamenode -h hdfs-secondarynamenode -p 50090:50090 --link=hdfs-namenode:hdfs-namenode -v /adamcloud:/adamcloud -v {}:/data {} {}'.format(
        hadoop_host_volume_path,
        hadoop_image + ':' + hadoop_image_tag,
        'hdfs secondarynamenode'
    )
    #hdfs secondarynamenode
    if not execute_over_ssh(secondarynamenode_host, command):
        print 'Failed to setup secondary namenode on', secondarynamenode_host
        return False

    index = 1
    failed = []
    for datanode_host in datanodes_host:
        print 'dn', datanode_host

        command = 'docker run -d --name hdfs-datanode{0} -h hdfs-datanode{0} -p 5008{0}:5008{0} --link=hdfs-namenode:hdfs-namenode --link=hdfs-secondarynamenode:hdfs-secondarynamenode -v /adamcloud:/adamcloud -v {1}:/data {2} {3}'.format(
            index,
            hadoop_host_volume_path,
            hadoop_image + ':' + hadoop_image_tag,
            'hdfs datanode'
        )
        #hdfs datanode
        if not execute_over_ssh(datanode_host, command):
            failed.append(datanode_host)
            continue

    if len(failed) > 0:
        print 'Failed to setup datanodes:', failed
        return False
    return True


def spark_run(env, master_host, workers_host):
    print 'spark setup'
    if len(workers_host) > 9:
        help('You can only have up to 9 workers.')
        return False
    print 'master', master_host
    command = 'docker run -d --name spark-master -h spark-master -p 8080:8080 -p 7077:7077 {0} {1}'.format(
        spark_image + ':' + spark_image_tag,
        'spark-class org.apache.spark.deploy.master.Master'
    )
    if not execute_over_ssh(master_host, command):
        print 'Failed to setup spark master on', master_host
        return False

    print 'workers', workers_host
    index = 0
    failed = []
    for worker_host in workers_host:
        index += 1
        command = 'docker run -d --name spark-worker{0} -h spark-worker{0} -p 808{0}:808{0} --link=hdfs-namenode:hdfs-namenode --link=spark-master:spark-master --link=adam:adam --link=avocado:avocado {1} {2}'.format(
            index,
            spark_image + ':' + spark_image_tag,
            'spark-class org.apache.spark.deploy.worker.Worker spark://spark-master:7077'
        )
        if not execute_over_ssh(worker_host, command):
            failed.append(worker_host)
            continue

    if len(failed) > 0:
        print 'Failed to setup workers:', failed
        return False
    return True


def help(error=''):
    print
    print error
    print
    print 'usage: env service [service-params]'
    print
    print 'env              the environment you want to setup:'
    print '                     local'
    print '                     macmini'
    print '                     aws'
    print 'service          the service to execute:'
    # print '                     hdfsconfigure [host1 [host2 [...]]]'
    print '                     hdfsformat nn-host'
    print '                     hdfsrun nn-host snn-host dn1-host [dn2-host [dn3-host [...]]]'
    print '                     spark master-host worker1-host [worker2-host [worker3-host [...]]]'


def validate_env(env):
    if env == 'local':
        print 'local'
    elif env == 'macmini':
        print 'macmini'
    elif env == 'aws':
        print 'aws'
    else:
        help('Environment "' + env + '" is not valid.')
        return False
    return True


def init():
    try:
        args_iterator = iter(sys.argv)
        next(args_iterator)  # Skip the path
        env = next(args_iterator)
        service = next(args_iterator)

        if not validate_env(env):
            return
        ips = list(args_iterator)
        if not is_valid_hostname(ips):
            print 'Mauvais ip'

        if service == 'hdfsconfigure':
            if not hdfs_configure(env, ips):
                print
                print 'Error: Configuring HDFS failed.'
        elif service == 'hdfsformat':
            print 'hdfssetup [host]'
            if not hdfs_format(env, ips[0]):
                print
                print 'Error: Formating HDFS failed.'
        elif service == 'hdfsrun':
            print 'hdfsrun nn-host snn-host dn1-host [dn2-host [dn3-host [...]]]'
            if not hdfs_run(env, ips[0], ips[1], ips[2:]):
                print
                print 'Error: Running HDFS failed.'
        elif service == 'spark':
            print 'spark spark-master-host worker1-host [worker2-host [worker3-host [...]]]'
            if not spark_run(env, ips[0], ips[1:]):
                print
                print 'Error: Running Spark failed.'
        else:
            help('Service "' + service + '" is not valid.')
            return
    except (IndexError, StopIteration):
        help('Some arguments are missing.')
        return


init()

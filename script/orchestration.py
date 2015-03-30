__author__ = 'flangelier'

import sys
import re
import paramiko
import getpass

adamcloud_base_path = 'https://raw.githubusercontent.com/GELOG/adamcloud/master/'
hadoop_image = 'gelog/hadoop'
hadoop_image_tag = 'latest'#2.6.0'
spark_image = ''
sudo_passwords = {}


def is_valid_hostname(hostname):
    if len(hostname) > 255:
        return False
    if hostname[-1] == ".":
        hostname = hostname[:-1]  # strip exactly one dot from the right, if present
    allowed = re.compile("(?!-)[A-Z\d-]{1,63}(?<!-)$", re.IGNORECASE)
    return all(allowed.match(x) for x in hostname.split("."))


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
        print_help('Connection to %s failed, make sure you pushed your public key on that host!' % host)
        return False
    return True


def hdfs_setup(env, host):
    print 'hdfs setup', host
    host_data_folder = '/hdfs-data'

    command = 'sudo mkdir -p ' + host_data_folder + '/conf'
    if not execute_over_ssh(host, command):
        return False

    base_command = 'sudo wget https://raw.githubusercontent.com/GELOG/docker-ubuntu-hadoop/{0}/env/{1}/{2} -O ' \
                   + host_data_folder + '/conf/{2}; '
    hadoop_tag = hadoop_image_tag
    hadoop_tag = 'master'

    if not execute_over_ssh(host, base_command.format(hadoop_tag, env, 'core-site.xml')):
        return False
    if not execute_over_ssh(host, base_command.format(hadoop_tag, env, 'yarn-site.xml')):
        return False
    if not execute_over_ssh(host, base_command.format(hadoop_tag, env, 'mapred-site.xml')):
        return False
    if not execute_over_ssh(host, base_command.format(hadoop_tag, env, 'hdfs-site.xml')):
        return False

    command = 'docker run --rm --name hdfs-setup -v {}:/data {} {}'.format(host_data_folder,
                                                                           hadoop_image + ':' + hadoop_image_tag,
                                                                           'hdfs namenode -format')
    print command
    if not execute_over_ssh(host, command):
        return False
    return True


def hdfs_run(namenode_host, secondarynamenode_host, datanodes_host):
    print 'hdfs setup'
    print 'nn', namenode_host
    # namenode-hdfs /usr/local/hadoop/sbin/hadoop-daemon.sh start namenode
    print 'snn', secondarynamenode_host
    #secnamenode-hdfs /usr/local/hadoop/sbin/hadoop-daemon.sh start secondarynamenode
    print 'dn', datanodes_host


def spark_run(master_host, workers_host):
    print 'hdfs setup'
    print 'master', master_host
    print 'workers', workers_host


def print_help(error=''):
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
    print '                     hdfssetup [host]'
    print '                     hdfsrun nn-host snn-host dn1-host [dn2-host [dn3-host [...]]]'
    print '                     spark spark-master-host worker1-host [worker2-host [worker3-host [...]]]'


def validate_env(env):
    if env == 'local':
        print 'local'
    elif env == 'macmini':
        print 'macmini'
    elif env == 'aws':
        print 'aws'
    else:
        print_help('Environment "' + env + '" is not valid.')
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

        if service == 'hdfssetup':
            print 'hdfssetup [host]'
            hdfs_setup(env, next(args_iterator))
        elif service == 'hdfsrun':
            print 'hdfsrun nn-host snn-host dn1-host [dn2-host [dn3-host [...]]]'
            hdfs_run(next(args_iterator), next(args_iterator), list(args_iterator))
        elif service == 'spark':
            print 'spark spark-master-host worker1-host [worker2-host [worker3-host [...]]]'
            spark_run(next(args_iterator), list(args_iterator))
        else:
            print_help('Service "' + service + '" is not valid.')
            return
    except StopIteration as e:
        print_help('Some arguments are missing.')
        return


init()

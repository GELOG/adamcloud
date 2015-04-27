__author__ = 'flangelier'

import sys
import re
import paramiko
import getpass

snap_image = 'gelog/snap'
snap_image_tag = 'latest'

adam_image = 'gelog/adam'
adam_image_tag = 'latest'

avocado_image = 'gelog/avocado'
avocado_image_tag = 'latest'

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


def snap_index(fasta, snap):
    host = '127.0.0.1'
    print 'Running snap index on host', host

    sub_command = 'snap index /adamcloud/{0} /adamcloud/{1}'.format(fasta, snap)
    command = 'docker run --rm -ti --name snap -h snap -v /adamcloud:/adamcloud {} {}'.format(
                                                                           snap_image + ':' + snap_image_tag,
                                                                           sub_command)
    if not execute_over_ssh(host, command):
        return False
    return True


def snap_align(fastq, snap, sam):
    host = '127.0.0.1'
    print 'Running snap align on host', host

    sub_command = 'snap single /adamcloud/{0} /adamcloud/{0} -o /adamcloud/{0}'.format(snap, fastq, sam)
    command = 'docker run --rm -ti --name snap -h snap -v /adamcloud:/adamcloud {} {}'.format(
                                                                           snap_image + ':' + snap_image_tag,
                                                                           sub_command)
    if not execute_over_ssh(host, command):
        return False
    return True


def adam(spark_master, hdfs_namenode, sam, adam):
    host = '127.0.0.1'
    print 'Running Adam on host', host

    sub_command = 'adam-submit --master spark://spark-master:7077 transform hdfs://hdfs-namenode:9000/{0} hdfs://hdfs-namenode:9000/{1}'.format(sam, adam)
    command = 'docker run --rm -ti --name adam -h adam -p 4040:4040 -v /adamcloud:/adamcloud --link=spark-master:spark-master --link=hdfs-namenode:hdfs-namenode {} {}'.format(
                                                                           adam_image + ':' + adam_image_tag,
                                                                           sub_command)
    if not execute_over_ssh(host, command):
        return False
    return True


def avocado(spark_master, hdfs_namenode, fasta, adam, avocado):
    host = '127.0.0.1'
    print 'Running Avocado on host', host

    sub_command = 'avocado-submit --master spark://spark-master:7077 hdfs://hdfs-namenode:9000/{0} /adamcloud/{1} /adamcloud/{2} /usr/local/avocado/avocado-sample-configs/basic.properties'.format(adam, fasta, avocado)
    command = 'docker run --rm -ti --name avocado -h avocado -v /adamcloud:/adamcloud --link=spark-master:spark-master --link=hdfs-namenode:hdfs-namenode {} {}'.format(
                                                                           avocado_image + ':' + avocado_image_tag,
                                                                           sub_command)
    if not execute_over_ssh(host, command):
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
#    print '                     link_to_swarm swarm_host swarm_salve1 [swarm_salve2 [swarm_salve3 [...]]]'
    print '                     snapIndex fasta snap'
    print '                     snapAlign fastq snap sam'
    print '                     adam spark-master hdfs-namenode sam adam'
    print '                     avocado spark-master hdfs-namenode fasta adam avocado'


def init():

    try:
        args_iterator = iter(sys.argv)
        next(args_iterator)  # Skip the path
        service = next(args_iterator)

        if service == 'snapIndex':
            if not snap_index(next(args_iterator), next(args_iterator)):
                print
                print 'Error: Indexing failed.'
        elif service == 'snapAlign':
            if not snap_align(next(args_iterator), next(args_iterator), next(args_iterator)):
                print
                print 'Error: Alignment failed.'
        elif service == 'adam':
            ips = list(args_iterator[:2])
            if not is_valid_hostname(ips):
                print 'Mauvais ip'
            if not adam(ips[0], ips[1], next(args_iterator), next(args_iterator)):
                print
                print 'Error: Adam failed.'
        elif service == 'avocado':
            ips = list(args_iterator[:2])
            if not avocado(ips[0], ips[1], next(args_iterator), next(args_iterator), next(args_iterator)):
                print
                print 'Error: Avocado failed.'
        else:
            help('Service "' + service + '" is not valid.')
            return
    except (IndexError, StopIteration):
        help('Some arguments are missing.')
        return

init()
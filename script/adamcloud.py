__author__ = 'flangelier'

import sys
import re
from subprocess import call
#from docker import Client

#master = Client
#slaves = []
#docker_run_base_arg = 'docker run --rm -ti -v /data:/data'.split(' ')
docker_run_base_arg = 'docker run -ti -v /data:/data'.split(' ')


def is_valid_hostname(hostname):
    if len(hostname) > 255:
        return False
    if hostname[-1] == ".":
        hostname = hostname[:-1]  # strip exactly one dot from the right, if present
    allowed = re.compile("(?!-)[A-Z\d-]{1,63}(?<!-)$", re.IGNORECASE)
    return all(allowed.match(x) for x in hostname.split("."))


def setup_master(host, is_master_node_alone):
    print 'Setup master', host
    docker_pull_base_arg = 'docker pull'.split(' ')
    #master = Client(base_url='tcp://' + host + ':2375')

    print 'Pulling gelog/snap:1.0beta.15'
    call(docker_pull_base_arg + ['gelog/snap:1.0beta.15'])
    #master.pull(repository='gelog/snap', tag='1.0beta.15')

    print 'Pulling gelog/adam:0.14.0'
    call(docker_pull_base_arg + ['gelog/adam:0.14.0'])
    #master.pull(repository='gelog/adam', tag='0.14.0')

    print 'Pulling gelog/avocado:0.0.0-master-branch'
    call(docker_pull_base_arg + ['gelog/avocado:0.0.0-master-branch'])
    #master.pull(repository='gelog/avocado', tag='0.0.0-master-branch')

    print 'Pulling gelog/spark:1.1.0-bin-hadoop2.3'
    call(docker_pull_base_arg + ['gelog/spark:1.1.0-bin-hadoop2.3'])
    #master.pull(repository='gelog/spark', tag='1.1.0-bin-hadoop2.3')

    if not is_master_node_alone:
        print 'Pulling gelog/snap:1.0beta.15'
        #call(docker_pull_base_arg + ['gelog/snap:1.0beta.15'])
        #master.pull(repository='gelog/spark', tag='')


#docker run --volume=/:/rootfs:ro --volume=/var/run:/var/run:rw --volume=/sys:/sys:ro --volume=/var/lib/docker/:/var/lib/docker:ro --publish=8079:8080 --detach=true --name=cadvisor google/cadvisor:latest

#Running the clients (SNAP, ADAM and AVOCADO)

#Running the Spark Master with web interface on port 8080
#sudo weave run 192.168.0.9/24 -ti --name master-spark -h master-spark -p 8080:8080 gelog/spark:1.1.0-bin-hadoop2.3 /usr/local/spark/bin/spark-class org.apache.spark.deploy.master.Master --ip 192.168.0.9

#Running the HDFS NameNode with web interface on port 50070
#sudo weave run 192.168.0.19/24 -ti --name namenode-hdfs -h namenode-hdfs -p 50070:50070 -v /docker-volume:/docker-volume gelog/hadoop:2.3.0
#docker exec namenode-hdfs hdfs namenode -format
#docker exec namenode-hdfs mkdir /usr/local/hadoop-2.3.0/logs
#docker exec namenode-hdfs /usr/local/hadoop/sbin/hadoop-daemon.sh start namenode

#Running the HDFS SecondaryNameNode with web interface on port 50090
#sudo weave run 192.168.0.20/24 -ti --name secnamenode-hdfs -h secnamenode-hdfs -p 50090:50090 gelog/hadoop:2.3.0
#docker exec secnamenode-hdfs mkdir /usr/local/hadoop-2.3.0/logs
#docker exec secnamenode-hdfs /usr/local/hadoop/sbin/hadoop-daemon.sh start secondarynamenode
    return True


def run_snap(index_path, index_folder, genome_path, sam_path):
    print "Running snap index on", genome_path, 'indexed by', index_path

    host = 'localhost'
    #master = Client(base_url='tcp://' + host + ':2375')

    # sudo weave run 192.168.0.1/24 -ti --name client-snap -h client-snap -v /docker-volume:/docker-volume gelog/snap
    #container = master.create_container(tty=True,
    #                        stdin_open=True,
    #                        hostname='client-snap',
    #                        volumes='/data:/data',
    #                        image='gelog/snap:1.0beta.15',
    #                        command=['index', index_path, index_folder])
    # docker run --rm=true -ti -v /data:/data gelog/snap index /data/chr1.fa /data/snap-index.chr1
    #response = master.start(container=container.get('Id'))
    #print(response)

    snap_index = docker_run_base_arg[:] + ['-h', 'snap_index', '--name', 'snap_index', 'gelog/snap:1.0beta.15'] + ['index', index_path, index_folder]
    snap_single = docker_run_base_arg[:] + ['-h', 'snap_single', '--name', 'snap_single', 'gelog/snap:1.0beta.15'] + ['single', index_folder, genome_path, '-o', sam_path]

    #mkdir -p /data/
    #wget -O /data/chr1.fa.gz http://hgdownload.cse.ucsc.edu/goldenPath/hg19/chromosomes/chr1.fa.gz
    #gzip -d /data/chr1.fa.gz

    call(snap_index)

    #wget -O /data/SRR062634.filt.fastq.gz ftp://ftp.1000genomes.ebi.ac.uk/vol1/ftp/data/HG00096/sequence_read/SRR062634.filt.fastq.gz
    #gzip -d /data/Sdocker run --rm=true -ti -v /data:/data gelog/snap single /data/snap-index.chr1/ /data/SRR062634.filt.fastq -o /data/SRR062634.samRR062634.filt.fastq.gz

    call(snap_single)


def run_adam(sam_path, adam_path):
    print "Running adam with sam @", sam_path, 'and outputing the adam @', adam_path
    adam_transform = docker_run_base_arg[:] + ['-h', 'adam', '--name', 'adam'] + \
        ['-name adam', 'gelog/adam:0.14.0', 'adam-submit', 'transform', sam_path, adam_path]
    call(adam_transform)


def run_avocado(adam_path, index_path, avr_path):
    print "Running avocado with adam @", adam_path, ', index @', index_path, 'and outputing the avr @', avr_path
    basic_properties = '/usr/local/avocado/avocado-sample-configs/basic.properties'
    avocado_submit = docker_run_base_arg[:] + ['-h', 'avocado', '--name', 'avocado', '-v', '/avocado:/usr/local/avocado/bin'] + \
        ['gelog/avocado:0.0.0-master-branch', 'avocado-submit', '-Dspark.executor.memory=10g',
         adam_path, index_path, avr_path, basic_properties]
    call(avocado_submit)
    #, '-v', '/avocado:/usr/local/avocado/bin'

#docker run -ti --rm --name client-genomics -v /data:/data avo /bin/bash
#avocado-submit /data/SRR062634.adam /data/chr1.fa /data/SRR062634.avr\
 #       /usr/local/avocado/avocado-sample-configs/basic.properties

def setup_spark():
    print 'spark'
    #Running the Spark Master and Worker with web interfaces on ports 8080 and 8081
    #docker run -d -ti --name spark -h spark -p 8080:8080 -p 8081:8081 --link client-genomics:client-genomics
    #  -v /docker-volume:/docker-volume spark_1.1.0-prebuilthadoop2.3
    #docker exec -d spark /usr/local/spark/bin/spark-class org.apache.spark.deploy.master.Master
    #docker exec -d spark /usr/local/spark/bin/spark-class org.apache.spark.deploy.worker.Worker spark://spark:7077

    #Add hosts entry for Spark IP Address in the client
    #SPARK_IP=`eval "docker inspect --format '{{ .NetworkSettings.IPAddress }}' spark"`
    #docker exec client-genomics sudo -- sh -c "echo $SPARK_IP spark >> /etc/hosts"
 #   master.create_container(tty=True,
 #                           stdin_open=True,
 #                           hostname='spark',
 #                           volumes='/data:/data',
 #                           image='gelog/spark',
 #                           tag='1.1.0-bin-hadoop2.3',
 #                           ports=[8080, 8081])


def setup_slave(host, slave_id):
    return
    print 'Setup slave ', slave_id, ' ', host
    slave = Client(base_url='tcp://' + host + ':2375')
    slaves.append((slave_id, slave))


def print_help(error=''):
    print error
    print 'usage: command master [slave1 [slave2 [...]]]'
    print
    print 'command          the command to execute: snap, adam, avocado'
    print 'master           the hostname or IP of the master'
    print 'slave[1-...]     the hostname or IP of the slave'


def init():
    if len(sys.argv) <= 1:
        print_help()
        return

    index_path = '/data/chr1.fa'
    genome_path = '/data/SRR062634.filt.fastq'

    directory = '/'.join(index_path.split('/')[:-1])
    index_name = index_path.split('/')[-1].split('.')[0]
    genome_name = genome_path.split('/')[-1].split('.')[0]

    index_folder = directory + '/snap-index.' + index_name
    sam_path = directory + '/' + genome_name + '.sam'
    adam_path = directory + '/' + genome_name + '.adam'
    avr_path = directory + '/' + genome_name + '.avr'

    args_iterator = iter(sys.argv)
    next(args_iterator) # Skip the path
    cmd_to_do = next(args_iterator)

    # IPs
    is_master_setup = False
    slave_count = 0
    is_node_alone = len(sys.argv) == 3

    while True:
        try:
            arg = args_iterator.next()
            if is_valid_hostname(arg):
                if not is_master_setup:
                    is_master_setup = True  # setup_master(arg, is_node_alone)
                else:
                    slave_count += 1
                    setup_slave(arg, slave_count)
            else:
                print_help(arg + ' is not a valid hostname or IP.')
                return

        except StopIteration as e:
            break

    if is_node_alone:
        print 'Only 1 node'
        if cmd_to_do == 'pull':
            setup_master('localhost', True)
        elif cmd_to_do == 'snap':
            run_snap(index_path, index_folder, genome_path, sam_path)
        elif cmd_to_do == 'adam':
            run_adam(sam_path, adam_path)
        elif cmd_to_do == 'avocado':
            run_avocado(adam_path, index_path, avr_path)
        else:
            print_help(cmd_to_do + ' is not a valid command.')

# print 'Number of arguments:', len(sys.argv), 'arguments.'
# print 'Argument List:', str(sys.argv)

init()
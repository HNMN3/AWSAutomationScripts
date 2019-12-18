import boto3
import paramiko
import time


def print_docker_container_status(instance_id, conn):
    stdin, stdout, stderr = conn.exec_command("sudo docker ps | grep ubuntu")

    output_lines = stdout.readlines()
    for line in output_lines:
        container_id = line.split()[0]
        stdin, stdout, stderr = conn.exec_command("sudo docker exec {} top -bn1 | grep Cpu".format(container_id))
        cpu_status = stdout.readlines()[0]
        print('{}\t{}\t{}'.format(instance_id, container_id, cpu_status))


def monitor_ec2_docker_instances():
    instance_ids = ['i-09a9d8546718467a8', 'i-0e498a183f5cf762c', 'i-026a684f7e6ccc9c3']
    # print(instance_ids)
    print("Instance ID\t\tContainer ID\tCPU Status")
    key = paramiko.RSAKey.from_private_key_file("sand_security.pem")
    port = 22
    s = paramiko.SSHClient()
    s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ec2_client = boto3.resource('ec2')
    instance_list = ec2_client.instances.filter(InstanceIds=instance_ids).all()
    update_instance_details = False
    while True:
        for instance in instance_list:
            try:
                hostname = instance.network_interfaces_attribute[0]['Association']['PublicDnsName']
            except:
                print("Instance ID: {} | Instance Not started properly!!".format(instance.id))
                update_instance_details = True
                continue
            s.connect(hostname, port, username='ubuntu', pkey=key, allow_agent=False, look_for_keys=False)
            print_docker_container_status(instance.id, s)
            s.close()
        if update_instance_details:
            update_instance_details = False
            instance_list = ec2_client.instances.filter(InstanceIds=instance_ids).all()
        print("-" * 10)
        time.sleep(5)


if __name__ == '__main__':
    monitor_ec2_docker_instances()

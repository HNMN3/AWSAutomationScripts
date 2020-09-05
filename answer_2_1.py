import boto3
import paramiko
import time


# from answer_1_2 import start_instances


def monitor_ec2_instances(instance_ids):
    print("Instance ID\t\tCPU Status")
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
                print("{}\tInstance Not started properly!!".format(instance.id))
                update_instance_details = True
                continue
            s.connect(hostname, port, username='ubuntu', pkey=key, allow_agent=False, look_for_keys=False)
            command = 'top -bn1 | grep Cpu'
            (stdin, stdout, stderr) = s.exec_command(command)
            # print(stdin, stdout, stderr)
            line = stdout.readlines()[0]
            print("{}\t{}".format(instance.id, line))
            s.close()
        if update_instance_details:
            update_instance_details = False
            instance_list = ec2_client.instances.filter(InstanceIds=instance_ids).all()
        print("-" * 10)
        time.sleep(5)


if __name__ == '__main__':
    # Instance ids will be provided in below variable to monitor them
    instance_ids_to_monitor = ['i-09a9d8546718467a8', 'i-0e498a183f5cf762c', 'i-026a684f7e6ccc9c3']
    monitor_ec2_instances(instance_ids_to_monitor)

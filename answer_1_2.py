import boto3


def start_instances(num_instances, image_id=None, key_name=None, group_ids=None, instance_type=None, subnet_id=None):
    running_state = 'running'
    pending_state = 'pending'
    default_image_id = 'ami-0d5d9d301c853a04a'
    default_key_name = 'sand_key'
    default_group_ids = ['sg-06b586adaf0fe5caf']
    default_instance_type = 't2.micro'
    default_subnet_id = 'subnet-16bb3b5a'
    ec2_client = boto3.resource('ec2')
    res = ec2_client.create_instances(
        MaxCount=num_instances,
        MinCount=num_instances,
        ImageId=image_id or default_image_id,
        InstanceType=instance_type or default_instance_type,
        KeyName=key_name or default_key_name,
        SecurityGroupIds=group_ids or default_group_ids,
        SubnetId=subnet_id or default_subnet_id
    )

    pending_instance_ids = list(map(lambda x: x.id, res))
    running_instance_ids = list()
    other_state_instance = list()

    # Wait until all instances come into running state
    while pending_instance_ids:
        instance_list = ec2_client.instances.filter(InstanceIds=pending_instance_ids).all()
        pending_instance_ids = list()

        for instance in instance_list:
            instance_state = instance.state.get('Name')
            if instance_state == running_state:
                running_instance_ids.append(instance.id)
            elif instance_state == pending_state:
                pending_instance_ids.append(instance.id)
            else:
                other_state_instance.append("{} - {}".format(instance.id, instance_state))
    if other_state_instance:
        print('Some instance went into unknonwn state!!')
        print('\n'.join(other_state_instance))

    return running_instance_ids


if __name__ == '__main__':
    instance_ids = start_instances(3)
    print("Ids of newly created instances: {}".format(' '.join(instance_ids)))

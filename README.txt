Prerequisite:
	- Make sure you have an account on Amazon AWS and one user is created.
	- Install Python 3.7 on the system.
	- Open terminal and cd to the directory where this README.txt file is present and then install required libraries by following command:
		pip install -r requirements.txt
	- Get the access_key_id and secret_access_key from AWS Console and setup in the system using following command:
		aws configure
	- Create a security group and authorize it as follows:
		aws ec2 create-security-group --group-name sand_security --description "Security Group"
		aws ec2 authorize-security-group-ingress --group-name sand_security --protocol tcp --port 22 --cidr 0.0.0.0/0
	- Create a key pair and save in pem file also provide the appropriate permissions to it as follows:
		aws ec2 create-key-pair --key-name sand_key --query 'KeyMaterial' --output text > sand_security.pem 
		chmod 400 sand_security.pem
	- Install the docker on the system


- Running the programs
	- Answer 1.1
		- Start the ec2 instance via following command.
			aws ec2 run-instances \
			--image-id ami-0d5d9d301c853a04a \
			--key-name sand_key \
			--security-group-ids sg-06b586adaf0fe5caf \
			--instance-type t2.micro \
			--subnet-id subnet-16bb3b5a
		- Copy the ip of instance from the output of above command or use the amazon console.
		- Get the public ip using following command or via AWS Console
			aws ec2 describe-instances --instance-ids [instance_id]
		- Connect to instance using following command
			ssh -i [path to sand_security.pem file] ubuntu@[public_domain_of_instance]

	- Answer 1.2
		- update the number of instance to create in the file answer_1_2.py and run the program as follows 
			python answer_1_2.py

	- Answer 1.3
		- update the source_bucket_name and dest_bucket_name in the file answer_1_3.py and run the program as follows 
			python answer_1_3.py

	- Answer 1.4
		- Create one instance using answer_1_2.py and connect to it.
		- Install Docker and pull the image via below command:
			sudo docker pull hnmn3/sandy_ubuntu_pyspark
		- Start one container using pulled image
			sudo docker run --name sandy_ubuntu_pyspark -p 2222:22\ -itd hnmn3/sandy_ubuntu_pyspark
		- Attach to the container
			sudo docker exec -it sandy_ubuntu_pyspark bash
		- Here port 2222 is bind to 22 port of container, so whichever port you bind make sure to allow connetions on that via AWS Console's security group.

		- Now connect to this newly created container from external host using below command.
			ssh -p 2222 [public_domain_of_instance]

		- Run the word_count.py file via following command:
			spark-submit word_count.py

	- Answer 2.1
		- Create any number of instance via script answer_1_2.py and put their ids in file answer_2_1.py
		- Run the program via following command 
			python answer_2_1.py 

	- Answer 2.2
		- Create any number of instance via script answer_1_2.py and put their ids in file answer_2_1.py
		- Now install docker on each instance and create some containers with ubuntu image.
		- Now run the program via following command 
			python answer_2_2.py 


	



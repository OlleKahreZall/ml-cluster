# README #

### Repository for project 3 Data Engineering 2 course ###

* Setting up the cluster
* Setting up Git hooks

### Setting up the cluster ###

Install necessary packages:
```
sudo apt install python3-openstackclient
sudo apt install python3-novaclient
sudo apt install python3-keystoneclient
```

1 - Create cluster keys to access the VMs:
```
ssh-keygen
```
Specify folder ~/cluster-keys to store the public and private key

2 - We need authorization to deploy machines on the cluster:

```
source ~/UPPMAX\ 2020_1-3-openrc.sh
```

3 - Then, we need to run the start_instances script to deploy the production server and the development server.
	Go to model_serving/openstack-client/single_node_with_docker_ansible_client. First modify the key_name filed for your own ssh key. Then run:
	
```
python3 start_instances.py
```


4 - Next, on the client VM run:
```
sudo vim /etc/ansible/hosts
```
Change the IPs for the production and development server for the current ones.

5 - ssh to each of the new VMs to check that they are deployed correctly and we can access them:
```
ssh -i ~/cluster-keys/cluster-key appuser@192.168.2.X
```

6 - Finally run the ansible configuration file to apply the changes on the machines
```
ansible-playbook configuration.yml --private-key=/home/ubuntu/cluster-keys/cluster-key
```

### Setting up Git Hooks

1 - Login to the development server and generate a new SSH key
```
$ ssh -i cluster-key appuser@192.168.2.X
$ ssh-keygen
```

2 - Press enter three times. This will put the new keys in this path '/home/appuser/.ssh/' and not assigning a password.

3 - After that copy the public key '/home/appuser/.ssh/id_rsa.pub' and put it in the '/home/appuser/.ssh/authorized_keys' file (production server).

4 - While in the production server, create a new directory in tbe 'home/appuser' directory. In additon, create an empty git repository in this new folder.

```
$ mkdir new_models
$ cd new_models
$ git init --bare
```

5 - Then create a git hook post-receive file, copy the conent of the bash script and change the permissions of the file.

```
$ nano hooks/post-receive
```
```
#!/bin/bash
while read oldrev newrev ref
do
  if [[ $ref =~ .*/master$ ]];
  then
    echo "Master ref received. Deploying master branch to production..."
    sudo git --work-tree=/model_serving/ci_cd/production_server --git-dir=/home/appuser/new_models checkout -f
  else
  echo "Ref $ref successfully received. Doing nothing: only the master branch may be deployed on this server."
 fi
done
```
```
$ sudo chmod +x hooks/post-receive
```
 6 - Exit the production server and login to the development server. Create a new folder in '/home/appuser' and initialize an empty git repository.
 
 ```
 $ mkdir new_models
 $ git init 
 ```
7 - Go back to '/home/appuser' and clone the GitHub repository. Next, install pip, sklearn and pandas. After that, run the Python scripts that you want to be executed in the '/home/appuser/model_serving/training’ folder.
```
$ git clone https://github.com/OlleKahreZall/model_serving.git
$ sudo apt install python3-pip
$ pip3 install sklearn
$ pip3 install pandas
$ cd model_serving
$ python3 bagging.py
```
8 – The saved models have been stored in the '/home/appuser/model_serving/training/models' folder. Copy the saved models and put it in the '/home/appuser/new_models' folder (which is connected to the production server).
```
$ cd ..
$ cp model_serving/training/models/* ~/new_models
```


9 - Now, make the commits and connect to the production server.

```
$ git add .
$ git commit -m "Added new models"
$ git remote add production appuser@192.168.2.X:/home/appuser/new_models
$ git push production master
```

9 - Visit the production server's website to see the new results.


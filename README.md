# README #

This README would normally document whatever steps are necessary to get your application up and running.

### What is this repository for? ###

* Quick summary
* Version
* [Learn Markdown](https://bitbucket.org/tutorials/markdowndemo)

### Setting up the cluster ###

1 - Create cluster keys to access the VMs:
```
ssh-keygen
```

2 - We need authorization to deploy machines on the cluster:

```
source ~/UPPMAX\ 2020_1-3-openrc.sh
```

3 - Then, we need to run the start_instances script to deploy the production server and the development server.
	Go to github_stargazers/model_serving/openstack-client/single_node_with_docker_ansible_client and run:
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
? - To be able to train the models in the development server, the following Python modules are needed:
```
$ sudo apt install python3-pip
$ pip3 install sklearn
$ pip3 install pandas
```
7 - Go back to '/home/appuser' and clone the GitHub repository. Then copy the content in the '/home/appuser/model_serving/training/models' folder to the '/home/appuser/new_models' folder.

```
$ cd ..
$ git clone https://github.com/OlleKahreZall/model_serving.git
$ cp model_serving/training/models/* ~/new_models
```

8 - Now, make the commits and connect to the production server.

```
$ git add .
$ git commit -m "Added new models"
$ git remote add production appuser@192.168.2.X:/home/appuser/new_models
$ git push production master
```

9 - Visit the production server's website to see the new results.


* Summary of set up
* Configuration
* Dependencies
* Database configuration
* How to run tests
* Deployment instructions

### Contribution guidelines ###

* Writing tests
* Code review
* Other guidelines

### Who do I talk to? ###

* Repo owner or admin
* Other community or team contact

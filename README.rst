#### HEAD-COUNT DETECTION using APACHE MESOS

#### STEP 1: Clone or download cloudmesh.mesos repository to local machine in '~/github/' directory

    git clone https://github.com/cloudmesh/cloudmesh.mesos.git 

#### STEP 2: Install & configure Ansible and Cloudmesh Client using their respective documentations
    http://docs.ansible.com/ansible/intro_installation.html  
    http://cloudmesh.github.io/client/installation.html

#### STEP 3: Create a secgroup with the following ports open
    
    5050 - required for master
    
    5051 - required for agents
    
    80, 443, 22 - for HTTP, HTTPS and SSH respectively
    
    Preferably all tcp and icmp ports should be open
    
    (In this deployment, a secgroup named mesos-secgroup is used. It can be changed as required in the scripts/create-cluster.sh)

#### STEP 4: Start deployment

    ./scripts/deploy-mesos.sh

#### STEP 5: Get the IP addresses of the nodes of the deployed cluster

    cm cluster nodes
    
#### STEP 6: ssh into each VM and run the following commands from the '~/mesos-1.2.0/build/' directory for each VM

    sudo make
    
    sudo make check -j 2 V=0
    
#### STEP 7: Run mesos-master

    ./scripts/run-master.sh
        
#### STEP 8: Run agent 1

    ./scripts/run-agent1.sh
    
#### STEP 7: Run agent 2

    ./scripts/run-agent2.sh
    
#### STEP 8: Run framework

    ./scripts/run-framework.sh

#### HEAD-COUNT DETECTION using APACHE MESOS

#### STEP 1: Clone or download cloudmesh.mesos repository to local machine in '~/github/' directory

    git clone https://github.com/cloudmesh/cloudmesh.mesos.git 

#### STEP 2: Install & configure Ansible and Cloudmesh Client using their respective documentations
    http://docs.ansible.com/ansible/intro_installation.html  
    http://cloudmesh.github.io/client/installation.html

#### STEP 3: Create a secgroup with the following ports open
    
    5050 - required for master <br />
    5051 - required for agents <br />
    80, 443, 22 - for HTTP, HTTPS and SSH respectively <br />
    Preferably all tcp and icmp ports should be open <br />
    (In this deployment secgroup named mesos-secgroup is used but it can be changed in the scripts/create-cluster.sh) <br />

#### STEP 4: Start deployment

    ./scripts/deploy-mesos.sh
    

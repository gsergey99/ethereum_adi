# Add ethereum ppa
add-apt-repository ppa:ethereum/ethereum

# Add ethereum-dev ppa
add-apt-repository ppa:ethereum/ethereum-dev

# Add ethereum libs ppa
add-apt-repository ppa:ethereum/cpp-build-deps

# Apt update
apt update

# Download setup_10.x
wget -q https://deb.nodesource.com/setup_10.x -P /tmp/

# Add execute permissions to setup_10.x
chmod 744 /tmp/setup_10.x

# Execute setup_10.x
/tmp/setup_10.x

# Install depends
apt install -y net-tools build-essential solc ethereum nodejs python3-pip ruby-full docker.io dos2unix

# Install truffle
npm install -g truffle@5.0.5

# Install pip3 dependencies
pip3 install web3==5.15.0 PyYAML==5.4.1 tox==2.5.0 eth_account==0.5.4

# Get kubectl
wget -q https://storage.googleapis.com/kubernetes-release/release/v1.14.2/bin/linux/amd64/kubectl -P /tmp/

# Add execute permissions to kubectl
chmod 755 /tmp/kubectl

# Move kubectl to path
mv /tmp/kubectl /usr/local/bin/kubectl

# Get minikube
wget -q https://storage.googleapis.com/minikube/releases/v1.14.2/minikube-linux-amd64 -P /tmp/

# Change minikube name
mv /tmp/minikube-linux-amd64 /tmp/minikube

# Add execute permissions to minikube
chmod 755 /tmp/minikube

# Move minikube to path
mv /tmp/minikube /usr/local/bin/minikube

# Add user to group docker
usermod -aG docker vagrant

# Create project directory
mkdir /home/vagrant/ethereum-adi

# Copy project
cp -r /vagrant/* /home/vagrant/ethereum-adi

# Change CRLF to LF
find /home/vagrant/ethereum-adi/ -type f -print0 | xargs -0 dos2unix

# Change owner of the project
chown vagrant:vagrant -R /home/vagrant/ethereum-adi/

# Disable minikube update notice
minikube config set WantUpdateNotification false

# Start the network
runuser -l vagrant -c 'cd /home/vagrant/ethereum-adi/network && python3 /vagrant/network/clustETHr.py -s'

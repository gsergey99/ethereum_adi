def external_iface()
  return `ip route | awk '/^default via/ {printf "%s", $5}'`
end

Vagrant.configure("2") do |config|
    config.vm.box = "ubuntu/bionic64"
    config.vm.provider :virtualbox do |vb|
      vb.memory = 16384
      vb.cpus = 4
    end

    config.vm.define "adi" do |node|
      node.vm.hostname = "adi"
      node.vm.network "public_network", bridge: external_iface(), use_dhcp_assigned_default_route: true
    end
    
    config.vm.provision "shell", path: "provision.sh"
end

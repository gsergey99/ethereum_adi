Vagrant.configure("2") do |config|
    config.vm.box = "ubuntu/bionic64"
    config.vm.provider :virtualbox do |vb|
      vb.memory = 4096
      vb.cpus = 2
    end

    config.vm.define "adi" do |node|
      node.vm.hostname = "adi"

      node.vm.provision "ansible" do |ansible|
        ansible.verbose = "v"
        ansible.playbook = "playbook-main.yml"
      end
    end
end
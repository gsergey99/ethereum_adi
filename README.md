# ethereum_adi
Repositorio del proyecto final de ADI

#### Versions

- Ansible >= 2.9
- Vagrant >= 2.2.6
- virtualbox >= 6.1

### Before how to run
Es necesario instalar virtualbox con su paquete de extensión.

```
apt install virtualbox virtualbox-ext-pack
```

#### How to run
Para iniciar el entorno de trabajo:

```
vagrant up
vagrant ssh adi
ganache-cli
```

Modificar el fichero truffle-config.js para que se conecte a ganache-cli:
```
module.exports = {
  networks: {
    development: {
      host: "localhost",
      port: 8545,
      network_id: "*"
    }
  }
};
```

Iniciar ganache-cli:
```
ganache-cli
```

### Versiones para la red

- kubectl: 1.14.2
- kuberneter: 1.14.2
- minikube: 1.14.2
- Truffle: 5.0.5
- PyYAML: 5.3.1

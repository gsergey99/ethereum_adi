# Proyecto final de Aplicaciones Distribuidas en Internet: Introducción a blockchains.

Basado en [Ethereum POA (Clique) on Kubernetes](https://medium.com/@edi.sinovcic/ethererum-poa-clique-on-kubernetes-6e86fed0c310).

Como entorno de laboratorio necesitamos una máquina Windows o Linux con las siguientes versiones:

- python>= 3.8.6
- vagrant >= 2.2.14
- virtualbox >= 6.1
- guest additions >= 5.2.42

*Estas son las que se han probado, lo que no quita que otras sean posibles.*

#### Se creará una máquina virtual con los siguientes recursos: **4 vCPUs y 16 GB de RAM**.

### Despliegue de la red

- Clonamos el repositorio.
- Nos movemos a la carpeta `ethereum_adi`.
- Ejecutamos el script de python3 `start_network.py`.

Una vez este comando haya acabado tendremos una máquina virtual sobre la que se ejecutará el cluster de `Kubernetes` (usando `minikube`) donde se estará ejecutando la red de Ethereum POA.

### Uso del *frontend*

- Ejecutamos `vagrant ssh` para conectamos a la máquina virtual.
- Nos movemos al directorio `ethereum_adi/frontend`.
- Ejecutamos: `python3 votaciones_cli.py`.

#### Ejecución de la *test suite*

- Ejecutamos `vagrant ssh` para conectamos a la máquina virtual.
- Nos movemos al directorio `ethereum_adi/frontend`.
- Ejecutamos: `tox`.


### 3rd parties utilizadas 

#### apt-get

- net-tools 
- build-essential 
- solc 
- ethereum 
- nodejs 
- python3
- python3-pip 
- ruby-full 
- docker.io 
- dos2unix

#### pip3
- PyYAML
- web3
- tox
- eth_account

#### npm

- truffle
- ganache-cli

#### Otros 

- kubectl
- kubernetes
- minikube
- vagrant

- virtualbox
- virtualbox-guest-additions

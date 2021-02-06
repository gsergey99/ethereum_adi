# Proyecto final de Aplicaciones Distribuidas en Internet: Introducción a blockchains.

Basado en [Ethereum POA (Clique) on Kubernetes](https://medium.com/@edi.sinovcic/ethererum-poa-clique-on-kubernetes-6e86fed0c310).

Como entorno de laboratorio necesitamos una máquina Windows o Linux con las siguientes versiones:

- python>= 3.8.6
- vagrant >= 2.2.14
- virtualbox >= 6.1
- virtualbox-guest-additions >= 5.2.42

*Estas son las que se han probado, lo que no quita que otras sean posibles.*

#### Se creará una máquina virtual con los siguientes recursos: **4 vCPUs y 16 GB de RAM**.

### Despliegue de la red

- Clonamos el repositorio.
- Nos movemos a la carpeta `ethereum_adi`.
- Ejecutamos el script de python3 `start_network.py`.

Una vez este comando haya acabado tendremos una máquina virtual sobre la que se ejecutará el cluster de `Kubernetes` (usando `minikube`) donde se estará ejecutando la red de Ethereum POA.

La red consta de un *bootnode*, tres nodos mineros, un nodo monitor y un nodo explorador. El nodo monitor y el nodo explorar cuentan con una interfaz web en el puerto 3001 y 3000 respectivamente. Estas interfaces estarán disponibles una vez se haya desplegado la red por completo.

### Control de la red

#### Añadir un nodo a la red

- Ejecutamos `vagrant ssh` para conectamos a la máquina virtual.
- Nos movemos al directorio `ethereum_adi/network`.
- Ejecutamos: `python3 clustETHr.py -a`.

#### Quitar un nodo a la red

- Ejecutamos `vagrant ssh` para conectamos a la máquina virtual.
- Nos movemos al directorio `ethereum_adi/network`.
- Ejecutamos: `python3 clustETHr.py -r`.

#### Monitorizar la red

- Ejecutamos `vagrant ssh` para conectamos a la máquina virtual.
- Nos movemos al directorio `ethereum_adi/network`.
- Ejecutamos: `python3 clustETHr.py -w`.

#### Destruir la red

- Ejecutamos `vagrant ssh` para conectamos a la máquina virtual.
- Nos movemos al directorio `ethereum_adi/network`.
- Ejecutamos: `python3 clustETHr.py -d`.

### Uso del *frontend*

- Ejecutamos `vagrant ssh` para conectamos a la máquina virtual.
- Nos movemos al directorio `ethereum_adi/frontend`.
- Ejecutamos: `python3 votaciones_CLI.py`.

#### Ejecución de la *test suite* de integración

- Ejecutamos `vagrant ssh` para conectamos a la máquina virtual.
- Nos movemos al directorio `ethereum_adi/frontend`.
- Ejecutamos: `tox`.

#### Ejecución de la *test suite* del *smart contract*

- Ejecutamos `vagrant ssh` para conectamos a la máquina virtual.
- Nos movemos al directorio `ethereum_adi/frontend`.
- Ejecutamos: `sudo truffle test --network 123456`.


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

### Autores

|              Miembro              |    DNI    |              Rol             |
|:---------------------------------:|:---------:|:----------------------------:|
|      Sergio Jiménez del Coso      | 45774386Q |      Backend / Frontend      |
|       Héctor Moreno Sánchez       | 02318660F |      Backend / Frontend      |
|       Raúl Bernalte Sánchez       | 71360779J |      Backend / Frontend      |
|         Ismael Vélez Recio        | 50355567B |      Backend / Frontend      |
|         Juan Romero Cañas         | 05939767V | Red Blockchain / Integración |
| Enrique Adrián Villarrubia Martín | 05722202D | Red Blockchain / Integración |


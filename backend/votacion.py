import sys
import json

from web3 import Web3, HTTPProvider

class Votacion:
    
    def  __init__ (self, contract, w3, owner):
        
        self.w3 = w3
        self.owner = owner
        self.contract = contract

   
    def crear_votacion(self):
        '''
        Creación de una votación
        '''
        print('GAS estimation:', self.contract.functions.crearVotacion().estimateGas())
        transaccion = self.contract.functions.crearVotacion().transact({'from': self.owner})  
        
        receipt = self.w3.eth.getTransactionReceipt(transaccion)
        print(receipt)

        block_id = receipt['blockNumber'] - 1
        votacion_id = self.contract.functions.crearVotacion().call(block_identifier=block_id)
        
        return votacion_id


    def add_candidato(self, votacion_id, candidato):
        '''
        Añadir un único candidato
        '''
        print('GAS estimation:', self.contract.functions.addCandidato(votacion_id, candidato).estimateGas())
        transaccion = self.contract.functions.addCandidato(votacion_id, candidato).transact({'from': self.owner})

        receipt = self.w3.eth.getTransactionReceipt(transaccion)
        print(receipt)


    def cerrar_lista(self, votacion_id):
        '''
        Cerrar lista de candidatos
        '''
        print('GAS estimation:', self.contract.functions.cerrarLista(votacion_id).estimateGas())
        transaccion = self.contract.functions.cerrarLista(votacion_id).transact({'from': self.owner})
        receipt = self.w3.eth.getTransactionReceipt(transaccion)
        print(receipt)

    def cerrar_votacion(self, votacion_id):
        '''
        Cerrar una única votación
        '''
        print('GAS estimation:', self.contract.functions.cerrarEncuesta(votacion_id).estimateGas())
        transaccion = self.contract.functions.cerrarEncuesta(votacion_id).transact({'from': self.owner})
        receipt = self.w3.eth.getTransactionReceipt(transaccion)
        print(receipt)


    def votar(self, votacion_id, candidato):
        '''
        Votar a un candidato
        '''
        print('GAS estimation:', self.contract.functions.votar(votacion_id, candidato).estimateGas())
        transaction = self.contract.functions.votar(votacion_id, candidato).transact({'from': self.owner})
        receipt = self.w3.eth.getTransactionReceipt(transaction)
        print(receipt)
 

    def listar_candidatos(self, votacion_id):
        '''
        Listar nombres de los candidatos
        '''
        candidatos = self.contract.functions.listaCandidatos(votacion_id).call()
        return candidatos

 

    def ver_ganador(self, votacion_id):
        '''
        Obtener ganador de una votación
        '''
        ganador = self.contract.functions.ganador(votacion_id).call()
        return ganador


class Transaccion:

    def loadABI(self,binaryContractFile):
        '''
        Carga el ABI de la transaccion
        '''
        with open(binaryContractFile, 'r') as contents:
            contract = json.load(contents)
        if 'abi' not in contract:
            raise RuntimeError('PTTTTTTTTTRRRRRR!!')
        return contract['abi']
    
    def loadAddress(self,file_name):
        '''
        Lectura de la dirección del contractAddress de la red
        '''

        with open(file_name,'r') as json_file:
            storage = json.load(json_file)

        return storage['address']

    
    def run(self):
    
        w3 = Web3(HTTPProvider('http://localhost:8545'))

        if not w3.isConnected():
            print('Cannot connect to node!')
            sys.exit(1)
        print('Node connected')

        print('Blockchain size: %s' % w3.eth.blockNumber)
        blockNumber = w3.eth.blockNumber - 1
        if blockNumber < 0:
            print('Blockchain is in the genesis block')
            sys.exit(0)
        
        try:
            contractAddress = self.loadAddress('address.json')
            
        except KeyError:
            print('No contract address found!')
            sys.exit(1)

        
        contract = w3.eth.contract(
            address = contractAddress,
            abi = self.loadABI('build/contracts/Votaciones.json')
        )
        owner = w3.eth.accounts[0]
        
        votacion = Votacion(contract, w3, owner)
        
        votacion.crear_votacion() 
        votacion.add_candidato(0, 'Raul')
        votacion.add_candidato(0,'Hector')
        lista = votacion.listar_candidatos(0)
        votacion.cerrar_lista(0)
        votacion.votar(0,'Hector')
        votacion.cerrar_votacion(0)
        gana=votacion.ver_ganador(0)
        print(gana)

if __name__ == "__main__":

    transaccion = Transaccion()
    sys.exit(transaccion.run())
    


import sys
import json

from web3 import Web3, HTTPProvider, exceptions

class Votation:
    
    def  __init__ (self, contract, w3, owner):
        
        self.w3 = w3
        self.owner = owner
        self.contract = contract

    
    def choose_option(self):
        '''
        Método para elegir la opción correspondiente
        '''

        option = 0

        while True:
            try:
                option = int(input("-> Introduce la opción: "))
                break

            except ValueError:
                print('¡¡¡Error, no se ha introducido algún valor correcto!!! \n')
        return option
    
    
    def run(self):
        '''
        Inicio del menú de interacción
        '''

        while True:
            try:

                print('****** SISTEMA DE VOTACIONES ******')
                print('\t 1. Crear votación \n',
                '\t 2. Añadir candidato a una votación \n',
                '\t 3. Cerrar lista de candidatos \n',
                '\t 4. Votar candidato \n',
                '\t 5. Consultar candidatos \n',
                '\t 6. Consultar resultado de los candidatos \n',
                '\t 7. Cerrar votación \n',
                '\t 8. Salir \n')
                opt = self.choose_option()

                if(opt > 0 and opt <8):

                    operaciones = {
                    '1': self.create_votation,
                    '2': self.add_candidate,
                    '3': self.close_list,
                    '4': self.vote,
                    '5': self.list_candidates,
                    '6': self.view_winner,
                    '7': self.close_votation
                    }
                    operaciones[str(opt)]()

                elif (opt == 8):
                    print('¡Buen día! \n')
                    sys.exit(0)
                else:
                    print('\t ¡¡¡Error, no se ha introducido una opcion correcta!!!')
            
            except KeyboardInterrupt:
                print('\n ¡Buen día! \n')
                sys.exit(0) 

    def create_votation(self):
        '''
        Creación de una votación
        '''
        print('GAS estimation:', self.contract.functions.crearVotacion().estimateGas())
        transaction = self.contract.functions.crearVotacion().transact({'from': self.owner})  
        
        receipt = self.w3.eth.getTransactionReceipt(transaction)
        print(receipt)

        block_id = receipt['blockNumber'] - 1
        
        try:
            votacion_id = self.contract.functions.crearVotacion().call(block_identifier=block_id)
        
        except exceptions.Solidity as error:
            print(error)
            
        
        print(f'Votación creada. (Id. votación: {votacion_id})')
        

    def add_candidate(self):
        '''
        Añadir un único candidato a un único id
        '''
        votation_id = 0
        candidate = ''
                
        while True:
            try:
                votation_id = int(input("-> Introduce identificador de votación: "))
                candidate = input("-> Introduce candidato: ")
                break

            except ValueError:
                print('¡¡¡Error, no se ha introducido algún valor correcto!!!\n')

        try:
            print('GAS estimation:', self.contract.functions.addCandidato(votation_id, candidate).estimateGas())

            transaction = self.contract.functions.addCandidato(votation_id, candidate).transact({'from': self.owner})
            receipt = self.w3.eth.getTransactionReceipt(transaction)
            print(receipt)
            print(f'Candidato "{candidate}" añadido. (Id. votación: {votation_id}) \n')
            
        except exceptions.SolidityError as error:
            print('\n¡¡¡Error!!!, el candidato está añadido \n')
            print(error)


    def close_list(self):
        '''
        Cerrar lista de candidatos
        '''
        votation_id = 0

        while True:
            try:

                votation_id = int(input("-> Introduce identificador de votación: "))
                break
            
            except ValueError:
                print('¡¡¡Error, no se ha introducido algún valor correcto!!! \n')

        try:
            print('GAS estimation:', self.contract.functions.cerrarLista(votation_id).estimateGas())
            transaction = self.contract.functions.cerrarLista(votation_id).transact({'from': self.owner})
            receipt = self.w3.eth.getTransactionReceipt(transaction)
            print(receipt)
            print(f'Lista de candidatos cerrada. (Id. votación: {votation_id}) \n')

        except exceptions.SolidityError:
            print('\n¡¡¡Error!!!, la lista de candidatos no está cerrada \n')


    def close_votation(self):
        '''
        Cerrar una única votación
        '''
        while True:
            try:

                votation_id = int(input("-> Introduce identificador de votación: "))
                break

            except ValueError:
                print('¡¡¡Error, no se ha introducido algún valor correcto!!! \n')


        try:
            print('GAS estimation:', self.contract.functions.cerrarEncuesta(votation_id).estimateGas())
            transaction = self.contract.functions.cerrarEncuesta(votation_id).transact({'from': self.owner})
            receipt = self.w3.eth.getTransactionReceipt(transaction)
            print(receipt)
            print(f'Votación cerrada. (Id. votación: {votation_id}) \n')

        except exceptions.SolidityError:
            print('\n¡¡¡Error!!!, la votación no está cerrada \n')


    def vote(self):
        '''
        Votar a un candidato
        '''
        votation_id = 0
        candidate = ''

        while True:
            try:

                votation_id = int(input("-> Introduce identificador de votación: "))
                candidate = input("-> Introduce candidato: ")
                break

            except ValueError:
                print('¡¡¡Error, no se ha introducido algún valor correcto!!! \n')

        try:
            print('GAS estimation:', self.contract.functions.votar(votation_id, candidate).estimateGas())
            transaction = self.contract.functions.votar(votation_id, candidate).transact({'from': self.owner})
            receipt = self.w3.eth.getTransactionReceipt(transaction)
            print(receipt)
            print(f'Candidato "{candidate}" votado. (Id. votación: {votation_id})')

        except exceptions.SolidityError:
            print('\n¡¡¡Error!!!, la votación no se ha realizado correctamente. Indique de la ID de la votación y el candidato \n')


    def list_candidates(self):
        '''
        Listar nombres de los candidatos
        '''
        votation_id = 0

        while True:
            try:

                votation_id = int(input("-> Introduce identificador de votación: "))
                break

            except ValueError:
                print('¡¡¡Error, no se ha introducido algún valor correcto!!! \n')

        print(f'Candidatos (Id. votación: {votation_id}): ')
        
        try:
            candidates = self.contract.functions.listaCandidatos(votation_id).call()
            for candidate in candidates:
                print(f'\t \t - {candidate} ')
        
        except exceptions.SolidityError:
            print('\n¡¡¡Error!!!, la lista de candidatos no está disponible \n')

    def view_winner(self):
        '''
        Obtener ganador de una votación
        '''
        votation_id = 0

        while True:
            try:

                votation_id = int(input("-> Introduce identificador de votación: "))
                break

            except ValueError:
                print('¡¡¡Error, no se ha introducido algún valor correcto!!! \n')

        try:
            winner = self.contract.functions.ganador(votation_id).call()
            print(f'Candidato "{winner}" ganador. (Id. votación: {votation_id})')
        
        except exceptions.SolidityError:
            print('\n¡¡¡Error!!!, el candidato ganador no está disponible \n')
        


class Conection:

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
        
        votation = Votation(contract, w3, owner)
        
        return votation
        

if __name__ == "__main__":

    conection = Conection()
    votation = conection.run()
    sys.exit(votation.run())
    
    

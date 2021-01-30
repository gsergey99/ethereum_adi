#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import json
from web3 import Web3, HTTPProvider, exceptions
from web3.middleware import geth_poa_middleware

class Votation:
    
    def  __init__ (self, contract, w3, owner):
        self.w3 = w3
        self.w3.middleware_onion.inject(geth_poa_middleware, layer=0)
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
                print('\n****** SISTEMA DE VOTACIONES ******')
                print('\t 1. Crear votación \n',
                '\t 2. Añadir candidato a una votación \n',
                '\t 3. Votar candidato \n',
                '\t 4. Cerrar lista de candidatos \n',
                '\t 5. Cerrar votación \n',
                '\t 6. Consultar ganador \n',
                '\t 7. Consultar candidatos\n',
                '\t 8. Consultar resultados de los candidatos \n', 
                '\t 9. Salir \n')
                opt = self.choose_option()

                if (opt > 0 and opt < 9):
                    operaciones = {
                        '1': self.create_votation,
                        '2': self.add_candidate,
                        '3': self.vote,
                        '4': self.close_list,
                        '5': self.close_votation,
                        '6': self.view_winner,
                        '7': self.list_candidates,
                        '8': self.list_results
                    }

                    if (opt == 1):
                        operaciones[str(opt)]()

                    elif (opt > 3 and opt < 9):
                        while True:
                            try:
                                votation_id = int(input("-> Introduce identificador de votación: "))
                                args = [votation_id]
                                break
                                                        
                            except ValueError:
                                print('¡¡¡Error, no se ha introducido algún valor correcto!!! \n')
                            
                        operaciones[str(opt)](*args)
                    
                    elif (opt > 1 and opt < 4):
                        while True:
                            try:
                                votation_id = int(input("-> Introduce identificador de votación: "))
                                candidate = input("-> Introduce candidato: ")
                                args = [votation_id, candidate]
                                break
                            except ValueError:
                                print('¡¡¡Error, no se ha introducido algún valor correcto!!!\n')

                        operaciones[str(opt)](*args)
                elif (opt == 9):
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
        
        receipt = self.w3.eth.waitForTransactionReceipt(transaction)
        block_id = receipt['blockNumber'] - 1
        
        try:
            votation_id = self.contract.functions.crearVotacion().call(block_identifier=block_id)
        
            print(f'Votación creada. (Id. votación: {votation_id})')

            return votation_id
        except exceptions.Solidity as error:
            raise Exception('Error en la creación de la votación \n') 

    def add_candidate(self, *args):
        '''
        Añadir un único candidato a un único id
        '''
        votation_id = args[0]
        candidate = args[1]

        try:
            print('GAS estimation:', self.contract.functions.addCandidato(votation_id, candidate).estimateGas())

            transaction = self.contract.functions.addCandidato(votation_id, candidate).transact({'from': self.owner})
            receipt = self.w3.eth.waitForTransactionReceipt(transaction)

            print(f'Candidato "{candidate}" añadido. (Id. votación: {votation_id}) \n')
            
            return receipt['status']
        except exceptions.SolidityError:
            raise Exception('\n¡¡¡Error!!!, el candidato está añadido \n')

    def close_list(self, *args):
        '''
        Cerrar lista de candidatos
        '''
        votation_id = args[0]

        try:
            print('GAS estimation:', self.contract.functions.cerrarLista(votation_id).estimateGas())
            transaction = self.contract.functions.cerrarLista(votation_id).transact({'from': self.owner})
            receipt = self.w3.eth.waitForTransactionReceipt(transaction)

            print(f'Lista de candidatos cerrada. (Id. votación: {votation_id}) \n')
            
            return receipt['status']
        except exceptions.SolidityError:
            raise Exception('\n¡¡¡Error!!!, la lista de candidatos no se ha cerrado correctamente \n')

    def close_votation(self, *args):
        '''
        Cerrar una única votación
        '''
        votation_id = args[0]

        try:
            print('GAS estimation:', self.contract.functions.cerrarEncuesta(votation_id).estimateGas())
            transaction = self.contract.functions.cerrarEncuesta(votation_id).transact({'from': self.owner})
            receipt = self.w3.eth.waitForTransactionReceipt(transaction)

            print(f'Votación cerrada. (Id. votación: {votation_id}) \n')
    
            return receipt['status']
        except exceptions.SolidityError:
            raise Exception('\n¡¡¡Error!!!, la votación no está cerrada \n')

    def vote(self, *args):
        '''
        Votar a un candidato
        '''
        votation_id = args[0]
        candidate = args[1]

        try:
            print('GAS estimation:', self.contract.functions.votar(votation_id, candidate).estimateGas())
            transaction = self.contract.functions.votar(votation_id, candidate).transact({'from': self.owner})
            receipt = self.w3.eth.waitForTransactionReceipt(transaction)
            
            print(f'Candidato "{candidate}" votado. (Id. votación: {votation_id})')

            return receipt['status']
        except exceptions.SolidityError:
            raise Exception('\n¡¡¡Error!!!, la votación no se ha realizado correctamente. Indique de la ID de la votación y el candidato \n')

    def list_candidates(self, *args):
        '''
        Listar nombres de los candidatos
        '''
        votation_id = args[0]

        print(f'Candidatos (Id. votación: {votation_id}): ')
        
        try:
            candidates = self.contract.functions.listaCandidatos(votation_id).call()
            for candidate in candidates:
                print(f'\t \t - {candidate} ')
        
            return candidates
        except exceptions.SolidityError:
            raise Exception('\n¡¡¡Error!!!, la lista de candidatos no está disponible \n')

    def view_winner(self,*args):
        '''
        Obtener ganador de una votación
        '''
        votation_id = args[0]

        try:
            winner = self.contract.functions.ganador(votation_id).call()
            print(f'Candidato "{winner}" ganador. (Id. votación: {votation_id})')
        
            return winner
        except exceptions.SolidityError:
            raise Exception('\n¡¡¡Error!!!, el candidato ganador no está disponible \n')
        
    def list_results(self,*args):
        '''
        Obtener resultados de los candidatos
        '''
        votation_id = args[0]

        try:
            list_results = self.contract.functions.listaVotos(votation_id).call()
            candidates = self.contract.functions.listaCandidatos(votation_id).call()

            for i in range(len(candidates)):
                print(f'\t \t - {candidates[i]} --- {list_results[i]} votos')
        except exceptions.SolidityError:
            raise Exception('\n¡¡¡Error!!!, la votación no ha terminado \n')


class Connection:

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
            contractAddress = self.loadAddress('../backend/address.json')
        except KeyError:
            print('No contract address found!')
            sys.exit(1)
        
        contract = w3.eth.contract(
            address = contractAddress,
            abi = self.loadABI('../backend/build/contracts/Votaciones.json')
        )
        owner = w3.eth.accounts[0]
        
        votation = Votation(contract, w3, owner)
        
        return votation
        

if __name__ == "__main__":
    try:
        connection = Connection()
        votation = connection.run()
        sys.exit(votation.run())
    
    except Exception as error:
        print(error)

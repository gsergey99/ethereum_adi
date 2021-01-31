#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from web3 import Web3, HTTPProvider, exceptions
from web3.middleware import geth_poa_middleware

class Connection:
    def connect(self):
        self.w3 = Web3(HTTPProvider('http://localhost:8545'))

        if not self.w3.isConnected():
            raise Exception('Cannot connect to node!')

        blockNumber = self.w3.eth.blockNumber - 1
        if blockNumber < 0:
            raise Exception('Blockchain is in the genesis block')
    
    def run(self, account_index):
        
        contractAddress = self._loadAddress('../backend/address.json')
        
        contract = self.w3.eth.contract(
            address = contractAddress,
            abi = self._loadABI('../backend/build/contracts/Votaciones.json')
        )
        owner = self.w3.eth.accounts[account_index]
        votation = Votation(contract, self.w3, owner)
        
        return votation

    def _loadABI(self,binaryContractFile):
        '''
        Carga el ABI de la transaccion
        '''
        with open(binaryContractFile, 'r') as contents:
            contract = json.load(contents)

        if 'abi' not in contract:
            raise RuntimeError('ABI not found in contract')

        return contract['abi']
    
    def _loadAddress(self,file_name):
        '''
        Lectura de la dirección del contractAddress de la red
        '''
        with open(file_name, 'r') as json_file:
            storage = json.load(json_file)

        return storage['address']

class Votation:
    def  __init__ (self, contract, w3, owner):
        self.w3 = w3
        self.w3.middleware_onion.inject(geth_poa_middleware, layer=0)
        self.owner = owner
        self.contract = contract

    def create_votation(self):
        '''
        Creación de una votación
        '''
        transaction = self.contract.functions.crearVotacion().transact({'from': self.owner})  
        receipt = self.w3.eth.waitForTransactionReceipt(transaction)

        block_id = receipt['blockNumber'] - 1
        votation_id = self.contract.functions.crearVotacion().call(block_identifier=block_id)

        return (receipt, votation_id)

    def add_candidate(self, votation_id, candidate):
        '''
        Añadir un único candidato a un único id
        '''
        transaction = self.contract.functions.addCandidato(votation_id, candidate).transact({'from': self.owner})
        receipt = self.w3.eth.waitForTransactionReceipt(transaction)
        
        return (receipt, None)

    def close_list(self, votation_id):
        '''
        Cerrar lista de candidatos
        '''
        transaction = self.contract.functions.cerrarLista(votation_id).transact({'from': self.owner})
        receipt = self.w3.eth.waitForTransactionReceipt(transaction)

        return (receipt, None)

    def close_votation(self, votation_id):
        '''
        Cerrar una única votación
        '''
        transaction = self.contract.functions.cerrarEncuesta(votation_id).transact({'from': self.owner})
        receipt = self.w3.eth.waitForTransactionReceipt(transaction)

        return (receipt, None)

    def vote(self, votation_id, candidate):
        '''
        Votar a un candidato
        '''
        transaction = self.contract.functions.votar(votation_id, candidate).transact({'from': self.owner})
        receipt = self.w3.eth.waitForTransactionReceipt(transaction)

        return (receipt, None)
    
    def list_candidates(self, votation_id):
        '''
        Listar nombres de los candidatos
        '''
        candidates = self.contract.functions.listaCandidatos(votation_id).call()
        return (None, candidates)

    def view_winner(self, votation_id):
        '''
        Obtener ganador de una votación
        '''
        winner = self.contract.functions.ganador(votation_id).call()
        return (None, winner)
        
    def list_results(self, votation_id):
        '''
        Obtener resultados de los candidatos
        '''
        list_results = self.contract.functions.listaVotos(votation_id).call()
        candidates = self.contract.functions.listaCandidatos(votation_id).call()
        
        results = []
        for i in range(len(candidates)):
            results.append((candidates[i], list_results[i]))
        
        return (None, results)



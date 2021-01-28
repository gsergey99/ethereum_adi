#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import json
import pprint

from web3 import Web3, HTTPProvider


def loadABI(binaryContractFile):
    with open(binaryContractFile, 'r') as contents:
        contract = json.load(contents)
    if 'abi' not in contract:
        raise RuntimeError('PTTTTTTTTTRRRRRR!!')
    return contract['abi']

if __name__ == '__main__':
    w3 = Web3(HTTPProvider('http://localhost:8545'))
    if not w3.isConnected():
        print('Cannot connect to node!')
        sys.exit(1)
    print('Node connected!')

    print('Blockchain size: %s' % w3.eth.blockNumber)
    blockNumber = w3.eth.blockNumber - 1
    if blockNumber < 0:
        print('Blockchain is in the genesis block')
        sys.exit(0)
    block = w3.eth.getBlock(blockNumber)
    try:
        transaction = block['transactions'][0]
    except (KeyError, IndexError):
        print('No transactions found!')
        sys.exit(1)

    receipt = w3.eth.getTransactionReceipt(transaction)
    try:
        contractAddress = receipt['contractAddress']
    except KeyError:
        print('No contract address found!')
        sys.exit(1)
    HelloWorld = w3.eth.contract(
        address=contractAddress,
        abi=loadABI('contracts/HelloWorld.json')
    )
    print('GAS estimation: %s' % HelloWorld.functions.hi().estimateGas())
    returnValue = HelloWorld.functions.hi().call()
    print('Contract return: %s' % returnValue)


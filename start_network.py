#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import time
import subprocess

def vagrant_up():
    os.system('vagrant up')

def forwarding_web3_miner01():
    print('⏩  Forwarding one miner node...')
    output = ''

    while output != b'Running':
        try:
            output = subprocess.check_output('vagrant ssh -c "kubectl get pod geth-miner01-0 -o jsonpath=\'{.status.phase}\'"', shell=True)
        except subprocess.CalledProcessError:
            output = ''
        time.sleep(1)

    os.system('vagrant ssh -c "nohup kubectl port-forward --address 0.0.0.0 geth-miner01-0 8545:8545 & sleep 1"')

def forwarding_web3_miner02():
    print('⏩  Forwarding another miner node...')
    output = ''

    while output != b'Running':
        try:
            output = subprocess.check_output('vagrant ssh -c "kubectl get pod geth-miner02-0 -o jsonpath=\'{.status.phase}\'"', shell=True)
        except subprocess.CalledProcessError:
            output = ''
        time.sleep(1)

    os.system('vagrant ssh -c "nohup kubectl port-forward --address 0.0.0.0 geth-miner02-0 8546:8545 & sleep 1"')

def forwarding_monitor():
    print('⏩  Forwarding monitor node...')
    output = ''

    while output != b'Running':
        try:
            output = subprocess.check_output('vagrant ssh -c "kubectl get pod monitor-0 -o jsonpath=\'{.status.phase}\'"', shell=True)
        except subprocess.CalledProcessError:
            output = ''
        time.sleep(1)

    os.system('vagrant ssh -c "nohup kubectl port-forward --address 0.0.0.0 monitor-0 3001:3001 & sleep 1"')

def forwarding_explorer():
    print('⏩  Forwarding explorer node...')
    output = ''

    while output != b'Running':
        try:
            output = subprocess.check_output('vagrant ssh -c "kubectl get pod explorer-0 -o jsonpath=\'{.status.phase}\'"', shell=True)
        except subprocess.CalledProcessError:
            output = ''
        time.sleep(1)

    os.system('vagrant ssh -c "nohup kubectl port-forward --address 0.0.0.0 explorer-0 3000:3000 & sleep 1"')

def restart_explorer():
    os.system('vagrant ssh -c "kubectl exec -it explorer-0 -- /sbin/killall5 &> /dev/null"')
    print('🔄  Restarting explorer node...')

def truffle_migrate():
    os.system('vagrant ssh -c "cd /home/vagrant/ethereum-adi/backend/ && sudo truffle migrate"')

if __name__ == '__main__':
    vagrant_up()
    forwarding_web3_miner01()
    forwarding_web3_miner02()
    forwarding_monitor()
    forwarding_explorer()
    restart_explorer()
    forwarding_explorer()
    truffle_migrate()

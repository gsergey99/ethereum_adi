#!/usr/bin/python3
import argparse
import os
import json
import sys
import yaml

from eth_account import Account
from datetime import datetime

def generate_account():
    acct = Account.create()
    eth_addr = acct.address
    eth_key = acct.key

    print('💰  Generated eth account:')
    print(f'🏘️   Eth addr: {eth_addr}')
    print(f'🔑  Eth key: {eth_key}')

    json_encrypt = Account.encrypt(eth_key, '123')

    file_name =  f'UTC--{datetime.utcnow().isoformat()}000Z-e-{eth_addr[2:]}'
    file_name = file_name.replace(':', '-')
    path_file_name = f'keystore/{file_name}'

    with open(path_file_name, 'w', encoding='utf-8') as f:
        json.dump(json_encrypt, f, ensure_ascii=False, indent=4)
        f.write('\n')

    with open('environment.yaml', 'r') as f:
        data_loaded = yaml.safe_load(f)

    n = len(data_loaded['nodes']) + 1
    node_name = f'miner0{n}'
    node_info = [ {node_name: {'k8s': {'replicas': 1},
                'geth': {'storage_size': 20,
                        'Eth_Etherbase': f'{eth_addr}',
                        'Eth_Password': '123',
                        'Node_UserIdent': node_name,
                        'Node_DataDir': f'/etc/testnet/{node_name}',
                        'Node_HTTPPort': 8545,
                        'Node_WSPort': 8546,
                        'NodeP2P_DiscoveryAddr': 30303,
                        'Dashboard_Port': 8080,
                        'Dashboard_Refresh': 3000000000 } } } ]
    node_list = data_loaded['nodes']
    data_loaded['nodes'] = node_list + node_info

    data_loaded['keystore']['items'][eth_addr] = file_name

    with open('environment.yaml', 'w') as f:
        yaml.dump(data_loaded, f)

def degenerate_account():
    with open('environment.yaml', 'r') as f:
        data_loaded = yaml.safe_load(f)

    # Number of nodes
    n = len(data_loaded['nodes'])
    if n <= 2:
        print('🚯  Must be at least two nodes in the network!')
        print('ℹ️   The network is configured with 3 sealers, so there must be N/2 + 1 nodes!')
        return -1

    node_to_remove = data_loaded['nodes'][-1:][0]

    # Remove node info
    node_list = data_loaded['nodes']
    data_loaded['nodes'] = node_list[:-1]

    # Remove key_file to keystore
    key_filename = data_loaded['keystore']['items'][node_to_remove[list(node_to_remove.keys())[0]]['geth']['Eth_Etherbase']]
    os.system(f'rm keystore/{key_filename}')
    del data_loaded['keystore']['items'][node_to_remove[list(node_to_remove.keys())[0]]['geth']['Eth_Etherbase']]

    with open('environment.yaml', 'w') as f:
        yaml.dump(data_loaded, f)

    return n

def add_node():
    generate_account()
    
    os.system('./blockchainit')
    os.system('kubectl apply -f yaml/ > /dev/null')
    
    print('🚀  Successful added new node!')

def del_node():
    n = degenerate_account()
    
    if n != -1:
        print('🚮  Deleting new node...')
        os.system(f'kubectl delete sts geth-miner0{n} > /dev/null')
        os.system(f'kubectl delete svc miner0{n}-svc > /dev/null')
        os.system(f'kubectl delete pvc volume-miner0{n} > /dev/null')
        os.system(f'rm miner0{n}.toml')
        os.system('./blockchainit')
        os.system('kubectl apply -f yaml/ > /dev/null')

        print('🗑️   Successful deleted new node!')

def start_cluster():
    os.system('minikube start --cpus=6 --memory=12288 --kubernetes-version=v1.14.2')
    os.system('./blockchainit')
    os.system('kubectl apply -f yaml/ > /dev/null')
    os.system('watch -n 1 kubectl get po,svc,pv,pvc,statefulset,deployment -o wide')

def del_cluster():
    os.system('minikube delete')

def view_cluster():
    os.system('watch -n 1 kubectl get po,svc,pv,pvc,statefulset,deployment -o wide')

def forwarding_web3():
    print('⏩  Forwarding one miner node...')
    os.system('kubectl port-forward geth-miner01-0 8545:8545')

def forwarding_monitor():
    print('⏩  Forwarding monitor node...')
    os.system('kubectl port-forward monitor-0 3001:3001')

def forwarding_explorer():
    print('⏩  Forwarding explorer node...')
    os.system('kubectl port-forward explorer-0 3000:3000')

def restart_explorer():
    os.system('kubectl exec -it explorer-0 -- /sbin/killall5')
    print('🔄  Restarting explorer node...')

def main():
    parser = argparse.ArgumentParser(description='clustETHr. All you need to manage your Ethereum kubernetes cluster.')
    parser.add_argument('-a', '--add', action='store_true', help='Add a new node')
    parser.add_argument('-r', '--remove', action='store_true', help='Remove a node')
    parser.add_argument('-s', '--start', action='store_true', help='Start the cluster')
    parser.add_argument('-d', '--delete', action='store_true', help='Delete the cluster from your system')
    parser.add_argument('-v', '--view', action='store_true', help='Visualize stats from your cluster')
    parser.add_argument('-fw3', '--forwarding-web3', action='store_true', help='Forwarding and expose one web3 endpoint')
    parser.add_argument('-fm', '--forwarding-monitor', action='store_true', help='Forwarding for monitor node')
    parser.add_argument('-fe', '--forwarding-explorer', action='store_true', help='Forwarding for explorer node')
    parser.add_argument('-re', '--restart-explorer', action='store_true', help='Restart explorer node')

    args = parser.parse_args()

    args = vars(parser.parse_args())

    if args['add']:
        add_node()
    elif args['remove']:
        del_node()
    elif args['start']:
        start_cluster()
    elif args['delete']:
        del_cluster()
    elif args['view']:
        view_cluster()
    elif args['forwarding_web3']:
        forwarding_web3()
    elif args['forwarding_monitor']:
        forwarding_monitor()
    elif args['forwarding_explorer']:
        forwarding_explorer()
    elif args['restart_explorer']:
        restart_explorer()
    else:
        parser.print_help()

if __name__ == '__main__':
    main()

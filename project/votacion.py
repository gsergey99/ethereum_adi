import fire
import sys
import json

from web3 import Web3, HTTPProvider



class Votacion:
    
    def  __init__ (self, Contract, w3, owner):
        
        self.w3 = w3
        self.owner = owner
        self.Contract = Contract

   
    def add_lista(self):
        
        n_votaciones = self.Contract.functions.push(1).transact({'from':self.owner})  
        print("Number of votations {}".format(n_votaciones))
        return self.w3.eth.getTransactionReceipt(n_votaciones)

    def get_lista(self):
        
        n_votaciones = self.Contract.functions.get().call()
        print(n_votaciones)

"""
  def cerrar_lista(self, id_votacion):
	if votacion_no_existe:
		return 'Esa votación no existe'
	if lista_ya_cerrada:
		return 'La lista ya está cerrada'
  	if lista_candidatos_vacia:
		return 'Una votación debe tener candidatos'
    return 'Lista cerrada correctamente'

  def cerrar_votacion(self, id_votacion):
	if votacion_no_existe:
		return 'Esa votación no existe'
	if votacion_ya_cerrada:
		return 'La votación ya está cerrada'
    return 'Votacion cerrada correctamente'

  def aniadir_candidato(self, id_votacion, candidato):
	if votacion_no_existe:
		return 'Esa votación no existe'
	if candidato_ya_añadido:
		return 'Ese candidato ya existe'
    return 'Añadido correctamente'

  def votar(self, id_votacion, voto):
	if votacion_no_existe:
		return 'Esa votación no existe'
	if ya_has_votado:
		return 'Esa votación no existe'
    return 'Pos ya has votao'

  def listar_candidatos(self, id_votacion):
	if votacion_no_existe:
		return 'Esa votación no existe'
	if lista_abierta:
		return 'La lista de candidatos sigue abierta'
    return 'Emiliano García Page dios supremo de CLM'

  def calcular_ganador(self, id_votacion):
	if votacion_no_existe:
		return 'Esa votación no existe'
	if votacion_no_terminada:
		return 'Esa votación todavía no ha terminado'
    return 'Ganador calculado'

  def ver_ganador(self, id_votacion):
  	if votacion_no_existe:
		return 'Esa votación no existe'
	if votacion_no_terminada:
		return 'Esa votación todavía no ha terminado'
    return 'Ha ganado Page'
"""

    

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
    
    def loadLast(self,src_file):
        '''
        Obtener la última conexión
        '''
        with open(src_file)
    
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
        Contract = w3.eth.contract(
            address=contractAddress,
            abi=self.loadABI('build/contracts/Votaciones.json')
        )
        owner = w3.eth.accounts[0]
       
        print(receipt)
        votacion = Votacion(Contract, w3, owner)
        votacion.add_lista()
        votacion.get_lista()
        #votacion.add_lista()
        #votacion.get_lista()
        #votacion.add_lista()
        #votacion.add_lista()
        #votacion.get_lista()

        return votacion 

if __name__ == "__main__":

    transaccion = Transaccion()
    sys.exit(transaccion.run())
    #Contract, w3, owner = transaccion.run()
    #sys.exit(fire.Fire(Votacion(Contract, w3, owner)))
    


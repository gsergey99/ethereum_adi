#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from votacion import Connection
import sys


def crearVotacion(votaciones):
    status = votaciones.create_votation()
    receipt = status[0]
    votation_id = status[1]

    print("Gas Used:", str(receipt['gasUsed']), "\n")
    print(f'Votación creada. (Id. votación: {votation_id})')

def addCandidato(votaciones, votation_id, candidate):
    status = votaciones.add_candidate(votation_id, candidate)
    receipt = status[0]

    print("Gas Used:", str(receipt['gasUsed']), "\n")
    print(f'Candidato "{candidate}" añadido. (Id. votación: {votation_id}) \n')

def cerrarLista(votaciones, votation_id):
    status = votaciones.close_list(votation_id)
    receipt = status[0]

    print("Gas Used:", str(receipt['gasUsed']), "\n")
    print(f'Lista de candidatos cerrada. (Id. votación: {votation_id}) \n')

def cerrarVotacion(votaciones, votation_id):
    status = votaciones.close_votation(votation_id)
    receipt = status[0]

    print("Gas Used:", str(receipt['gasUsed']), "\n")
    print(f'Votación cerrada. (Id. votación: {votation_id}) \n')

def consultarCandidatos(votaciones, votation_id):
    status = votaciones.list_candidates(votation_id)
    candidates = status[1]

    print(f'Candidatos (Id. votación: {votation_id}): ')
    for candidate in candidates:
        print(f'\t \t - {candidate} ')

def votarCandidato(votaciones, votation_id, candidate):
    status = votaciones.vote(votation_id, candidate)
    receipt = status[0]

    print("Gas Used:", str(receipt['gasUsed']), "\n")
    print(f'Candidato "{candidate}" votado. (Id. votación: {votation_id})')

def consultarGanador(votaciones, votation_id):
    status = votaciones.view_winner(votation_id)
    winner = status[1]

    print(f'Candidato "{winner}" ganador. (Id. votación: {votation_id})')

def consultarResultados(votaciones, votation_id):
    status = votaciones.list_results(votation_id)
    results = status[1]

    print(f'Resultados (Id. votación: {votation_id}): ')
    for result in results:
        print(f'\t \t - {result[0]} --- {result[1]} votos')

def input_range(min_value, max_value, msg):
    while True:
        try:
            value = int(input(msg))
        except ValueError:
            print('¡¡¡Error, no se ha introducido algún valor correcto!!!\n')

        if value < min_value or value > max_value:
            print('¡¡¡Error, el valor introducido no está detro del rango válido!!!\n')
        else:
            break

    return value

def input_int(msg):
    while True:
        try:
            value = int(input(msg))
            break
        except ValueError:
            print('¡¡¡Error, no se ha introducido algún valor correcto!!! \n')
    return value

FUNCTIONS = {
        1 : crearVotacion,
        2 : addCandidato,
        3 : cerrarLista,
        4 : cerrarVotacion,
        5 : consultarCandidatos,
        6 : votarCandidato,
        7 : consultarGanador,
        8 : consultarResultados
    }

REQUIERE_VOTACION = [2, 3, 4, 5, 6, 7, 8]
REQUIERE_CANDIDATO = [2, 6]

def main():
    connection = Connection()
    try:
        connection.connect()
    except Exception as ex:
        print(str(ex))
        sys.exit(1)
    
    print('Node connected')
    print('Blockchain size: %s' % connection.w3.eth.blockNumber)

    n_account = len(connection.w3.eth.accounts)
    account_index = input_range(0, n_account, f'-> Introduce el índice de la cuenta a usar [0 - {n_account}]: ')
    try:
        votaciones = connection.run(account_index)
    except Exception as ex:
        print('No contract address found!')
        sys.exit(1)

    while True:
        print('\n****** SISTEMA DE VOTACIONES ****** \n',
        '\n',
        '\t --- Gestionar votaciones --- \n',
        '\t 1. Crear votación \n',
        '\t 2. Añadir candidato a una votación \n',
        '\t 3. Cerrar lista de candidatos \n',
        '\t 4. Cerrar votación \n',
        '\n',
        '\t --- Participar en votaciones --- \n',
        '\t 5. Consultar candidatos\n',
        '\t 6. Votar candidato \n',
        '\t 7. Consultar ganador \n',
        '\t 8. Consultar resultados de los candidatos \n',
        '\n',
        '\t 0. Salir \n')

        opt = input_range(0, 8, '-> Introduce una opción: ')
        
        if opt == 0:
            print('\n ¡Buen día! \n')
            break
        
        args = [votaciones]

        if opt in REQUIERE_VOTACION:
            args.append(input_int('-> Introduce identificador de votación: '))
        
        if opt in REQUIERE_CANDIDATO:
            args.append(input("-> Introduce candidato: "))

        try:
            FUNCTIONS[opt](*args)
        except Exception as e:
            error = str(e)
            print(error[70:])

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print('\n ¡Buen día! \n')
        sys.exit(0)


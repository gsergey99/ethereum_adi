#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
from votacion import Connection

INVALID_ID = 1234

CUENTA_1 = 0
CUENTA_2 = 1

CANDIDATO = 'Pepe'
INVALID_CANDIDATO = "Pepa"

CONNECTION_1 = Connection()
CONNECTION_1.connect()
VOTATION_1 = CONNECTION_1.run(CUENTA_1)

CONNECTION_2 = Connection()
CONNECTION_2.connect()
VOTATION_2 = CONNECTION_2.run(CUENTA_2)


class Tests(unittest.TestCase):
    
    def test_crear_votacion(self):
        '''
        Crear una votación correctamente
        '''
        result = VOTATION_1.create_votation()
        self.assertIsNotNone(result[0]) 
    
    def test_add_candidato(self):
        '''
        Añadir un candidato correctamente a la lista de candidatos
        '''
        id_votation = VOTATION_1.create_votation()[1]
        result = VOTATION_1.add_candidate(id_votation, CANDIDATO)
        
        self.assertEqual(result[0]['status'], 1)
    
    def test_add_candidato_votacion_no_existe(self):
        '''
        Añadir un candidato a una votación no existente
        '''
        with self.assertRaises(Exception):
            VOTATION_1.add_candidate(INVALID_ID, CANDIDATO)
   
    def test_usuario_cerrar_votacion(self):
        '''
        Solo el propietario de la votación podrá cerrar la votación
        '''
        id_votation = VOTATION_1.create_votation()[1]
        VOTATION_1.add_candidate(id_votation, CANDIDATO)
        VOTATION_1.close_list(id_votation)

        with self.assertRaises(Exception):
            VOTATION_2.close_votation(id_votation)

    def test_add_candidato_ya_en_lista(self):
        '''
        Añadir un candidato ya existente a la lista de candidatos
        '''
        id_votation = VOTATION_1.create_votation()[1]
        VOTATION_1.add_candidate(id_votation, CANDIDATO)
        
        with self.assertRaises(Exception):
            VOTATION_1.add_candidate(id_votation, CANDIDATO)
   
    def test_cerrar_lista(self):
        '''
        Cerrar una lista de candidatos correctamente
        '''
        id_votation = VOTATION_1.create_votation()[1]
        VOTATION_1.add_candidate(id_votation, CANDIDATO)
        result = VOTATION_1.close_list(id_votation)
        
        self.assertEqual(result[0]['status'], 1)

    def test_cerrar_lista_votacion_no_existe(self):
        '''
        Cerrar una lista de candidatos a una votación que no existe
        '''
        with self.assertRaises(Exception):  
            VOTATION_1.close_list(INVALID_ID, CANDIDATO)
    
    def test_cerrar_lista_propietario(self):
        '''
        Solo el propietario de la votación puede cerrar la lista de candidatos
        '''
        id_votation = VOTATION_1.create_votation()[1]
        VOTATION_1.add_candidate(id_votation, CANDIDATO)
        
        with self.assertRaises(Exception):
            VOTATION_2.close_list(id_votation)

    def test_cerrar_votacion(self):
        '''
        Cerrar una votación correctamente
        '''
        id_votation = VOTATION_1.create_votation()[1]
        VOTATION_1.add_candidate(id_votation, CANDIDATO)
        VOTATION_1.close_list(id_votation)
        result = VOTATION_1.close_votation(id_votation)
        
        self.assertEqual(result[0]['status'], 1)
    
    def test_cerrar_votacion_no_existe(self):
        '''
        Cerrar una votación que no existe
        '''    
        with self.assertRaises(Exception):
            VOTATION_1.close_votation(INVALID_ID)
	
    def test_votar(self):
        '''
        Votar correctamente
        '''
        id_votation = VOTATION_1.create_votation()[1]
        VOTATION_1.add_candidate(id_votation, CANDIDATO)
        VOTATION_1.close_list(id_votation)
        result = VOTATION_1.vote(id_votation, CANDIDATO)
        
        self.assertEqual(result[0]['status'], 1)
    
    def test_votar_varias_veces(self):
        '''
        Un usuario vota dos veces al mismo candidato
        '''
        id_votation = VOTATION_1.create_votation()[1]
        VOTATION_1.add_candidate(id_votation, CANDIDATO)
        VOTATION_1.close_list(id_votation)
        VOTATION_1.vote(id_votation, CANDIDATO)

        with self.assertRaises(Exception):
            VOTATION_1.vote(id_votation, CANDIDATO)

    def test_votar_candidato_no_existe(self):
        '''
        Votar a un candidato que no existe en la lista de candidatos
        '''
        id_votation = VOTATION_1.create_votation()[1]
        VOTATION_1.add_candidate(id_votation, CANDIDATO)
        VOTATION_1.close_list(id_votation)

        with self.assertRaises(Exception):
            VOTATION_1.vote(id_votation, INVALID_CANDIDATO)

    def test_get_candidatos_votacion_no_existe(self):
        '''
        Obtener candidatos de una votación que no existe
        '''
        with self.assertRaises(Exception):
            VOTATION_1.get_candidates(INVALID_ID)

    def test_get_resultado(self):
        '''
        Obtener resultados de una votación correctamente 
        '''
        id_votation = VOTATION_1.create_votation()[1]
        VOTATION_1.add_candidate(id_votation, CANDIDATO)
        VOTATION_1.close_list(id_votation)
        VOTATION_1.vote(id_votation, CANDIDATO)
        VOTATION_1.close_votation(id_votation)
        result = VOTATION_1.view_winner(id_votation)
        
        self.assertEqual(result[1], CANDIDATO)
    
    def test_resultados_votacion_abierta(self):
        '''
        Obtener resultados en una votacion abierta
        ''' 
        id_votation = VOTATION_1.create_votation()[1]
        VOTATION_1.add_candidate(id_votation, CANDIDATO)
        VOTATION_1.close_list(id_votation)
        VOTATION_1.vote(id_votation, CANDIDATO)

        with self.assertRaises(Exception):
            VOTATION_1.view_winner(id_votation)

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
from votacion import Conection 
from web3 import Web3, HTTPProvider, exceptions

CANDIDATO = 'Pepe'

class Tests(unittest.TestCase):
    
    def test_crear_votacion(self):
        '''
        Crear una votación correctamente
        '''
        conection = Conection()
        votation = conection.run()
        id_votation = votation.create_votation()
        self.assertIsNotNone(id_votation) 
    
    def test_add_candidato(self):
        '''
        Añadir un candidato correctamente
        '''
        conection = Conection()
        votation = conection.run()
        id_votation = votation.create_votation()
        args = [id_votation, CANDIDATO]
        result = votation.add_candidate(*args)
        self.assertEquals(result, 1)
    
    def test_add_candidato_votacion_no_existe(self):
        '''
        Añadir un candidato a una votación no existente
        '''
        conection = Conection()
        votation = conection.run()
        with self.assertRaises(Exception):
            args = [1234, CANDIDATO]
            votation.add_candidate(*args)
    
    def test_add_candidato_ya_en_lista(self):
        '''
        Añadir un candidato existente
        '''
        conection = Conection()
        votation = conection.run()
        id_votation = votation.create_votation()
        args = [id_votation, CANDIDATO]
        votation.add_candidate(*args)
        with self.assertRaises(Exception):
            votation.add_candidate(*args)
   
    def test_cerrar_lista(self):
        '''
        Cerrar una lista correctamente
        '''
        conection = Conection()
        votation = conection.run()
        id_votation = votation.create_votation()
        args = [id_votation, CANDIDATO]
        votation.add_candidate(*args)
        result = votation.close_list(*args)
        self.assertEquals(result, 1)

    def test_cerrar_lista_votacion_no_existe(self):
        '''
        Cerrar una lista de candidatos a una votación que no existe
        '''
        conection = Conection()
        votation = conection.run()
        with self.assertRaises(Exception):
            args = [1234, CANDIDATO]
            votation.close_list(*args)
	
    def test_cerrar_votacion(self):
        '''
        Cerrar una votación correctamente
        '''
        conection = Conection()
        votation = conection.run()
        id_votation = votation.create_votation()
        args_1 = [id_votation, CANDIDATO]
        votation.add_candidate(*args_1)
        args_2 = [id_votation]
        votation.close_list(*args_2)
        result = votation.close_votation(*args_2)
        self.assertEquals(result, 1)
    
    def test_cerrar_votacion_que_no_existe(self):
        '''
        Cerrar una votación que no existe
        '''
        conection = Conection()
        votation = conection.run()
        
        with self.assertRaises(Exception):
            args = [1234]
            votation.close_votation(*args)
	
    def test_votar(self):
        '''
        Crear un voto correctamente
        '''
        conection = Conection()
        votation = conection.run()
        id_votation = votation.create_votation()
        args_1 = [id_votation, CANDIDATO]
        votation.add_candidate(*args_1)
        args_2 = [id_votation]
        votation.close_list(*args_2)
        result = votation.vote(*args_1)
        self.assertEquals(result, 1)

    def test_votar_candidato_no_existe(self):
        '''
        Votar a un candidato que no existe
        '''
        conection = Conection()
        votation = conection.run()
        id_votation = votation.create_votation()
        args_1 = [id_votation, CANDIDATO] 
        args_2 = [id_votation]
        votation.add_candidate(*args_1)
        votation.close_list(*args_2)
        with self.assertRaises(Exception):
            votaciones.vote(*args_1)

    

    def test_get_candidatos_votacion_no_existe(self):
        '''
        Obtener candidatos de una votación que no existe
        '''
        conection = Conection()
        votation = conection.run()
        with self.assertRaises(Exception):
            args = [1234]
            votation.get_candidates(*args)

    def test_get_resultado(self):
        '''
        Obtener resultados de una votación correctamente 
        '''
        conection = Conection()
        votation = conection.run()
        id_votation = votation.create_votation()
        args_1 = [id_votation, CANDIDATO]
        votation.add_candidate(*args_1)
        args_2 = [id_votation]
        votation.close_list(*args_2)
        votation.vote(*args_1)
        votation.close_votation(*args_2)
        result = votation.view_winner(*args_2)
        self.assertEquals(result, "Pepe")


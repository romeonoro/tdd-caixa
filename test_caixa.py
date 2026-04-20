
from unittest import TestCase
from caixa import Caixa

class TestTroco(TestCase): 

    def test_nao_deve_dar_troco_para_valor_exato(self):
        caixa = Caixa()
        troco = caixa.pagar(10, {10: 1})
        self.assertEqual({}, troco)

    def test_deve_dar_troco_em_uma_cedula(self): 
        caixa = Caixa(disponivel = {5: 1})
        troco = caixa.pagar(5, {10: 1})
        self.assertEqual({5: 1}, troco)

    def test_deve_atualizar_caixa_ao_pagar(self): 
        caixa = Caixa(disponivel = {5: 1})
        caixa.pagar(5, {5: 1})
        self.assertEqual({5: 2}, caixa.disponivel)
        caixa.pagar(5, {10: 1})
        self.assertEqual({10: 1, 5: 1}, caixa.disponivel)


    def test_nao_deve_dar_troco_sem_dinheiro_disponivel(self): 
        caixa = Caixa()
        with self.assertRaises(Exception) as context:
            caixa.pagar(5, {10: 1})
        self.assertTrue("Não há dinheiro disponível para dar troco" in str(context.exception))

    def test_nao_deve_aceitar_pagamento_menor_que_valor(self):
        caixa = Caixa({5:1,2:1})
        with self.assertRaises(Exception) as context:
            caixa.pagar(5, {2: 1})
        self.assertTrue("Valor do pagamento deve ser igual ou maior que o valor devido" in str(context.exception))

    def test_nao_deve_dar_troco_quando_caixa_nao_tem_dinheiro_para_troco(self):
        caixa = Caixa(disponivel = {50: 1, 10: 3, 5: 2, 0.5: 5, 0.25: 3})
        with self.assertRaises(Exception) as context:
            caixa.pagar(37.8, {50: 1}) 
        self.assertTrue("Não há dinheiro disponível para dar troco" in str(context.exception))

    def test_nao_deve_aceitar_pagamento_com_valor_negativo(self):
        caixa = Caixa(disponivel = {5: 1})
        with self.assertRaises(Exception) as context:
            caixa.pagar(5, {10: -1})
        self.assertTrue("Valor do pagamento não pode ser negativo" in str(context.exception))

    def test_nao_deve_aceitar_pagamento_com_cedula_invalida(self):
        caixa = Caixa(disponivel = {5: 1})
        with self.assertRaises(Exception) as context:
            caixa.pagar(5, {12: 1})
        self.assertTrue("Valor do pagamento deve ter cédulas válidas" in str(context.exception))

    def test_nao_deve_aceitar_caixa_negativo(self):
        with self.assertRaises(Exception) as context:
            Caixa(disponivel = {5: -1})
        self.assertTrue("Valor de caixa não pode ser negativo" in str(context.exception))

    def test_nao_deve_aceitar_notas_invalidas(self):
        with self.assertRaises(Exception) as context:
            Caixa(disponivel = {2.5: 1})
        self.assertTrue("Valor de caixa deve ter cédulas válidas" in str(context.exception))
        with self.assertRaises(Exception) as context:
            Caixa(disponivel = {-3: 1})
        self.assertTrue("Valor de caixa deve ter cédulas válidas" in str(context.exception))

    def test_deve_retornar_troco_com_varias_cedulas(self):
        caixa = Caixa(disponivel = {10: 3, 2: 3, 0.1: 5})
        troco = caixa.pagar(37.8, {50: 1}) 
        self.assertEqual({10: 1, 2: 1, 0.1: 2}, troco)

    def test_deve_atualizar_caixa_com_varias_cedulas(self):
        caixa = Caixa(disponivel = {10: 3, 2: 3, 0.1: 5})
        caixa.pagar(37.8, {50: 1}) 
        self.assertEqual({50: 1, 10: 2, 2: 2, 0.1: 3}, caixa.disponivel)

    def test_deve_revisar_caixa(self):
        caixa = Caixa(disponivel = {10:2})
        caixa.atualizar({2:3, 5:3})
        self.assertEqual({10: 2, 2: 3, 5: 3}, caixa.disponivel)
        caixa.atualizar({0.25: 5, 20: 3})
        self.assertEqual({20: 3, 10: 2, 5: 3, 2: 3, 0.25: 5}, caixa.disponivel)

    def test_deve_retornar_troco_com_menor_numero_de_cedulas_possivel(self):
        caixa = Caixa(disponivel = { 0.1: 5, 2: 6, 5: 3, 10: 3})
        troco = caixa.pagar(38, {50: 1}) 
        self.assertEqual({10: 1, 2: 1}, troco)

    
    
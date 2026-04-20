
class Caixa:
    
    _CEDULAS_VALIDAS = [200, 100, 50, 20, 10, 5, 2, 1, 0.5, 0.25, 0.1, 0.05, 0.01]

    def __init__(self, disponivel: dict[float: int] = None):
        self._valida_cedulas(disponivel, "Valor de caixa") if disponivel else None
        self._disponivel ={v: q for v, q in sorted(disponivel.items(), reverse=True)} if disponivel else {}

    @property
    def disponivel(self):
        return self._disponivel

    def pagar(self, valor, pagamento):
        self._valida_cedulas(pagamento, "Valor do pagamento")
        valor_pago = sum([valor * quantidade for valor, quantidade in pagamento.items()])
        if valor_pago == valor:
            self._disponivel = self._atualizar_caixa(self._disponivel, pagamento, {})
            return {}
        if not self._disponivel:
            raise Exception("Não há dinheiro disponível para dar troco")
        if valor_pago < 0:
            raise Exception("Valor do pagamento deve ser positivo")
        valor_troco = round(valor_pago - valor, 2)
        if (valor_troco < 0):
            raise Exception("Valor do pagamento deve ser igual ou maior que o valor devido")
        troco = self._retornar_troco(valor_troco)
        self._disponivel = self._atualizar_caixa(self._disponivel, pagamento, troco)
        return troco

    def _valida_cedulas(self, pagamento: dict[float: int], identificador: str):
        for valor, quantidade in pagamento.items():
            self._validar_valores(valor, quantidade, identificador)


    def _retornar_troco(self, valor_troco): 
        troco = {}
        for valor, quantidade in self._disponivel.items():
            while valor_troco >= valor and quantidade > 0:
                if valor in troco:
                    troco[valor] += 1
                else:
                    troco[valor] = 1
                valor_troco = round(valor_troco -valor, 2)
                quantidade -= 1
        if valor_troco > 0:
            raise Exception("Não há dinheiro disponível para dar troco")  
        return troco
    
    def _atualizar_caixa(self, caixa_atual, pagamento, troco_calculado):
        if not caixa_atual: 
            caixa_atual = {}
        for valor, quantidade in troco_calculado.items():
            caixa_atual[valor] -= quantidade
            if (caixa_atual[valor] == 0):
                del caixa_atual[valor]
        for valor, quantidade in pagamento.items():
            if valor in caixa_atual:
                caixa_atual[valor] += quantidade
            else:
                caixa_atual[valor] = quantidade
        return caixa_atual
    
    def atualizar(self, revisao):
        if not self._disponivel:
            self._disponivel = {}
        if not revisao:
            return
        valores_revisao = {v:q for v, q in sorted(revisao.items(), reverse=True)}
        for valor, quantidade in valores_revisao.items():
            self._validar_valores(valor, quantidade, "Valor de caixa")
            if valor in self._disponivel:
                self._disponivel[valor] += quantidade
            else:
                self._disponivel[valor] = quantidade

    def _validar_valores(self, valor: float, quantidade: int, identificador: str):
        if valor not in Caixa._CEDULAS_VALIDAS:
            raise Exception(f"{identificador} deve ter cédulas válidas")
        if quantidade < 0:
            raise Exception(f"{identificador} não pode ser negativo")
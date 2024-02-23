from abc import ABC, abstractclassmethod, abstractproperty
from datetime import datetime
import textwrap


class Cliente:

    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta):
        transacao.realzar(conta)

    def add_contas(self, conta):
        self.contas.append(conta)


class PessoaFisica(Cliente):
    def __init__(self, cpf, nome, data_nascimento, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.cpf = cpf
        self.data_nasciemento = data_nascimento


class Conta:
    def __initi__(self, saldo, numero, agencia, cliente, historico):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, numero, cliente):
        return cls(numero, cliente)

    @property
    def saldo(self):
        return self._saldo
    
    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico
    
    

    def sacar(self, valor):
        saldo = self.saldo

        if valor > saldo:
            print("\nOperação não realizada!\nSaldo insuficiente!")

        elif valor > 0:
            self._saldo -= valor
            print("\nSaque realizado com sucesso!\nAguarde a contagem das cedulas!")
            return True

        else:
            print("\nOperação invalida!\nTente novamente")
        return False

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print("\nDepósito realizado com sucesso!")
            return True
        else:
            print("\nOperação invalida!\nTente novamente")
            return False 

        return True

class ContaCorrente(Conta):
    def __init__(self, cliente, numero, limite = 500 ,lim_saque = 3):
        super().__init__(cliente, numero)
        self.limite = limite
        self.lim_saque = lim_saque

    def sacar(self, valor):
        num_saques = len([transacao for transacao in self.historico.transacoes if transacao ["Tipo"] == Saque.__name__])

        lim_excedido = valor > self.limite
        QtdSaque_excedido = valor > self.lim_saque

        if lim_excedido: 
            print("\nOperação não realizada!\nValor diario disponível excedido")

        elif QtdSaque_excedido:
            print("\nOperação não realizada!\nQuantidade de saques diario excedido")

        else:
            return super().sacar(valor)

    def __str__(self):
        return f"""\
            Agência:\t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.cliente.nome}
        """

class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return slef._transacoes

    def add_transacao(self, transacao):
        self._transacoes.append({
            "Tipo": transacao.__class__.__name__,
            "Valor": transacao.valor,
            "Data": data.strftime('%d-%m-%Y %H:%m:%s')
        })


class Transacao(ABC):
    @property
    @abstractproperty
    def valor(self):
        pass

    @abstractclassmethod
    def resgistrar(self):
        pass

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        transacao_realizada = conta.sacar(self.valor)

        if transacao_realizada:
            conta.historico.add_transacao(self)

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        transacao_realizada = conta.depositar(self.valor)

        if transacao_realizada:
            conta.historico.add_transacao(self)

def menu():
    menu = """\n
    ==========Inicio==========
    [1] - Depósito
    [2] - Saque
    [3] - Extrato
    [4] - Criar nova conta 
    [5] - Criar novo cliente
    [6] - Listar contas 
    [7] - Sair
    ==========================
    ==>"""
    return input(textwrap.dedent(menu))

def filtrar_cliente(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliete.cpf==cpf]
    return clientes_filtrados[0] if clientes_filtrados else None

def recuperar_conta(cliente):
    if not cliente.contas:
        print("Cliente não encontrado")
        return
    
    return cliente.contas[0]
    

def deposito(clientes):
    cpf = input("Informe o CPF do cliente")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente.contas:
        print("Cliente não encontrado")
        return

    valor = float(input("Informe o valor do deposito"))
    transacao = Deposito(valor)

    conta = recuperar_conta(cliente)
    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)
    

def saque(clientes):
    cpf = input("Informe o CPF do cliente")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente.contas:
        print("Cliente não encontrado")
        return

    valor = float(input("Informe o valor do deposito"))
    transacao = Saque(valor)

    conta = recuperar_conta(cliente)
    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)
    

def exibir_extrato(clientes):
    cpf = input("Informe o CPF do cliente")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente.contas:
        print("Cliente não encontrado")
        return

    print("==========EXTRATO=========")
    transacoes = conta.historico.transacoes
    extrato = " "
    if not transacoes:
        extrato = "Não foram realziadas transações"
    else:
        for transacao in transacoes:
            extrato += f"\n{transacao['tipo']}: \n\tR$ {transacao['valor']:.2f} "

    print(extrato)
    print(f'\nSaldo:\n\tR$ {conta.saldo:.2f}')
    print("============================")
    

def criar_cliente(clientes):
    cpf = input("Informe o CPF do cliente")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente.contas:
        print("Cliente não encontrado")
        return

    nome = input("Informe o nome do cliente")
    data_nasciemento = input("informe a data de nascimento do cliente")
    endereco = input("Informe a data de nascimento do cliente")

    cliente = PessoaFisica(cpf, nome, data_nascimento, endereco)

    clientes.append(cliente)

    print("========= CLIENTE CRIADO COM SUCESSO ==========")



def criar_conta(num_conta, clientes, contas):
    cpf = input("Informe o seu CPF")
    cliente = filtrar_cliente(cpf, cliente)
     
    if not cliente:
        print("Cliente não encontrado, criação de conta encerrada")
        return
    
    conta = ContaCorrente.nova_conta(cliente=cliente, numero = num_conta)
    contas.append(conta)
    cliente.contas.append(conta)

def list_conta(contas):
    for conta in contas:
        print(textwrap.dedent(cont))

def main():
    clientes = []
    contas = []
    
    while True:
        op = menu()
        op = int(op)
        

        if op == 1:
            deposito(clientes)
        
        elif op == 2:
            saque(clientes)
            
            
        elif op == 3:
           exibir_extrato(clientes)


        elif op == 4:
            criar_cliente(clientes)


        elif op == 5:
            num_conta = len(contas) + 1
            criar_conta(num_conta, clientes, contas)
        
        elif op == 6:
            list_conta(contas)


        elif op == 7:
            break

        else:
            print("Operação inválida.\nTente novamente.")

main()
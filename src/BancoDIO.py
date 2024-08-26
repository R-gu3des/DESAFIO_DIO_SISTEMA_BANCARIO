from datetime import datetime
from time import sleep
import pandas as pd
import os

class BancoDIO:
    def __init__(self, nome_banco: str, valor_limite_saque: int) -> None:
        self.__nome_banco = nome_banco
        self.__limite_saques = 3
        self.__saldo = 0
        self.__valor_limite_saque = valor_limite_saque
        self.__caminho_arquivo = 'data/historico.csv'
        self.carregar_dados()

    @property
    def nome_banco(self):
        return self.__nome_banco

    @nome_banco.setter
    def nome_banco(self, nome_banco: str):
        self.__nome_banco = nome_banco

    @property
    def limite_saques(self):
        return self.__limite_saques

    @limite_saques.setter
    def limite_saques(self, limite_saque: int):
        self.__limite_saques = limite_saque

    @property
    def saldo(self):
        return self.__saldo

    @saldo.setter
    def saldo(self, saldo: float):
        self.__saldo = saldo

    @property
    def valor_limite_saque(self):
        return self.__valor_limite_saque

    @valor_limite_saque.setter
    def valor_limite_saque(self, valor_limite_saque: int):
        self.__valor_limite_saque = valor_limite_saque

    @property
    def caminho_arquivo(self):
        return self.__caminho_arquivo

    def carregar_dados(self):
        if os.path.exists(self.caminho_arquivo):
            df = pd.read_csv(self.caminho_arquivo)
            if 'Saldo Atual' in df.columns:
                self.saldo = df['Saldo Atual'].iloc[-1]  # Atualiza o saldo com o último valor

    def deposito(self):
        while True:
            valor_str = input("Digite um valor para depósito: ")

            # Verifica se o valor é um número positivo
            if valor_str.replace('.', '', 1).isdigit():
                valor = float(valor_str)
                if valor <= 0:
                    print(f"\033[91mO valor de depósito deve ser positivo.\033[0m")
                else:
                    self.saldo += valor
                    print(f"\033[92mDepósito realizado com sucesso!\033[0m")
                    self.informacao_transacao('Depósito', {'Valor Depositado': valor})
                    break
            else:
                print(f"\033[91mNão foi possível realizar o depósito. Verifique o valor digitado.\033[0m")
        sleep(6)

    def verificar_saques_diarios(self):
        hoje = datetime.now().date()
        if os.path.exists(self.caminho_arquivo):
            df = pd.read_csv(self.caminho_arquivo)
            if 'Dia da Transação' in df.columns and 'Tipo de Operação' in df.columns:
                df['Dia da Transação'] = pd.to_datetime(df['Dia da Transação']).dt.date
                saques_hoje = df[(df['Dia da Transação'] == hoje) & (df['Tipo de Operação'] == 'Saque')]
                return len(saques_hoje)
        return 0

    def saque(self):
        saques_hoje = self.verificar_saques_diarios()
        if saques_hoje >= 3:
            print(f"\033[91mLimite diário de saques atingido!\033[0m")
            return

        valor_str = input("Digite um valor para saque: ")

        # Verifica se o valor é um número positivo
        if valor_str.replace('.', '', 1).isdigit():
            valor = float(valor_str)
            if valor <= 0:
                print(f"\033[91mO valor de saque deve ser positivo.\033[0m")
            elif valor > self.saldo:
                print(f"\033[91mSaldo insuficiente para saque! Saldo atual: {self.saldo:.2f}\033[0m")
            elif valor > self.valor_limite_saque:
                print(f"\033[91mValor do saque excede o limite permitido! Limite de saque: {self.valor_limite_saque:.2f}\033[0m")
            else:
                self.saldo -= valor
                self.limite_saques -= 1
                self.informacao_transacao('Saque', {'Valor Sacado': valor})
                print(f"\033[92mSaque realizado com sucesso!\033[0m")

        else:
            print(f"\033[91mPor favor, insira um valor numérico válido.\033[0m")
            
        sleep(6)

    def informacao_transacao(self, transacao=None, dicionario=None):
        # Certifique-se de que o diretório existe
        caminho_diretorio = 'data'
        if not os.path.exists(caminho_diretorio):
            os.makedirs(caminho_diretorio)
        
        # Crie um DataFrame com as informações da transação
        dados = {
            'Nome do Banco': [self.nome_banco],
            'Dia da Transação': [datetime.now()],
            'Tipo de Operação': [transacao],
            'Saldo Atual': [self.saldo]
        }
        
        # Adicione os dados do dicionário ao DataFrame
        for chave, valor in dicionario.items():
            dados[chave.capitalize()] = [valor]

        df = pd.DataFrame(dados)

        # Salve o DataFrame como um arquivo CSV
        df.to_csv(self.caminho_arquivo, mode='a', header=not os.path.exists(self.caminho_arquivo), index=False)

    def historico_transacao(self):
        if os.path.exists(self.caminho_arquivo):
            df = pd.read_csv(self.caminho_arquivo)
            if df.empty:
                print(f"\033[91mAinda não foram realizadas transações!\033[0m")
            else:
                print('Histórico de Transações:')
                print(df)
        else:
            print(f"\033[91mO arquivo de histórico não foi encontrado.\033[0m")

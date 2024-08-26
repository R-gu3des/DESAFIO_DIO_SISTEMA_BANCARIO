from datetime import datetime
from time import sleep
import pandas as pd
import os

class BancoDIO:
    def __init__(self, nome_banco: str, valor_limite_saque: int) -> None:
        self.nome_banco = nome_banco
        self.limite_saques = 3
        self.saldo = 0
        self.valor_limite_saque = valor_limite_saque
        self.caminho_arquivo = 'data/historico.csv'
        self.carregar_dados()

    def carregar_dados(self):
        if os.path.exists(self.caminho_arquivo):
            df = pd.read_csv(self.caminho_arquivo)
            if 'Saldo Atual' in df.columns:
                self.saldo = df['Saldo Atual'].iloc[-1]  # Atualiza o saldo com o último valor

    def deposito(self):
        while True:
            valor_str = input("\nDigite um valor para depósito: ")
            if valor_str.replace('.', '', 1).isdigit():
                valor = float(valor_str)
                if valor > 0:
                    self.saldo += valor
                    print(f"\n\033[92mDepósito realizado com sucesso!\033[0m")
                    self.informacao_transacao('Depósito', {'Valor Depositado': valor})
                    break
                else:
                    print(f"\n\033[91mO valor de depósito deve ser positivo.\033[0m")
            else:
                print(f"\n\033[91mValor inválido. Tente novamente.\033[0m")
        sleep(4)

    def verificar_saques_diarios(self):
        hoje = datetime.now().date()
        if os.path.exists(self.caminho_arquivo):
            df = pd.read_csv(self.caminho_arquivo)
            df['Dia da Transação'] = pd.to_datetime(df['Dia da Transação']).dt.date
            saques_hoje = df[(df['Dia da Transação'] == hoje) & (df['Tipo de Operação'] == 'Saque')]
            return len(saques_hoje)
        return 0

    def saque(self):
        if self.verificar_saques_diarios() >= self.limite_saques:
            print(f"\n\033[91mLimite diário de saques atingido!\033[0m")
            return

        valor_str = input("\nDigite um valor para saque: ")
        if valor_str.replace('.', '', 1).isdigit():
            valor = float(valor_str)
            if valor > 0:
                if valor <= self.saldo and valor <= self.valor_limite_saque:
                    self.saldo -= valor
                    self.informacao_transacao('Saque', {'Valor Sacado': valor})
                    print(f"\n\033[92mSaque realizado com sucesso!\033[0m")
                elif valor > self.saldo:
                    print(f"\n\033[91mSaldo insuficiente! Saldo atual: {self.saldo:.2f}\033[0m")
                else:
                    print(f"\n\033[91mSaque excede o limite permitido: {self.valor_limite_saque:.2f}\033[0m")
            else:
                print(f"\n\033[91mO valor de saque deve ser positivo.\033[0m")
        else:
            print(f"\n\033[91mValor inválido. Tente novamente.\033[0m")
        sleep(4)

    def informacao_transacao(self, transacao=None, dicionario=None):
        os.makedirs('data', exist_ok=True)
        dados = {
            'Nome do Banco': [self.nome_banco],
            'Dia da Transação': [datetime.now()],
            'Tipo de Operação': [transacao],
            'Saldo Atual': [self.saldo]
        }
        for chave, valor in dicionario.items():
            dados[chave.capitalize()] = [valor]

        df = pd.DataFrame(dados)
        df.to_csv(self.caminho_arquivo, mode='a', header=not os.path.exists(self.caminho_arquivo), index=False)

    def historico_transacao(self):
        if os.path.exists(self.caminho_arquivo):
            df = pd.read_csv(self.caminho_arquivo)
            if not df.empty:
                print('\nHistórico de Transações:')
                print(df)
            else:
                print(f"\n\033[91mNenhuma transação realizada até o momento!\033[0m")
        else:
            print(f"\n\033[91mArquivo de histórico não encontrado.\033[0m")
        
        entrada = input('\nPressione qualquer tecla e clique ENTER para continuar: ')

        if entrada:
            pass

import BancoDIO
import os
import sys
from time import sleep

class Menu():

    def __init__(self, banco: BancoDIO) -> None:
        self.banco = banco

    def mostrar_menu(self):
        texto = f"""
========= Bem Vindo a sua conta no banco {self.banco.nome_banco} =========

Saldo Atual: {self.banco.saldo}
Limite de saques: {self.banco.limite_saques}
Valor limite por saque: {self.banco.valor_limite_saque}

Escolha uma das opções a seguir:

[0] Desejo sair
[1] Depósito
[2] Saque
[3] Histórico de Atividade

===========================================================
"""
        
        print(texto)

    def executar(self):
        while True:
            os.system('cls')
            self.mostrar_menu()
            tipo_de_operacao = input('Digite a opção desejada (0-3): ')

            # Verifica se a entrada é um número e se está dentro do intervalo válido
            if tipo_de_operacao.isdigit() and int(tipo_de_operacao) in range(4):
                tipo_de_operacao = int(tipo_de_operacao)  # Converte a opção para inteiro

                if tipo_de_operacao == 0:
                    print("\nSaindo do sistema...")
                    sys.exit()
                    
                elif tipo_de_operacao == 1:
                    print("\nIniciando operação de depósito!")
                    self.banco.deposito()

                elif tipo_de_operacao == 2:
                    print("\nIniciando operação de saque!")
                    self.banco.saque()

                elif tipo_de_operacao == 3:
                    print("\nVisualizando o histórico de atividades!")
                    # Chame o método de histórico de atividade
                    self.banco.historico_transacao()
                    
            else:
                print(f"\n\033[91mOpção inválida! Tente novamente.\033[0m")
                sleep(4)

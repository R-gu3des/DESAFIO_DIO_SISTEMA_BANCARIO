from BancoDIO import BancoDIO
from Menu import Menu

if __name__ == '__main__':
    banco_dio = BancoDIO('Banco DIO', 500)
    menu = Menu(banco_dio)
    menu.executar()

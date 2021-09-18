from io import open_code
from typing import Tuple
from cliente import Cliente
from os import set_inheritable
import socket
import mysql.connector
from mysql.connector import Error as db_error

# Python e MySQL : https://pynative.com/python-mysql-insert-data-into-database-table/


class Server():

    def __init__(self, host, port):
        # Construtor
        self._host = host
        self._port = port
        self._tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start(self):
        # Inicia o serviço do servidor
        # Definir uma porta específica para o serviço
        endpoint = (self._host, self._port)
        try:
            self._tcp.bind(endpoint)
            self._tcp.listen(1)  # Possíveis conexões
            print(f"Servidor iniciado em {self._host}:{self._port}")
            try:
                connection = mysql.connector.connect(host='localhost',
                                                     database='bd_distribuidos',
                                                     user='root',
                                                     password='1234')

                if connection.is_connected():
                    cursor = connection.cursor()
                    db_Info = connection.get_server_info()
                    print(
                        "Connected to MySQL database... MySQL Server version on ", db_Info)
            except db_error:
                print("Error while connecting to MySQL", db_error)
            finally:

                while True:
                    # Con é informações do cliente | cliente é ip e porta do cliente
                    con, cliente = self._tcp.accept()
                    # Executar os serviços.
                    self._service(con, cliente, cursor, connection)
                if connection.is_connected():
                    connection.close()
                    print("MySQL connection is closed")
        except Exception as e:
            print(f"Erro ao inicializar o server: {e.args}")

    def _service(self, con, cliente, cursor, connection):
        # Método dos serviços do servidor (banco de dados)
        while True:
            print(f"Atendendo o cliente {cliente}")
            try:
                # Recebendo a mensagem do cliente, dados brutos, fluxo de bytes
                mensagem = con.recv(2048)
                mensagem_decodificada = str(mensagem.decode(
                    'ascii'))  # Bytes representam caracteres
                """
                    A nossa ideia é splitar a mensagem com ":".
                    Mensagem de login -> login:usuario:senha
                    Mensagem de cadastro-> cadastro:coins:nickname:password:nome:email
                """
                msg = mensagem_decodificada.split(
                    ":")  # Nossa mensagem é da forma: acao:operadores:...
                print(f"Mensagem: {msg}")
                if (msg[0] == "cadastro"):
                    resposta = self.__cadastro(
                        cursor, connection, msg[1], msg[2], msg[3], msg[4], msg[5])
                elif (msg[0] == "login"):
                    resposta = self.__login(cursor, connection, msg[1], msg[2])
                else:
                    break

                # Converter a resposta para bytes também.
                con.send(bytes(str(resposta), 'ascii'))
                print(f"{cliente} -> requisição atendida !")

            # Erros de conexão (envio ou recebimento dos dados, divisão por 0, algum caractere invalido)
            except OSError as os:
                print(f"Erro na conexão {cliente}:{os.args}")
                return

   #################################################################################################################################
    """
        Seção para criarmos as funcionalidades do servidor de cadastro, login, etc :
    """

    def __cadastro(self, cursor, connection, coins, nickname, password, nome, email):
        try:
            """
                Verificar se essas credenciais já estão no banco:
            """
            queryVerificacao = """SELECT * FROM usuario WHERE (usuario.nickname = '"""+str(
                nickname)+"""');"""
            # print(queryVerificacao)
            cursor = connection.cursor()
            cursor.execute(queryVerificacao)
            verificacao = cursor.fetchall()
            #print(f"Numero de registros: {len(verificacao)}")
            if (len(verificacao) > 0):
                return("======> Nickname ja existente! Tente novamente.")
            else:
                """
                    Primeiramente, criaremos o álbum desse usuário:
                """
                queryCriaAlbum = """INSERT INTO album VALUES();"""
                result = cursor.execute(queryCriaAlbum)
                connection.commit()
                #print("Query executada")
                print("==> Álbum criado com sucesso !")
                """
                    Pegando o id do último album inserido
                """

                cursor = connection.cursor()
                cursor.execute("SELECT MAX(idAlbum) AS ultimoValor FROM album")
                resultado = cursor.fetchall()
                for id in resultado:
                    resultado = id[0]
                """
                    Setando as cartas nos slots respectivos desse usuário
                """
                for i in range(1, 31):
                    queryInsertSlot = """INSERT INTO album_has_slot values (""" + str(
                        resultado)+""","""+str(i)+""","""+str(i)+""",False);"""
                    # print(queryInsertSlot)
                    result = cursor.execute(queryInsertSlot)
                    connection.commit()
                print("==> Slots iniciados com sucesso!")
                """
                    Criando a mochila desse usuário
                """
                queryCriaMochila = """INSERT INTO mochila values();"""
                result = cursor.execute(queryCriaMochila)
                connection.commit()
                print("==> Mochila criada com sucesso !")
                """
                    Montando a query de inserção do usuário em sino Banco de Dados  :
                """
                query = """INSERT INTO usuario (coins,nickname,password,nome,email,Mochila_idMochila,Album_idAlbum) values (""" + \
                    coins+",'"+nickname+"','"+password+"','"+nome+"','" + \
                        email+"',"+str(resultado)+","+str(resultado)+""");"""
                print(f"{query}")
                result = cursor.execute(query)
                connection.commit()
                print("===> Todas as querys foram executadas")
                return("=====> Cadastro realizado com sucesso !")

        except db_error:
            return("=====> Erro ao realizar o cadastro !")

    def __login(self, cursor, connection, nickname, senha):
        """
            Formato padrão da query de seleção
        """
        query = """SELECT * FROM usuario WHERE (nickname='""" + \
            nickname+"'"+" and password='"+senha+"');"
        # print(f"{query}")
        """
            Tentando executar a query de seleção
        """
        try:
            result = cursor.execute(query)
            """
                Retorna uma lista com os registros encontrados:
            """
            resultados = cursor.fetchall()
            if(len(resultados) > 0):
                """
                    PRÓXIMO PASSO: MANDAR ESSAS INFORMAÇÕES DE LOGIN PARA SEREM CARREGADAS NA NOSSA TELA INICIAL DO GAME
                    PARA PODER CARREGAR O ALBUM DESSE USUÁRIO, SUA MOCHILA E DEMAIS INFORMAÇÕES.
                """
                print(resultados)
                return(("login",) + tuple(resultados[0]))

            else:
                return("=====> Nao foi possivel realizar login !")
        except db_error:
            return("=====> Erro ao realizar o login !")


# <>loja - -> tipo compra(5 cartas randons) --> tem que criar mochila_has_carta com o id
    # gerado randomicamente, além disso deve retirar a quantidade de coins.
    # <INSERT INTO mochila_has_carta VALUE(resultados[6], random, 1);>
    # <UPDATE usuario SET coins = coins - 25 WHERE idUsuario = resultados[0];>

# <>mostrar album

# <>colocar carta no album -> subtrair do mochila_has_carta e faz is_ocupado ser 1

# <>retirar carta do album --> incremnta do mochila_has_carta e faz is_ocupado ser 0

# <>deletar carta
# <UPDATE mochila_has_carta SET numero = numero - 1 WHERE Mochila_idMochila = resultados[6]>

# <>sistema de recompensa de coins.

# <>leilão

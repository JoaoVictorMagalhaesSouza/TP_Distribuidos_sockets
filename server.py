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
                                                     password='JVictor@00')

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
                elif (msg[0] == "loja"):
                    cartas = []
                    for i in range(4,len(msg)):
                        
                        cartas.append(int(msg[i]))
                    
                    resposta = self.__compraCartaLoja(cursor,connection,msg[1],msg[2],msg[3],cartas)
                elif (msg[0] == "minhaMochila"):
                    resposta = self.__minhaMochila(cursor,connection,msg[1])
                elif (msg[0] == "insereAlbum"):
                    resposta = self.__insereAlbum(cursor,connection,msg[1],msg[2],msg[3])
                elif (msg[0] == "visualizaAlbum"):
                    resposta = self.__visualizaAlbum(cursor,connection,msg[1])
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
    def __visualizaAlbum(self,cursor,connection,idAlbum):
        try:
            #Mostrar somente as cartas que ele colocou no álbum.
            queryVisualizaAlbum = "SELECT * FROM album_has_slot WHERE (Album_idAlbum = '"+idAlbum+"' and is_ocupado=1);"
            cursor = connection.cursor()
            cursor.execute(queryVisualizaAlbum)
            verificacao = cursor.fetchall()
            cartas = []
            nomeCartas = []
            if (len(verificacao)==0):
                return("Voce ainda nao possui cartas no album.")
            else:
                for i in verificacao:
                    cartas.append(i[2])
                for i in cartas:
                    query = "SELECT * FROM carta WHERE (idCarta = '"+str(i)+"');"
                    print(f"Q1: {query}")
                    cursor = connection.cursor()
                    cursor.execute(query)
                    verificacao = cursor.fetchall()
                    for j in verificacao:
                        nomeCartas.append(j[1])
                return(nomeCartas)


        except db_error:
            return("Nao foi possivel exibir o album.")
    
    def __insereAlbum(self,cursor,connection,idMochila,idAlbum,nomeCarta):
        try:
            
            """
                Primeiro tirar a carta da mochila.
            """
            queryIdentificacao = "SELECT * FROM carta WHERE (nome = '"+nomeCarta+"');"
            cursor = connection.cursor()
            cursor.execute(queryIdentificacao)
            verificacao = cursor.fetchall()
            
            for i in verificacao:
                idCarta = i[0]
            queryRemocao = "UPDATE mochila_has_carta SET numero = numero - 1 WHERE (Mochila_idMochila = '"""+str(idMochila)+"' and Carta_idCarta = '"+str(idCarta)+"');"
            print(f"QR {queryRemocao}")
            result = cursor.execute(queryRemocao)
            connection.commit()
            
            """
                Verificar se a carta já está lá
            """
            queryVerificaAlbum = "SELECT * FROM album_has_slot WHERE (Album_idAlbum = '"+str(idAlbum)+"' and Slot_Carta_idCarta = '"+str(idCarta)+"' and is_ocupado = 0);"
            print(f"QV {queryVerificaAlbum}")
            cursor = connection.cursor()
            cursor.execute(queryVerificaAlbum)
            verificacao = cursor.fetchall()
            
            print(len(verificacao))
            if (len(verificacao)==1): #Significa que a carta ainda não está no Album
                queryAdicionaAlbum = "UPDATE album_has_slot SET is_ocupado = 1 WHERE (Album_idAlbum = '"+str(idAlbum)+"' and Slot_Carta_idCarta = '"+str(idCarta)+"');"
                result = cursor.execute(queryAdicionaAlbum)
                connection.commit()
                return("=====> Carta inserida no album com sucesso!")
            else: #Siginifica que a carta já está no album
                return("Carta ja esta no album.")
        except db_error:
            return("Erro ao inserir carta no album.")
        
    
    def __minhaMochila(self,cursor,connection,idMochila):
        try:
            queryVisualizaMochila = "SELECT * FROM mochila_has_carta WHERE (Mochila_idMochila = '"+idMochila+"' and numero > 0);"
            print(f"Q0: {queryVisualizaMochila}")
            cursor = connection.cursor()
            cursor.execute(queryVisualizaMochila)
            verificacao = cursor.fetchall()
            cartas = []
            nomeCartas =  []
            for i in verificacao:
                cartas.append(i[1])

            for i in cartas:
                query = "SELECT * FROM carta WHERE (idCarta = '"+str(i)+"');"
                print(f"Q1: {query}")
                cursor = connection.cursor()
                cursor.execute(query)
                verificacao = cursor.fetchall()
                for j in verificacao:
                    nomeCartas.append(j[1])


            #print(f"Cartas que o usuario possui: {cartas}")

            return(nomeCartas)

        except db_error:
            return("Erro ao visualizar dados da mochila do usuário.")

    def __compraCartaLoja(self,cursor,connection,coinsRemovidas,idMochila,idUser,cartas):
        
# <>loja - -> tipo compra(5 cartas randons) --> tem que criar mochila_has_carta com o id
    # gerado randomicamente, além disso deve retirar a quantidade de coins.
    # <INSERT INTO mochila_has_carta VALUE(resultados[6], random, 1);>
    # <UPDATE usuario SET coins = coins - 25 WHERE idUsuario = resultados[0];>
        try:
            print(f"Coins: {coinsRemovidas}")
            print(f"Cartas: {cartas}")
            for i in cartas: #Avaliar cada carta a ser inserida...
                #Primeiro temos que verificar se a carta já está na mochila
                queryVerificaCartaMochila = """SELECT * FROM mochila_has_carta WHERE (Mochila_idMochila = '"""+str(idMochila)+"' and Carta_idCarta = '"+str(i)+"');"
                print(f"Q1: {queryVerificaCartaMochila}")
                cursor = connection.cursor()
                cursor.execute(queryVerificaCartaMochila)
                verificacao = cursor.fetchall()
               
                if (len(verificacao) > 0): #Carta já está na mochila
                    queryInsereMochila = "UPDATE mochila_has_carta SET numero = numero + 1 WHERE (Mochila_idMochila = '"""+str(idMochila)+"' and Carta_idCarta = '"+str(i)+"');"
                else:
                    queryInsereMochila = """INSERT INTO mochila_has_carta VALUES("""+"'"+str(idMochila)+"','"+str(i)+"','1');"
                print(f"Q2: {queryInsereMochila}")
                result = cursor.execute(queryInsereMochila)
                connection.commit()
            """
                Remover as coins
            """
            queryRemoveCoins = "UPDATE usuario SET coins = coins -"+coinsRemovidas+" WHERE (idUsuario = '"+idUser+"'); "
            print(f"Q3: {queryRemoveCoins}")
            result = cursor.execute(queryRemoveCoins)
            connection.commit()
            return("====> Cartas compradas com sucesso !")

        except db_error:
            return("Erro ao comprar carta!")

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



# <>mostrar album

# <>colocar carta no album -> subtrair do mochila_has_carta e faz is_ocupado ser 1

# <>retirar carta do album --> incremnta do mochila_has_carta e faz is_ocupado ser 0

# <>deletar carta
# <UPDATE mochila_has_carta SET numero = numero - 1 WHERE Mochila_idMochila = resultados[6]>

# <>sistema de recompensa de coins.

# <>leilão

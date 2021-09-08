from cliente import Cliente
from os import set_inheritable
import socket
import mysql.connector
from mysql.connector import Error as db_error

class Server():

    def __init__(self, host, port) :
        #Construtor
        self._host = host
        self._port = port
        self._tcp = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    def start(self):
        #Inicia o serviço do servidor
        endpoint = (self._host, self._port) #Definir uma porta específica para o serviço 
        try:
            self._tcp.bind(endpoint)
            self._tcp.listen(1) #Possíveis conexões
            print(f"Servidor iniciado em {self._host}:{self._port}")
            try:
                connection = mysql.connector.connect(host='localhost',
                                                    database='bd_distribuidos',
                                                    user='root',
                                                    password='JVictor@00')

                if connection.is_connected():
                    cursor = connection.cursor()
                    db_Info = connection.get_server_info()
                    print("Connected to MySQL database... MySQL Server version on ", db_Info)
            except db_error:
                print("Error while connecting to MySQL", db_error)
            finally:
                
                while True:
                    con, cliente = self._tcp.accept() #Con é informações do cliente | cliente é ip e porta do cliente
                    self._service(con,cliente,cursor,connection) # Executar os serviços.
                if connection.is_connected():
                    connection.close()
                    print("MySQL connection is closed")
        except Exception as e:
            print(f"Erro ao inicializar o server: {e.args}")

    def __cadastro(self,cursor,connection):
        query = """INSERT INTO usuario (coins,nickname,password,nome,email,Mochila_idMochila,Album_idAlbum) values """+"""(20000,"CoCriator","Unamed","Unamed1234","melhordetodos@gmail.com",1,1);"""
        print(f"{query}")
        print("1")
        result = cursor.execute(query)
        connection.commit()
        print("Query executada")
        
                      

   

    
    def _service(self,con,cliente,cursor,connection):
        #Método dos serviços do servidor (banco de dados)
        print(f"Atendendo o cliente {cliente}")
        try:
            mensagem = con.recv(1024) #Recebendo a mensagem do cliente, dados brutos, fluxo de bytes
            mensagem_decodificada = str(mensagem.decode('ascii')) #Bytes representam caracteres
            self.__cadastro(cursor,connection)
            

           
            con.send(bytes(str(resposta),'ascii')) #Converter a resposta para bytes também.
            print(f"{cliente} -> requisição atendida !")

            

        except OSError as os: #Erros de conexão (envio ou recebimento dos dados, divisão por 0, algum caractere invalido)
            print(f"Erro na conexão {cliente}:{os.args}")
            return 
        except Exception as e:
            print(f"Erro nos dados recebidos do cliente {cliente}:{e.args}")
            con.send(bytes("Erro",'ascii'))
    

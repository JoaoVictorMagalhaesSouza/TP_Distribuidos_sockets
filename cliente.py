import socket

class Cliente():
    def __init__(self,server_ip,porta):
        self.__server_ip = server_ip
        self.__port = porta
        self.__tcp = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    def start(self):  #Inicializa a conexão do cliente
        endpoint = (self.__server_ip,self.__port) 
        try:
            self.__tcp.connect(endpoint) #Tentativa de conexão com o server
            print("Conexão realizada!")
            self.__method()
        except Exception as e:
            print(f"Erro ao estabelecer conexão com o server {e.args}")
    def __method(self):# __ é privado
        try:
            mensagem = ""
            mensagem = input("Digite a operação: ")
            while mensagem!="x":
                self.__tcp.send(bytes(mensagem,'ascii'))
                resposta = self.__tcp.recv(2048)
                print(f"= {resposta.decode('ascii')}")
                mensagem = input("Digite a operação: ")
            self.__tcp.close()
        except Exception as e:
            print(f"Houve um erro na comunicação {e.args}")

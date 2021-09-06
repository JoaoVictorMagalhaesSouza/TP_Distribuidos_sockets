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
            while mensagem!="x":
                mensagem = input("Digite a operação: ")
                if mensagem=="":
                    continue
                elif mensagem=="x":
                    break
                self.__tcp.send(bytes(mensagem,"ascii"))
                resposta = self.__tcp.recv(1024)
                print(f"= {resposta.decode('ascii')}")
            self.__tcp.close()
        except Exception as e:
            print(f"Houve um erro na comunicação {e.args}")

import socket

class Server():

    def __init__(self, host, port) :
        #Construtor
        self.host = host
        self.port = port
        self._tcp = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    def start():
        #Inicia o serviço do servidor
        endpoint = (self._host, self._port) #Definir uma porta específica para o serviço 
        try:
            self._tcp.bind(endpoint)
            self._tcp.listen(1) #Possíveis conexões
            print(f"Servidor iniciado em {self._host}:{self._port}")
            while True:
                con, cliente = self._tcp.accept() #Con é informações do cliente | cliente é ip e porta do cliente
                self._service(con,cliente) # Executar os serviços.
        except Exception as e:
            print(f"Erro ao inicializar o server: {e.args}")
    
    def _service(self,con,cliente):
        #Método dos serviços do servidor (banco de dados)
        print(f"Atendendo o cliente {cliente}")


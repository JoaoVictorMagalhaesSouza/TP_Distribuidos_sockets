import socket

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
            while True:
                con, cliente = self._tcp.accept() #Con é informações do cliente | cliente é ip e porta do cliente
                self._service(con,cliente) # Executar os serviços.
        except Exception as e:
            print(f"Erro ao inicializar o server: {e.args}")
    
    def _service(self,con,cliente):
        #Método dos serviços do servidor (banco de dados)
        print(f"Atendendo o cliente {cliente}")
        operadores = ["+","-","*","/"]
        while True:
            try:
                mensagem = con.recv(1024) #Recebendo a mensagem do cliente, dados brutos, fluxo de bytes
                mensagem_decodificada = str(mensagem.decode('ascii')) #Bytes representam caracteres
                #É importante criar uma formatação da mensagem enviada pelo cliente
                #Exemplo: 15+5 onde 15 é o operando1, "+" operador e 5 o operando2
                #Logo, a mensagem é da forma: operando1operadoroperando2
                for x in operadores:
                    if mensagem_decodificada.find(x) > 0:
                        op = x
                        mensagem_decodificada = mensagem_decodificada.split(op)
                        print("Mensagem decodificada",mensagem_decodificada)
                        break
                if op=="+":
                    resposta = float(mensagem_decodificada[0]) + float(mensagem_decodificada[1])
                elif op=="-":
                    resposta = float(mensagem_decodificada[0]) - float(mensagem_decodificada[1])
                elif op=="*":
                    resposta = float(mensagem_decodificada[0]) * float(mensagem_decodificada[1])
                elif op=="/":
                    resposta = float(mensagem_decodificada[0]) / float(mensagem_decodificada[1])
                else:
                    resposta = "Operação inválida"

                con.send(bytes(str(resposta),'ascii')) #Converter a resposta para bytes também.
                print(f"{cliente} -> requisição atendida !")

            except OSError as os: #Erros de conexão (envio ou recebimento dos dados, divisão por 0, algum caractere invalido)
                print(f"Erro na conexão {cliente}:{os.args}")
                return 
            except Exception as e:
                print(f"Erro nos dados recebidos do cliente {cliente}:{e.args}")
                con.send(bytes("Erro",'ascii'))

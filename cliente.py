import socket
import random


class Cliente():
    def __init__(self, server_ip, porta):
        self.__server_ip = server_ip
        self.__port = porta
        self.__tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start(self):  # Inicializa a conexão do cliente
        endpoint = (self.__server_ip, self.__port)
        try:

            self.__tcp.connect(endpoint)  # Tentativa de conexão com o server
            print("Conexão realizada!")
            self.__method()
        except Exception as e:
            print(f"Erro ao estabelecer conexão com o server {e.args}")

    def __method(self):  # __ é privado
        try:
            mensagem = ""
            mensagem = input("Digite a operação: ")
            while mensagem != "x":
                self.__tcp.send(bytes(mensagem, 'ascii'))
                resposta = self.__tcp.recv(2048)
                resposta = resposta.decode('ascii')
                resposta = resposta.split(",")
                novo = []
                for x in resposta:
                    item = x
                    for y in ['\n', '\t', '/', '.', '-', '(', ')', "'"]:
                        item = item.replace(y, "")
                    novo.append(item)
                resposta=novo
                print(f"= Resposta: {novo}")
                #('login', 1, 300, 'a', 'b', 'c', 'd', 1, 1)
                if (resposta[0] == 'login'): #Se o login for bem sucedido.
                    while True:
                        
                        print("BEM VINDO(A) AO NOSSO GAME!")
                        print("1) Acessar a Loja.")
                        print("2) Inserir Carta da Mochila no Álbum.")
                        print("3) Ver meu Álbum de Figurinhas.")
                        print("0) Sair.")
                        escolha = input("Digite sua escolha: ")
                        if (escolha=="1"): #Loja
                            print("Pacotinhos disponíveis:")
                            print("1) 1 carta aleatória = $50 coins.")
                            print("2) 3 cartas aleatórias = $135 coins.")
                            print("3) 5 cartas aleatórias = $225 coins.")
                            
                            pacotinho = input(f"Você tem {resposta[2]} coins. Escolha qual pacotinho quer comprar: ")
                            if (int(resposta[2]) < 50):
                                print("Voce nao tem moedas suficentes! Faca uma recarga agora!")
                                continue
                            elif (pacotinho=="1") and (int(resposta[2])>=50):
                                cartaPacote = []
                                cartaPacote.append(random.randint(1,31)) # Gerar uma carta de 1 a 30.
                                mensagem="loja:50:"+resposta[1]+":"+resposta[7]+":"+str(cartaPacote[0]) # Padronização da mensagem
                                resposta[2] = str(int(resposta[2])-50)
                            elif (pacotinho=="2") and (int(resposta[2])>=135):
                                cartaPacote = []
                                for i in range(3):
                                    cartaPacote.append(random.randint(1,31))
                                mensagem="loja:135:"+resposta[1]+":"+resposta[7]+":"+str(cartaPacote[0])+":"+str(cartaPacote[1])+":"+str(cartaPacote[2])
                                resposta[2] = str(int(resposta[2])-135)
                            elif (pacotinho=="3") and (int(resposta[2])>=225):
                                cartaPacote = []
                                for i in range(5):
                                    cartaPacote.append(random.randint(1,31))
                                mensagem="loja:225:"+resposta[1]+":"+resposta[7]+":"+str(cartaPacote[0])+":"+str(cartaPacote[1])+":"+str(cartaPacote[2])+":"+str(cartaPacote[3])+":"+str(cartaPacote[4])
                                resposta[2] = str(int(resposta[2])-225)
                            self.__tcp.send(bytes(mensagem, 'ascii'))
                            respostaLoja = self.__tcp.recv(2048)
                            respostaLoja = respostaLoja.decode('ascii')
                            print(respostaLoja)
                        if (escolha=="2"):
                            print("As cartas que você tem na mochila são: ")
                            mensagem1 = "minhaMochila:"+resposta[7] #idMochila
                            self.__tcp.send(bytes(mensagem1, 'ascii'))
                            respostaCartasMochila = self.__tcp.recv(2048)
                            respostaCartasMochila = respostaCartasMochila.decode('ascii')
                            print(respostaCartasMochila)
                            """
                                Tratar aqui depois: deixar o cara digitar apenas uma das cartas mostradas.
                            """
                            escolhaCarta = input("Digite o nome da carta que você quer inserir no álbum: ")
                            mensagem2 = "insereAlbum:"+resposta[7]+":"+resposta[8]+":"+escolhaCarta #idMochila:idAlbum:Python
                            self.__tcp.send(bytes(mensagem2, 'ascii'))   
                            respostaInsereAlbum = self.__tcp.recv(2048)
                            respostaInsereAlbum = respostaInsereAlbum.decode('ascii')
                            print(respostaInsereAlbum)
                        if (escolha=="3"):
                            mensagem3 = "visualizaAlbum:"+resposta[8]
                            self.__tcp.send(bytes(mensagem3, 'ascii'))   
                            respostaVisualizaAlbum = self.__tcp.recv(2048)
                            respostaVisualizaAlbum = respostaVisualizaAlbum.decode('ascii')
                            print(f"As cartas do seu album sao: {respostaVisualizaAlbum}")


                mensagem = input("Digite a operação: ")

            self.__tcp.close()
        except Exception as e:
            print(f"Houve um erro na comunicação {e.args}")

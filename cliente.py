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
            #print("Conexão realizada!")
            self.__method()
        except Exception as e:
            print(f"Erro ao estabelecer conexão com o server {e.args}")

    def __method(self):  # __ é privado
        try:
            mensagem = ""
            print("#################################################################")
            print("#    Olá ! Seja bem vindo ao Programming Language Collection    #")
            print("#    1) Fazer cadastro.                                         #")
            print("#    2) Fazer login.                                            #")
            print("#    3) Sair do sistema.                                        #")   
            print("#################################################################")
            print("")
            print("")
            escolha = input("Digite a operação: ")
            if (escolha == "1"):
                print("#################################################################")
                print("#                   INFORMAÇÕES DE CADASTRO                     #")
                print("#################################################################")
                nick = input("Digite seu nickname: ")
                senha = input("Digite sua senha: ")
                nome = input("Digite seu nome: ")
                email = input("Digite seu email: ")
                mensagem = "cadastro:0:"+nick+":"+senha+":"+nome+":"+email
                print("")
                print("")
            elif (escolha == "2"):
                print("#################################################################")
                print("#                     INFORMAÇÕES DE LOGIN                      #")
                print("#################################################################")
                nick = input("Digite seu nickname: ")
                senha = input("Digite sua senha: ")               
                mensagem = "login:"+nick+":"+senha
                print("")
                print("")
            else:
                mensagem = "3"
            while mensagem != "3":
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
                resposta = novo
                if(resposta[0] != 'login'):
                    print(f"{resposta}")
                    print("")
                    print("")
                #('login', 1, 300, 'a', 'b', 'c', 'd', 1, 1)
                if (resposta[0] == 'login'):  # Se o login for bem sucedido.
                    print("=====> Login realizado com sucesso !")
                    print("")
                    print("")

                    while True:
                        print("*****************************************************************")
                        print("*    BEM VINDO(A) AO NOSSO GAME!                                *")
                        print("*    1) Acessar a Loja.                                         *")
                        print("*    2) Inserir Carta da Mochila no Álbum.                      *")
                        print("*    3) Visualizar meu Álbum de Figurinhas.                     *")
                        print("*    4) Visualizar Cartas na Mochila.                           *")
                        print("*    5) Deletar Carta da Mochila.                               *")
                        print("*    6) Mover Carta do Álbum para a Mochila.                    *")
                        print("*    7) Leiloar/Comprar/Remover uma Carta.                      *")
                        print("*    0) Logoff.                                                 *")
                        print("*****************************************************************")
                        escolha = input("Digite sua escolha: ")
                        print("")
                        print("")
                        if (escolha == "1"):  # Loja
                            print("Pacotinhos disponíveis:")
                            print("1) 1 carta aleatória = $50 coins.")
                            print("2) 3 cartas aleatórias = $135 coins.")
                            print("3) 5 cartas aleatórias = $225 coins.")
                            pacotinho = input(
                                f"Você tem {resposta[2]} coins. Escolha qual opção de pacotinho quer comprar: ")
                            print("")
                            print("")

                            if (int(resposta[2]) < 50):
                                print(
                                    "=====> [ERRO] Voce nao tem moedas suficentes! Faca uma recarga agora!")
                                continue
                            elif (pacotinho == "1") and (int(resposta[2]) >= 50):
                                cartaPacote = []
                                # Gerar uma carta de 1 a 30.
                                cartaPacote.append(random.randint(1, 31))
                                # Padronização da mensagem
                                mensagem = "loja:50:" + \
                                    resposta[1]+":"+resposta[7] + \
                                    ":"+str(cartaPacote[0])
                                resposta[2] = str(int(resposta[2])-50)
                            elif (pacotinho == "2") and (int(resposta[2]) >= 135):
                                cartaPacote = []
                                for i in range(3):
                                    cartaPacote.append(random.randint(1, 31))
                                mensagem = "loja:135:"+resposta[1]+":"+resposta[7]+":"+str(
                                    cartaPacote[0])+":"+str(cartaPacote[1])+":"+str(cartaPacote[2])
                                resposta[2] = str(int(resposta[2])-135)
                            elif (pacotinho == "3") and (int(resposta[2]) >= 225):
                                cartaPacote = []
                                for i in range(5):
                                    cartaPacote.append(random.randint(1, 31))
                                mensagem = "loja:225:"+resposta[1]+":"+resposta[7]+":"+str(cartaPacote[0])+":"+str(
                                    cartaPacote[1])+":"+str(cartaPacote[2])+":"+str(cartaPacote[3])+":"+str(cartaPacote[4])
                                resposta[2] = str(int(resposta[2])-225)
                            self.__tcp.send(bytes(mensagem, 'ascii'))
                            respostaLoja = self.__tcp.recv(2048)
                            respostaLoja = respostaLoja.decode('ascii')
                            print(respostaLoja)

                            mensagem = "login:"+nick+":"+senha
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
                            resposta = novo
                            print("")
                            print("")

                        elif (escolha == "2"):
                            print("As cartas que você tem na mochila são: ")
                            mensagem1 = "minhaMochila:" + \
                                resposta[7]  # idMochila
                            self.__tcp.send(bytes(mensagem1, 'ascii'))
                            respostaCartasMochila = self.__tcp.recv(2048)
                            respostaCartasMochila = respostaCartasMochila.decode(
                                'ascii')
                            if (respostaCartasMochila == "0"):
                                print(
                                    f"=====> Você ainda não possui cartas na mochila !")
                            else:
                                # print(respostaCartasMochila)
                                print("=====> Suas cartas são: ")
                                myCards = respostaCartasMochila.split(",")
                                j = 0
                                for i in myCards:
                                    i = i.replace("'", "")
                                    i = i.replace(" ", "")
                                    i = i.replace("[", "")
                                    i = i.replace("]", "")
                                    myCards[j] = i
                                    print(f"{j}) {i}")
                                    j += 1

                                """
                                    Tratar aqui depois: deixar o cara digitar apenas uma das cartas mostradas.
                                """
                                #print(f"{myCards}    {type(myCards)}")
                                escolhaCarta = input(
                                    "Digite o nome da carta que você quer inserir no álbum: ")
                                if (escolhaCarta in myCards):
                                    # idMochila:idAlbum:Python
                                    mensagem2 = "insereAlbum:" + \
                                        resposta[7]+":"+resposta[8] + \
                                        ":"+escolhaCarta
                                    self.__tcp.send(bytes(mensagem2, 'ascii'))
                                    respostaInsereAlbum = self.__tcp.recv(2048)
                                    respostaInsereAlbum = respostaInsereAlbum.decode(
                                        'ascii')
                                    print(respostaInsereAlbum)
                                else:
                                    print(
                                        "=====> [ERRO] Digite uma carta que você possui !")
                            print("")
                            print("")

                        elif (escolha == "3"):
                            mensagem3 = "visualizaAlbum:"+resposta[8]
                            self.__tcp.send(bytes(mensagem3, 'ascii'))
                            respostaVisualizaAlbum = self.__tcp.recv(2048)
                            respostaVisualizaAlbum = respostaVisualizaAlbum.decode(
                                'ascii')
                            myAlbum = respostaVisualizaAlbum.split(",")
                            print(f"=====> As cartas do seu album sao: ")
                            for i in myAlbum:
                                i = i.replace("'", "")
                                i = i.replace(" ", "")
                                i = i.replace("[", "")
                                i = i.replace("]", "")
                                print(f"{i}")
                            print("")
                            print("")

                        elif (escolha == "4"):
                            mensagem1 = ""
                            print("As cartas que você tem na mochila são: ")
                            mensagem1 = "minhaMochila:" + \
                                resposta[7]  # idMochila
                            self.__tcp.send(bytes(mensagem1, 'ascii'))
                            respostaCartasMochila_2 = self.__tcp.recv(2048)
                            respostaCartasMochila_2 = respostaCartasMochila_2.decode(
                                'ascii')
                            if (respostaCartasMochila_2 == "0"):
                                print(
                                    f"=====> Você ainda não possui cartas na mochila !")
                            else:
                                # print(respostaCartasMochila)
                                print("=====> Suas cartas são: ")
                                myCards = respostaCartasMochila_2.split(",")
                                j = 0
                                for i in myCards:
                                    i = i.replace("'", "")
                                    i = i.replace(" ", "")
                                    i = i.replace("[", "")
                                    i = i.replace("]", "")
                                    print(f"{j}) {i}")
                                    j += 1
                            print("")
                            print("")

                        elif (escolha == "5"):
                            carta = input(
                                'Digite o nome da carta: ')
                            print('A carta escolhida é:', carta)
                            self.__tcp.send(
                                bytes('deletaCarta:' + carta + ':' + resposta[7], 'ascii'))

                            respostaRetirarCarta = self.__tcp.recv(2048)
                            respostaRetirarCarta = respostaRetirarCarta.decode(
                                'ascii')
                            print(respostaRetirarCarta)
                            print("")
                            print("")

                        elif(escolha == "6"):
                            carta = input(
                                'Digite o nome da carta: ')
                            print('A carta escolhida é:', carta)
                            self.__tcp.send(
                                bytes('retiraAlbum:' + carta + ':' + resposta[7] + ':' + resposta[8], 'ascii'))

                            respostaRetirarCarta = self.__tcp.recv(2048)
                            respostaRetirarCarta = respostaRetirarCarta.decode(
                                'ascii')
                            print(respostaRetirarCarta)
                            print("")
                            print("")

                        elif (escolha == "7"):
                            print("Bem vindo ao leilão!")
                            print("1) Anunciar uma Carta")
                            print("2) Comprar/Visualizar Cartas à Venda")
                            print("3) Retirar uma carta anunciada.")
                            escolhaLeilao = input(
                                "Escolha uma funcionalidade: ")
                            # Ver se já possui uma carta anunciada.
                            if (escolhaLeilao == "1"):
                                print(f"As cartas que você pode anunciar são: ")
                                mensagem1 = "minhaMochila:" + \
                                    resposta[7]  # idMochila
                                self.__tcp.send(bytes(mensagem1, 'ascii'))
                                respostaCartasMochila = self.__tcp.recv(2048)
                                respostaCartasMochila = respostaCartasMochila.decode(
                                    'ascii')
                                respostaCartasMochila = respostaCartasMochila.split(
                                    ",")
                                j = 0
                                for i in respostaCartasMochila:
                                    i = i.replace("'", "")
                                    i = i.replace(" ", "")
                                    i = i.replace("[", "")
                                    i = i.replace("]", "")
                                    print(f"{i}")
                                    j += 1

                                cartaAnunciada = input(
                                    "Digite o nome da carta a ser anunciada: ")
                                precoCarta = input(
                                    "Especifique por quanto deseja leiloar essa carta: ")

                                mensagemAnuncio = "leiloaCarta:" + \
                                    resposta[7]+":" + \
                                    cartaAnunciada+":"+precoCarta
                                self.__tcp.send(
                                    bytes(mensagemAnuncio, 'ascii'))
                                respostaLeiloaCarta = self.__tcp.recv(2048)
                                respostaLeiloaCarta = respostaLeiloaCarta.decode(
                                    'ascii')
                                print(respostaLeiloaCarta)
                                print("")
                                print("")

                            elif (escolhaLeilao == "2"):
                                
                                mensagemCartasLeilao = "mostraCartasLeilao:"
                                self.__tcp.send(
                                    bytes(mensagemCartasLeilao, 'ascii'))
                                respostaCartasLeilao = self.__tcp.recv(2048)
                                respostaCartasLeilao = respostaCartasLeilao.decode(
                                    'ascii')
                                # Transformar string em dict
                                if (respostaCartasLeilao=="0"):
                                    print("=====> Não há cartas anunciadas no leilao!")
                                else:
                                    print("Cartas à venda: ")
                                    respostaCartasLeilao = eval(
                                        respostaCartasLeilao)
                                    for i in range(len(respostaCartasLeilao["idVenda"])):
                                        print(
                                            f""" => ID: {respostaCartasLeilao["idVenda"][i]}    |    Nome do Vendedor: {respostaCartasLeilao["Nome"][i]}   |   Carta: {respostaCartasLeilao["Carta"][i]}   |   Preço: {respostaCartasLeilao["Preco"][i]}""")

                                    escolhaComprar = input(
                                        "Deseja comprar alguma carta ? 1-Sim | 2-Não :")
                                    if (escolhaComprar == "1"):
                                        print(f"Você possui {resposta[2]} coins.")
                                        cartaDesejada = int(
                                            input("Digite o id da compra que contém sua carta de interesse: "))
                                        print("A carta desejada é "+respostaCartasLeilao["Carta"][cartaDesejada]+", vendida por "+respostaCartasLeilao["Nome"][cartaDesejada]+" no valor de "+str(
                                            respostaCartasLeilao["Preco"][cartaDesejada])+" coins.")
                                        if (int(resposta[2]) >= int(respostaCartasLeilao["Preco"][cartaDesejada])):
                                            mensagemVenda = "vendeLeilao:" + \
                                                resposta[7]+":" + \
                                                respostaCartasLeilao["Nome"][cartaDesejada]
                                            self.__tcp.send(
                                                bytes(mensagemVenda, 'ascii'))
                                            respostaVenda = self.__tcp.recv(2048)
                                            respostaVenda = respostaVenda.decode(
                                                'ascii')
                                            print(respostaVenda)
                                        else:
                                            print(
                                                "=====> [ERRO] Você não possui moedas suficientes para comprar esta carta.")
                            elif (escolhaLeilao == "3"):
                                retiraLeilao = input(
                                    "Tem certeza que deseja remover a carta anunciada ? 1 - Sim | Outro - Não: ")

                                if (retiraLeilao == "1"):
                                    mensagemRetiraLeilao = "retiraCartaLeilao:" + \
                                        resposta[7]
                                    self.__tcp.send(
                                        bytes(mensagemRetiraLeilao, 'ascii'))
                                    respostaRetiraLeilao = self.__tcp.recv(
                                        2048)
                                    respostaRetiraLeilao = respostaRetiraLeilao.decode(
                                        'ascii')
                                    print(respostaRetiraLeilao)

                            print("")
                            print("")

                        elif (escolha == "0"):
                            self.__tcp.send(
                                bytes('logout:', 'ascii'))
                            break

                mensagem = ""
                print("#################################################################")
                print("#    Olá ! Seja bem vindo ao Programming Language Collection    #")
                print("#    1) Fazer cadastro.                                         #")
                print("#    2) Fazer login.                                            #")   
                print("#################################################################")
                escolha = input("Digite a operação: ")
                if (escolha == "1"):
                    nick = input("Digite seu nickname: ")
                    senha = input("Digite sua senha: ")
                    nome = input("Digite seu nome: ")
                    email = input("Digite seu email")
                    mensagem = "cadastro:0:"+nick+":"+senha+":"+nome+":"+email
                else:
                    nick = input("Digite seu nickname: ")
                    senha = input("Digite sua senha: ")
                    mensagem = "login:"+nick+":"+senha

            self.__tcp.close()
        except Exception as e:
            print(f"Houve um erro na comunicação {e.args}")

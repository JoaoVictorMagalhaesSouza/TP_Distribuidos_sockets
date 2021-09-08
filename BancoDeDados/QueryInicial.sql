USE bd_distribuidos;
#Criar as cartas todas :
INSERT INTO carta (nome,descricao,allstar) values ("Ruby","Teste",True),
("C","Teste",False);
#Criar os slots das cartas:
INSERT INTO slot (Carta_idCarta)values (1),(2);
SELECT * from slot;
#Criar o album de novo usuário:
INSERT INTO album values();
INSERT INTO album values();
SELECT * FROM album;
#Adicionar uma carta em um slot de um album específico(de um usuário, no caso):
#Album 1, slot 1, carta 1, ocupado False
#Album 2, slot 1, carta 1, ocupado False
INSERT INTO album_has_slot values (1,1,1,False);
INSERT INTO album_has_slot values (2,1,1,False);
SELECT * FROM album_has_slot;
#Agora mudaremos o status de ocupado para True do slot 1 no album 1.
UPDATE album_has_slot SET is_ocupado=True WHERE (Album_idAlbum=1 and Slot_idSlot=1); 
SELECT * FROM album_has_slot;

#Criar mochila
INSERT INTO mochila values() ;
SELECT * FROM mochila ;

SELECT * from usuario;

USE bd_distribuidos;

INSERT INTO mochila  values ();
SELECT * FROM mochila ;
#ALTER TABLE slot ADD is_ocupado BOOLEAN ;
INSERT INTO carta (nome,descricao,allstar) values("Java","Horrivel",True);
SELECT * from carta;
INSERT INTO slot (Carta_idCarta,is_ocupado)values (1,False);
SELECT * from slot;

INSERT INTO album (idAlbum,Slot_idSlot) values(1,2);
SELECT * from album;

INSERT INTO usuario (coins,nickname,password,nome,email,Mochila_idMochila,
					Album_idAlbum
                    ) values (200,"OBrabo","jv","João","jv@gmail.com",1,1);
select * from usuario;

SELECT * from slot ;
SELECT * from album;
update slot set slot.is_ocupado=False;
SELECT * from album where (album.idAlbum=1 and album.Slot_idSlot=1);
update album,slot set slot.is_ocupado = True WHERE (album.idAlbum=1)
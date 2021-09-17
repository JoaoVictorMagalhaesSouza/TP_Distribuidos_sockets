INSERT INTO slot (Carta_idCarta) VALUES
(1),
(2),
(3),
(4),
(5),
(6),
(7),
(8),
(9),
(10),
(11),
(12),
(13),
(14),
(15),
(16),
(17),
(18),
(19),
(20),
(21),
(22),
(23),
(24),
(25),
(26),
(27),
(28),
(29),
(30)
;

SELECT * from slot;
SELECT max(idSlot) from slot;

SELECT * from album;
DELETE FROM album;
SELECT * from album_has_slot;
DELETE FROM album_has_slot;
SELECT * from usuario;
SELECT * from usuario where (usuario.nickname = 'a');
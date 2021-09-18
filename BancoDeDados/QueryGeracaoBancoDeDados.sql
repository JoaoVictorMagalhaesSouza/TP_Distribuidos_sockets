-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema BD_Distribuidos
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema BD_Distribuidos
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `BD_Distribuidos` DEFAULT CHARACTER SET utf8 ;
USE `BD_Distribuidos` ;

-- -----------------------------------------------------
-- Table `BD_Distribuidos`.`Mochila`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `BD_Distribuidos`.`Mochila` (
  `idMochila` INT NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`idMochila`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `BD_Distribuidos`.`Album`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `BD_Distribuidos`.`Album` (
  `idAlbum` INT NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`idAlbum`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `BD_Distribuidos`.`Usuario`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `BD_Distribuidos`.`Usuario` (
  `idUsuario` INT NOT NULL AUTO_INCREMENT,
  `coins` INT NOT NULL,
  `nickname` VARCHAR(45) NOT NULL,
  `password` VARCHAR(45) NOT NULL,
  `nome` VARCHAR(45) NOT NULL,
  `email` VARCHAR(45) NOT NULL,
  `Mochila_idMochila` INT NOT NULL,
  `Album_idAlbum` INT NOT NULL,
  PRIMARY KEY (`idUsuario`, `Mochila_idMochila`, `Album_idAlbum`),
  INDEX `fk_Usuario_Mochila_idx` (`Mochila_idMochila` ASC) VISIBLE,
  INDEX `fk_Usuario_Album1_idx` (`Album_idAlbum` ASC) VISIBLE,
  CONSTRAINT `fk_Usuario_Mochila`
    FOREIGN KEY (`Mochila_idMochila`)
    REFERENCES `BD_Distribuidos`.`Mochila` (`idMochila`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Usuario_Album1`
    FOREIGN KEY (`Album_idAlbum`)
    REFERENCES `BD_Distribuidos`.`Album` (`idAlbum`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `BD_Distribuidos`.`Carta`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `BD_Distribuidos`.`Carta` (
  `idCarta` INT NOT NULL AUTO_INCREMENT,
  `nome` VARCHAR(45) NOT NULL,
  `descricao` VARCHAR(200) NOT NULL,
  `allstar` TINYINT NOT NULL,
  PRIMARY KEY (`idCarta`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `BD_Distribuidos`.`Paradigma`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `BD_Distribuidos`.`Paradigma` (
  `idParadigma` INT NOT NULL AUTO_INCREMENT,
  `nome` VARCHAR(45) NULL,
  PRIMARY KEY (`idParadigma`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `BD_Distribuidos`.`Carta_has_Paradigma`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `BD_Distribuidos`.`Carta_has_Paradigma` (
  `Carta_idCarta` INT NOT NULL,
  `Paradigma_idParadigma` INT NOT NULL,
  PRIMARY KEY (`Carta_idCarta`, `Paradigma_idParadigma`),
  INDEX `fk_Carta_has_Paradigma_Paradigma1_idx` (`Paradigma_idParadigma` ASC) VISIBLE,
  INDEX `fk_Carta_has_Paradigma_Carta1_idx` (`Carta_idCarta` ASC) VISIBLE,
  CONSTRAINT `fk_Carta_has_Paradigma_Carta1`
    FOREIGN KEY (`Carta_idCarta`)
    REFERENCES `BD_Distribuidos`.`Carta` (`idCarta`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Carta_has_Paradigma_Paradigma1`
    FOREIGN KEY (`Paradigma_idParadigma`)
    REFERENCES `BD_Distribuidos`.`Paradigma` (`idParadigma`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `BD_Distribuidos`.`Mochila_has_Carta`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `BD_Distribuidos`.`Mochila_has_Carta` (
  `Mochila_idMochila` INT NOT NULL,
  `Carta_idCarta` INT NOT NULL,
  `numero` INT NOT NULL,
  PRIMARY KEY (`Mochila_idMochila`, `Carta_idCarta`),
  INDEX `fk_Mochila_has_Carta_Carta1_idx` (`Carta_idCarta` ASC) VISIBLE,
  INDEX `fk_Mochila_has_Carta_Mochila1_idx` (`Mochila_idMochila` ASC) VISIBLE,
  CONSTRAINT `fk_Mochila_has_Carta_Mochila1`
    FOREIGN KEY (`Mochila_idMochila`)
    REFERENCES `BD_Distribuidos`.`Mochila` (`idMochila`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Mochila_has_Carta_Carta1`
    FOREIGN KEY (`Carta_idCarta`)
    REFERENCES `BD_Distribuidos`.`Carta` (`idCarta`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `BD_Distribuidos`.`Slot`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `BD_Distribuidos`.`Slot` (
  `idSlot` INT NOT NULL AUTO_INCREMENT,
  `Carta_idCarta` INT NOT NULL,
  PRIMARY KEY (`idSlot`, `Carta_idCarta`),
  INDEX `fk_Slot_Carta1_idx` (`Carta_idCarta` ASC) VISIBLE,
  CONSTRAINT `fk_Slot_Carta1`
    FOREIGN KEY (`Carta_idCarta`)
    REFERENCES `BD_Distribuidos`.`Carta` (`idCarta`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `BD_Distribuidos`.`Leilao`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `BD_Distribuidos`.`Leilao` (
  `idLeilao` INT NOT NULL AUTO_INCREMENT,
  `Mochila_has_Carta_Mochila_idMochila` INT NOT NULL,
  `Mochila_has_Carta_Carta_idCarta` INT NOT NULL,
  `precoCarta` INT NOT NULL,
  PRIMARY KEY (`idLeilao`, `Mochila_has_Carta_Mochila_idMochila`, `Mochila_has_Carta_Carta_idCarta`),
  INDEX `fk_Leilao_Mochila_has_Carta1_idx` (`Mochila_has_Carta_Mochila_idMochila` ASC, `Mochila_has_Carta_Carta_idCarta` ASC) VISIBLE,
  CONSTRAINT `fk_Leilao_Mochila_has_Carta1`
    FOREIGN KEY (`Mochila_has_Carta_Mochila_idMochila` , `Mochila_has_Carta_Carta_idCarta`)
    REFERENCES `BD_Distribuidos`.`Mochila_has_Carta` (`Mochila_idMochila` , `Carta_idCarta`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `BD_Distribuidos`.`Album_has_Slot`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `BD_Distribuidos`.`Album_has_Slot` (
  `Album_idAlbum` INT NOT NULL,
  `Slot_idSlot` INT NOT NULL,
  `Slot_Carta_idCarta` INT NOT NULL,
  `is_ocupado` TINYINT NOT NULL,
  PRIMARY KEY (`Album_idAlbum`, `Slot_idSlot`, `Slot_Carta_idCarta`),
  INDEX `fk_Album_has_Slot_Slot1_idx` (`Slot_idSlot` ASC, `Slot_Carta_idCarta` ASC) VISIBLE,
  INDEX `fk_Album_has_Slot_Album1_idx` (`Album_idAlbum` ASC) VISIBLE,
  CONSTRAINT `fk_Album_has_Slot_Album1`
    FOREIGN KEY (`Album_idAlbum`)
    REFERENCES `BD_Distribuidos`.`Album` (`idAlbum`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Album_has_Slot_Slot1`
    FOREIGN KEY (`Slot_idSlot` , `Slot_Carta_idCarta`)
    REFERENCES `BD_Distribuidos`.`Slot` (`idSlot` , `Carta_idCarta`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;

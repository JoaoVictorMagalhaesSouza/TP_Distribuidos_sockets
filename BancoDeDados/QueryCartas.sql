INSERT INTO carta (nome,descricao,allstar) values
("Ruby","puts Hello World",False),
("Objective C","#import <Foundation/Foundation.h> int main(){ @autoreleasepool{ NSLog(@'Hello World'); } return 0 }",False),
("Go","package main import 'fmt' func main() { fmt.Println('hello world')}", True),
("Smalltalk","Transcript show: 'Hello, world!!!'",True),
("Kotlin","fun main() { println('Olá mundo!')}",False),
("Fortran","program hello !  print *, 'Hello, World!' end program hello",True),
("C#","Console.WriteLine('Hello World!');",False),
("C","#include <stdio.h> int main(){ printf('Hello World'); return 0}",True),
("C++","#include <iostream> int main() { std::cout << 'Hello World!'; return 0; }",False),
("PHP","<?php echo '<p>Olá Mundo</p>'; ?>",False),
("TypeScript","let message: string = 'Hello, World!'; console.log(message);",False),
("Elixir","iex(2)> 'hello' <> 'world'",False),
("LUA", "print('Hello World')",False),
("Haskell", "Prelude> putStrLn 'Hello World'",True),
("Erlang","-module(hello). -export([hello_world/0]). hello_world() -> io:fwrite('hello, world\n').",False),
("R","print('Hello World!')",False),
("Perl","use strict; use warnings; print('Hello World');",False),
("Scala","object Hello { def main(args: Array[String]) = { println('Hello, world') } }",False),
("Rust","fn main() { println!('Hello World'); }",False),
("Julia","print('Hello World')",False),
("ADA","with Text_IO; use Text_IO; procedure hello is begin Put_Line('Hello world!'); end hello;",True),
("Delphi","program HelloWorld; {$APPTYPE CONSOLE} begin WriteLn('Hello World'); end.",False),
("Visual Basic","Imports System Module Module1 Sub Main() Console.WriteLine('Hello World!') End Sub End Module",False),
("Python","print('Hello World')",True),
("Java","class Simple { public static void main(String args[]) { System.out.println('Hello World'); } }",True),
("JavaScript","console.log('Hello World')",True),
("COBOL","display 'Hello World'",False),
("Paskal","program Hello; begin writeln ('Hello World.'); end.",False),
("Algol","program HelloWorld; begin print 'Hello world'; end;",True),
("Dart","void main() { print('Hello World'); }",False)
;
select * from carta;
SELECT * from mochila_has_carta ;
SELECT * FROM leilao;
SELECT * from usuario;	
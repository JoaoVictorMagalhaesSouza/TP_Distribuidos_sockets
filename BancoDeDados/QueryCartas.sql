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
("R","print('Hello World!')",True)
;
SELECT * from carta
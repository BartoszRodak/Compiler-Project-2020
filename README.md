# Compiler project
## Course: Formal languages and translation technics
### on Wrocław University of Science and Technology

### Requirements and dependencies
* Python 3.7
* Sly library

### Example installation - Ubuntu
```
sudo apt update
sudo apt install python3.7
sudo apt install python3-pip
python3.7 -m pip install sly
```

## Use
Compiler may be run with `kompilator` command
```
./kompilator [source code file] [output file]
```
or directly running main Python script `compiler.py`
```
python3.7 src/compiler.py -i [source code file] -o [output file]
```

## Language and machine code
Source codes accepted by compiler are written is simple language given as a part of course materials. That language is described by grammar:
```
program       -> DECLARE declarations BEGIN commands END
              | BEGIN commands END

declarations  -> declarations, pidentifier
              | declarations, pidentifier(num:num)
              | pidentifier
              | pidentifier(num:num)

commands      -> commands command
              | command

command       -> identifier ASSIGN expression;
              | IF condition THEN commands ELSE commands ENDIF
              | IF condition THEN commands ENDIF
              | WHILE condition DO commands ENDWHILE
              | DO commands WHILE condition ENDDO
              | FOR pidentifier FROM value TO value DO commands ENDFOR
              | FOR pidentifier FROM value DOWNTO value DO commands ENDFOR
              | READ identifier;
              | WRITE value;

expression    -> value
              | value PLUS value
              | value MINUS value
              | value TIMES value
              | value DIV value
              | value MOD value

condition     -> value EQ value
              | value NEQ value
              | value LE value
              | value GE value
              | value LEQ value
              | value GEQ value

value         -> num
              | identifier

identifier    -> pidentifier
              | pidentifier(pidentifier)
              | pidentifier(num)
```
Standard file extension for source files is `.imp`

---

Result of compilation is expressed in pseudo machine code with given commands:

|Command|Description|
|-------|-----------|
|GET|read number from standard input and store in memory cell P(0), k = k + 1|
|PUT|display memory cell P(0) to standard output, k = k + 1|
|LOAD i| P(0) = P(i), k = k + 1|
|STORE i| P(i) = P(0), k = k + 1|
|LOADI i| P(0) = P(P(i)), k = k + 1|
|STOREI i| P(P(i)) = P(0), k = k + 1|
|ADD i| P(0) = P(0) + P(i), k = k + 1|
|SUB i| P(0) = P(0) - P(i), k = k + 1|
|SHIFT i| P(0) = floor(2^P(i) * P(0)), k = k + 1|
|INC|P(0) = P(0) + 1, k = k + 1|
|DEC|P(0) = P(0) - 1, k = k + 1|
|JUMP j| k = j|
|JPOS j| if P(0) > 0 then k = j else k = k + 1|
|JZERO j| if P(0) = 0 then k = j else k = k + 1|
|JNEG j| if P(0) < 0 then k = j else k = k + 1|
|HALT|stop execution|

Where `k` is program counter and memory `P` contains infinite number of arbitrary precision integer cells.

Standard file extension for result files is `.mr`

## Virtual machine
Example 'virtual machine', provided as a part of course, in `vm` directory. Build with Make. Standard version does not support arbitrarily big numbers required by machine code specification. Version `*-cln` supports arbitrary precision but depends on CLN library.

### More detail in `labor4.pdf` (in Polish)

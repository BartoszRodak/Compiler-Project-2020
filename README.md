# Projekt kompilator
## Języki formalne i techniki translacji 2020

## Wymagania i zależności
### Uruchomienie:
* Python 3
* Biblioteka Sly
### Instalacja 
Do instalacji biblioteki Sly wymagany jest dodatkowo menadżer pakietów PIP
### Przykładowa instalacja - Ubuntu
```
sudo apt update
sudo apt install python3 
sudo apt install python3-pip
pip3 install sly
```
## Korzystanie z programu
Program uruchamia się za pomocą komendy `kompilator` w głównym folderze projektu
```
./kompilator [plik wejściowy] [plik wyjściowy]
```
lub bezpośrednio odwołując się do skryptu w języku Python 
```
python3 src/compiler.py -i [plik wejściowy] -o [plik wyjściowy]
```
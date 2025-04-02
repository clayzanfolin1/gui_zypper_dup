# gui_zypper_dup
Ambiente gráfico para o comando zypper dup para atualizar o openSUSE Tumbleweed e Slowroll
E um programa e simples e visa ajudar quem tem dificuldade com terminal ou quer realizar a tarefa de um aforma mais simples gráfica.

O programa está sobre a licença: Licença Pública Geral GNU versão 2.0

E escrito em Python usei o Python 3.11 com PyQt5

Para que quiser usar é só instalar o Python311 caso já não tenha e a dependência python311-qt5

sudo zypper in  Python311 python311-qt5 python311-PyInstaller

Após isso no terminal na pasta onde baixou o  atualizacao.py
pyinstaller --onefile --windowed atualizacao1.0.py

Pronto será gerado o seu executável espero que ajude!

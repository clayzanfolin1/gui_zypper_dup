# gui_zypper_dup
Ambiente gráfico para o comando zypper dup para atualizar o openSUSE Tumbleweed e Slowroll
É um programa e simples e visa ajudar quem tem dificuldade com terminal ou quer realizar a tarefa de um aforma mais simples gráfica.

Ele executa para a atualizalçao do openSUSE com o comando:

zypper -v dup --force-resolution –no-allow-vendor-change –no-confirm

Também atualiza os aplicativos instalados do Flatpak

Para verificar se existe atualizações disponíveis é em modo usuário e após isso é libera os botões de atualização que precisa da senha do root para aplicar as atualizações.

O programa está sobre a licença: Licença Pública Geral GNU versão 2.0

E escrito em Python usei o Python 3.11 com PyQt5


Para que quiser usar é só instalar o Python311 caso já não tenha e a dependência python311-qt5

sudo zypper in  Python311 python311-qt5 python311-PyInstaller

Após isso no terminal na pasta onde baixou o  atualizacao.py
pyinstaller --onefile --windowed atualizacao1.0.py

Pronto será gerado o seu executável e espero que ajude!

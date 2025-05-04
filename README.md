# gui_zypper_dup
Ambiente gráfico para o comando zypper dup para atualizar o openSUSE Tumbleweed e Slowroll, já que não é recomendado atualizar pela opção da bandeja do sistema/área de notificação
É um programa simples e visa ajudar quem tem dificuldade com terminal ou quer realizar a tarefa de um aforma mais simples gráfica.

Ele executa a atualizalçao do openSUSE com o comando:

zypper -v dup --force-resolution –no-allow-vendor-change –no-confirm --auto-agree-with-licenses

Também atualiza os aplicativos instalados em Flatpak

Para verificar se existe atualizações disponíveis é em modo usuário e após isso é libera os botões de atualização que precisa da senha do root para aplicar as atualizações.

O programa está sobre a licença: Licença Pública Geral GNU versão 2.0

É escrito em Python, usei o Python 3.11 com PyQt5, assim tem a dependência do pacote: python311-qt5 ou no futuro python"versão do Python"-qt5


Para quem quiser usar é só instalar o Python311 caso já não tenha e a dependência python311-qt5

$ sudo zypper in  python311 python311-qt5 python311-PyInstaller ou via Yast >> Gerenciamento de software >> pesquisar por python311-qt5 e maraca para instalar e aceitar

Após isso no terminal na pasta onde baixou o atualizacao.py

$ pyinstaller --onefile --windowed atualizacao.py

Pronto será gerado o seu executável e espero que ajude!

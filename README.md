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

Pronto será gerado o seu executável!! 

Exemplo para adicionar no lançador de aplicativos do KDE:
Para colocar lançador de aplicativos, primeiro copie o arquivo resultante da compilação “atualizacao” para a pasta “bin” dentro da sua pasta de usuário, após isso clique com o botão direito no menu do lançador de aplicativos na barra de tarefas » Editar aplicativos… » clique em Sistema » Clique no botão Novo Item » Digite: Atualização e clique em “OK” » agora se quiser pode colocar uma descrição tipo: Atualização do Sistema e do Flatpak » em programa busque pelo arquivo “atualizacao” na pasta bin da sua pasta de usuário deixando assim /home/seu_usuário/bin/atualizacao » Agora pode escolher um ícone clicando no quadrado após nome e Descrição eu sugiro buscar update terá  ícones de atualização eu uso o “system-software-update” claque em “ok” » clique no botão salvar e pronto!


Espero que ajude!

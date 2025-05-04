import sys
import subprocess
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox,
    QInputDialog, QLineEdit, QTextEdit, QProgressBar, QDialog
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal


class AboutWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Sobre")
        self.setGeometry(200, 200, 300, 150)

        layout = QVBoxLayout()
        about_text = (
            "Desenvolvedor: Clayton Magalhães Zanfolin\n"
            "Licença: Licença Pública Geral GNU versão 2\n"
            "Versão: 1.0.1"
        )
        label = QLabel(about_text, self)
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

        btn_close = QPushButton("Fechar", self)
        btn_close.clicked.connect(self.close)
        layout.addWidget(btn_close)

        self.setLayout(layout)


class CommandThread(QThread):
    update_signal = pyqtSignal(str)
    progress_signal = pyqtSignal(int)

    def __init__(self, command, password=None):
        super().__init__()
        self.command = command
        self.password = password

    def run(self):
        try:
            process = subprocess.Popen(
                self.command,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            if self.password:
                process.stdin.write(f"{self.password}\n")
                process.stdin.flush()

            while True:
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break
                if output:
                    self.update_signal.emit(output.strip())

            stderr = process.stderr.read()
            if stderr:
                self.update_signal.emit(f"Erro: {stderr.strip()}")

            self.progress_signal.emit(100)
        except Exception as e:
            self.update_signal.emit(f"Erro ao executar o comando: {str(e)}")


class UpdaterApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.password = None

    def initUI(self):
        self.setWindowTitle("Atualizador de Sistema")
        self.setGeometry(100, 100, 1000, 520)

        layout = QVBoxLayout()

        self.label = QLabel("Clique em 'Verificar Atualizações' para começar.", self)
        layout.addWidget(self.label)

        self.text_updates = QTextEdit(self)
        self.text_updates.setReadOnly(True)
        self.text_updates.setMinimumHeight(200)
        self.text_updates.setFontFamily("Monospace")
        layout.addWidget(self.text_updates)

        self.progress_bar = QProgressBar(self)
        self.progress_bar.setAlignment(Qt.AlignCenter)
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)

        self.btn_check_updates = QPushButton("Verificar Atualizações", self)
        self.btn_check_updates.clicked.connect(self.check_updates)
        layout.addWidget(self.btn_check_updates)

        self.btn_update_flatpak = QPushButton("Atualizar Programa em Flatpak", self)
        self.btn_update_flatpak.clicked.connect(self.update_flatpak)
        self.btn_update_flatpak.setEnabled(False)
        layout.addWidget(self.btn_update_flatpak)

        self.btn_update_zypper = QPushButton("Atualizar o Sistema openSUSE", self)
        self.btn_update_zypper.clicked.connect(self.update_zypper)
        self.btn_update_zypper.setEnabled(False)
        layout.addWidget(self.btn_update_zypper)

        self.btn_about = QPushButton("Sobre", self)
        self.btn_about.clicked.connect(self.show_about)
        layout.addWidget(self.btn_about)

        self.setLayout(layout)

    def check_updates(self):
        self.btn_check_updates.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)

        self.label.setText("Verificando atualizações do Flatpak...")
        self.progress_bar.setValue(25)
        QApplication.processEvents()

        flatpak_updates = self.get_flatpak_updates()
        if flatpak_updates:
            self.text_updates.setPlainText("Atualizações do Flatpak:\n" + flatpak_updates)
            self.btn_update_flatpak.setEnabled(True)
        else:
            self.text_updates.append("Nenhuma atualização do Flatpak encontrada.")

        self.label.setText("Verificando atualizações do openSUSE...")
        self.progress_bar.setValue(50)
        QApplication.processEvents()

        zypper_updates = self.get_zypper_updates()
        if zypper_updates:
            self.text_updates.append("\nAtualizações do openSUSE:\n" + zypper_updates)
            self.btn_update_zypper.setEnabled(True)
        else:
            self.text_updates.append("Nenhuma atualização do openSUSE encontrada.")

        self.progress_bar.setValue(100)
        self.label.setText("Verificação de atualizações concluída.")
        self.btn_check_updates.setEnabled(True)

    def get_flatpak_updates(self):
        try:
            result = subprocess.run(
                ["flatpak", "remote-ls", "--updates", "--columns=app,arch,branch,origin,download"],
                capture_output=True, text=True
            )
            if result.returncode == 0:
                if result.stdout.strip():
                    # Processar a saída para melhor formatação
                    lines = result.stdout.split('\n')
                    if not lines:
                        return "Nenhuma atualização disponível para Flatpak."

                    # Criar cabeçalho formatado
                    header = "ID                             Ramo         Op       Remoto       Baixar"
                    separator = "-" * len(header)
                    formatted_lines = [header, separator]

                    # Adicionar linhas de pacotes
                    for line in lines:
                        if line.strip():
                            parts = line.split('\t')
                            if len(parts) >= 5:
                                app, arch, branch, origin, download = parts[:5]
                                formatted_line = f"{app[:30]:30} {branch[:12]:12} {arch[:8]:8} {origin[:12]:12} {download[:12]:12}"
                                formatted_lines.append(formatted_line)

                    return '\n'.join(formatted_lines)
                else:
                    return "Nenhuma atualização disponível para Flatpak."
            else:
                error_message = result.stderr.strip() if result.stderr else "Erro desconhecido."
                QMessageBox.warning(
                    self,
                    "Erro ao verificar Flatpak",
                    f"Falha ao verificar atualizações do Flatpak:\n{error_message}"
                )
                return None
        except FileNotFoundError:
            QMessageBox.warning(
                self,
                "Erro",
                "O comando 'flatpak' não foi encontrado. Certifique-se de que o Flatpak está instalado."
            )
            return None
        except Exception as e:
            QMessageBox.warning(
                self,
                "Erro",
                f"Erro ao verificar Flatpak: {str(e)}"
            )
            return None

    def get_zypper_updates(self):
        try:
            result = subprocess.run(
                ["zypper", "--no-refresh", "lu"],
                capture_output=True, text=True
            )
            if result.returncode == 0:
                output_lines = result.stdout.split('\n')
                formatted_output = []

                header_line = next((line for line in output_lines if line.startswith('S  |')), None)
                if header_line:
                    formatted_output.append(header_line)
                    separator_line = next((line for line in output_lines if line.startswith('---+')), '')
                    formatted_output.append(separator_line)

                    for line in output_lines:
                        if line and line[0] in ('v', ' ', 'p') and '|' in line:
                            formatted_output.append(line)

                return '\n'.join(formatted_output) if formatted_output else "Nenhuma atualização disponível."
            else:
                error_message = result.stderr.strip() if result.stderr else "Erro desconhecido."
                QMessageBox.warning(
                    self,
                    "Erro ao verificar atualizações",
                    f"Falha ao verificar atualizações do openSUSE:\n{error_message}"
                )
                return None
        except FileNotFoundError:
            QMessageBox.warning(
                self,
                "Erro",
                "O comando 'zypper' não foi encontrado. Certifique-se de que o zypper está instalado."
            )
            return None
        except Exception as e:
            QMessageBox.warning(self, "Erro", f"Erro ao verificar zypper: {str(e)}")
            return None

    def update_flatpak(self):
        self.password, ok = QInputDialog.getText(
            self, "Senha do Root", "Digite a senha do root:", QLineEdit.Password
        )
        if not ok or not self.password:
            QMessageBox.warning(self, "Erro", "Senha do root é necessária.")
            return

        self.btn_update_flatpak.setEnabled(False)
        self.btn_update_zypper.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)

        self.thread = CommandThread(["sudo", "-S", "flatpak", "update", "-y"], self.password)
        self.thread.update_signal.connect(self.update_output)
        self.thread.progress_signal.connect(self.update_progress)
        self.thread.start()

    def update_zypper(self):
        self.password, ok = QInputDialog.getText(
            self, "Senha do Root", "Digite a senha do root:", QLineEdit.Password
        )
        if not ok or not self.password:
            QMessageBox.warning(self, "Erro", "Senha do root é necessária.")
            return

        self.btn_update_flatpak.setEnabled(False)
        self.btn_update_zypper.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)

        self.thread = CommandThread(
            ["sudo", "-S", "zypper", "-v", "dup", "--force-resolution", "--no-allow-vendor-change", "--no-confirm", "--auto-agree-with-licenses"],
            self.password
        )
        self.thread.update_signal.connect(self.update_output)
        self.thread.progress_signal.connect(self.update_progress)
        self.thread.start()

    def update_output(self, message):
        self.text_updates.append(message)

    def update_progress(self, value):
        self.progress_bar.setValue(value)
        if value == 100:
            self.label.setText("Atualização concluída.")
            self.btn_update_flatpak.setEnabled("Atualizações do Flatpak" in self.text_updates.toPlainText())
            self.btn_update_zypper.setEnabled("Atualizações do openSUSE" in self.text_updates.toPlainText())

    def show_about(self):
        about_window = AboutWindow()
        about_window.exec_()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = UpdaterApp()
    window.show()
    sys.exit(app.exec_())

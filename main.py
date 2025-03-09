"""
author: Oscar Namicano

import yt_dlp

# Função para baixar o vídeo
def download_video(url):
    # Configurações do yt-dlp
    ydl_opts = {
        'format': 'best',  # Baixa o melhor formato de vídeo e áudio
        'outtmpl': '%(title)s.%(ext)s',  # Nome do arquivo de saída será o título do vídeo
    }

    try:
        # Baixar o vídeo com as opções fornecidas
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print(f"Iniciando o download do vídeo: {url}")
            ydl.download([url])  # Baixar o vídeo da URL
            print("Download concluído com sucesso!")
    except Exception as e:
        print(f"Erro ao baixar o vídeo: {e}")

# Pedir a URL do vídeo para o usuário
if __name__ == "__main__":
    video_url = input("Digite a URL do vídeo do YouTube: ")
    download_video(video_url)"""

import os
import threading
import yt_dlp
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.progressbar import ProgressBar
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.scrollview import ScrollView
from kivy.uix.recycleview import RecycleView
from kivy.core.window import Window
from kivy.uix.filechooser import FileChooserListView

# Ajuste de cor de fundo para o aplicativo
Window.clearcolor = (0.1, 0.1, 0.1, 1)  # Cor de fundo mais escura

# Função para baixar o vídeo ou o áudio
def download_media(url, is_audio, progress_callback, completion_callback, filename_callback):
    ydl_opts = {
        'format': 'bestaudio/best' if is_audio else 'best',  # Baixa o melhor formato de áudio ou vídeo
        'outtmpl': '%(title)s.%(ext)s',  # Nome do arquivo de saída será o título do vídeo
        'progress_hooks': [progress_callback],  # Atualiza o progresso
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print(f"Iniciando o download {'áudio' if is_audio else 'vídeo'}: {url}")
            result = ydl.download([url])  # Baixar o conteúdo da URL
            filename = ydl.prepare_filename(ydl.extract_info(url))
            print(f"Download concluído com sucesso! Arquivo salvo como: {filename}")
            filename_callback(filename)  # Passa o nome do arquivo para a função de callback
            completion_callback("Download concluído com sucesso!")
    except Exception as e:
        print(f"Erro ao baixar o conteúdo: {e}")
        completion_callback(f"Erro: {e}")

# Tela para inserir a URL e baixar o conteúdo (vídeo ou áudio)
class DownloadScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=20) #Widget principalmae do aplicativo onde todos os outros ficam

        # Cabeçalho com título
        header_layout = BoxLayout(size_hint_y=None, height=100)
        header_label = Label(text='Baixar Conteúdo', font_size=30, bold=True, color=(1, 1, 1, 1), size_hint=(None, None), size=(200, 100))
        header_layout.add_widget(header_label)
        self.layout.add_widget(header_layout)

        # Campo para inserir a URL do conteúdo
        self.url_input = TextInput(hint_text="Cole a URL do conteúdo", size_hint_y=None, height=40, background_normal='', background_active='', foreground_color=(0, 0, 0, 1), font_size=18)
        self.layout.add_widget(self.url_input)

        # Label para exibir mensagens
        self.message_label = Label(text="Aguardando URL", size_hint_y=None, height=40, color=(0.8, 0.8, 0.8, 1))
        self.layout.add_widget(self.message_label)

        # Barra de progresso
        self.progress_bar = ProgressBar(max=100, size_hint_y=None, height=20)
        self.layout.add_widget(self.progress_bar)

        # Botões "Baixar Vídeo" e "Baixar Áudio"
        buttons_layout = BoxLayout(size_hint_y=None, height=50, spacing=20)  # Layout horizontal para os botões
        self.download_video_button = Button(text="Baixar Vídeo", background_normal='', background_color=(0.3, 0.5, 0.8, 1), color=(1, 1, 1, 1), font_size=18)
        self.download_video_button.bind(on_press=self.start_video_download)
        buttons_layout.add_widget(self.download_video_button)

        self.download_audio_button = Button(text="Baixar Áudio", background_normal='', background_color=(0.3, 0.8, 0.3, 1), color=(1, 1, 1, 1), font_size=18)
        self.download_audio_button.bind(on_press=self.start_audio_download)
        buttons_layout.add_widget(self.download_audio_button)

        self.layout.add_widget(buttons_layout)

        # Botões "Sobre" e "Ver Downloads" na mesma linha
        info_buttons_layout = BoxLayout(size_hint_y=None, height=50, spacing=20)  # Layout horizontal para os botões
        self.view_downloads_button = Button(text="Ver Downloads", background_normal='', background_color=(0.3, 0.5, 0.8, 1), color=(1, 1, 1, 1), font_size=18)
        self.view_downloads_button.bind(on_press=self.show_downloads)
        info_buttons_layout.add_widget(self.view_downloads_button)

        self.about_button = Button(text="Sobre", background_normal='', background_color=(0.3, 0.5, 0.8, 1), color=(1, 1, 1, 1), font_size=18)
        self.about_button.bind(on_press=self.show_about_screen)
        info_buttons_layout.add_widget(self.about_button)

        self.layout.add_widget(info_buttons_layout)

        self.add_widget(self.layout)

    def start_video_download(self, instance):
        url = self.url_input.text
        if not url:
            self.message_label.text = "URL inválida!"
            return

        self.message_label.text = f"Iniciando o download do vídeo: {url}"

        # Iniciar o download em uma thread separada para vídeo
        download_thread = threading.Thread(target=download_media, args=(url, False, self.update_progress, self.on_download_complete, self.add_downloaded_file))
        download_thread.start()

    def start_audio_download(self, instance):
        url = self.url_input.text
        if not url:
            self.message_label.text = "URL inválida!"
            return

        self.message_label.text = f"Iniciando o download do áudio: {url}"

        # Iniciar o download em uma thread separada para áudio
        download_thread = threading.Thread(target=download_media, args=(url, True, self.update_progress, self.on_download_complete, self.add_downloaded_file))
        download_thread.start()

    def update_progress(self, progress_data):
        # Atualiza o progresso do download
        if progress_data['status'] == 'downloading':
            downloaded = progress_data.get('downloaded_bytes', 0)
            total = progress_data.get('total_bytes', 0)
            if total > 0:
                progress = (downloaded / total) * 100
                self.progress_bar.value = progress
            else:
                self.message_label.text = "Preparando o download..."

    def on_download_complete(self, message):
        self.message_label.text = message

    def add_downloaded_file(self, filename):
        # Adiciona o arquivo à lista de downloads
        app = App.get_running_app()
        app.downloaded_files.append(filename)

    def show_downloads(self, instance):
        # Troca para a tela de downloads
        self.manager.current = "downloads"

    def show_about_screen(self, instance):
        # Troca para a tela de informações sobre o app
        self.manager.current = "about"

# Tela para visualizar os downloads feitos (Agora um explorador de arquivos)
class DownloadsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=20)

        # Cabeçalho
        header_label = Label(text="Explorador de Downloads", font_size=30, bold=True, color=(1, 1, 1, 1), size_hint=(None, None), size=(200, 100))
        self.layout.add_widget(header_label)

        # FileChooser para visualizar e navegar pelos arquivos
        self.file_chooser = FileChooserListView(size_hint=(1, None), height=Window.height - 150)
        self.layout.add_widget(self.file_chooser)

        # Botão para voltar à tela de download
        self.back_button = Button(text="Voltar", size_hint_y=None, height=50, background_normal='', background_color=(0.3, 0.5, 0.8, 1), color=(1, 1, 1, 1), font_size=18)
        self.back_button.bind(on_press=self.go_back)
        self.layout.add_widget(self.back_button)

        self.add_widget(self.layout)

    def go_back(self, instance):
        # Volta para a tela de download
        self.manager.current = "download"

# Tela de "Sobre" - Informações sobre o app e a política de uso
class AboutScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=20)

        # Cabeçalho
        header_label = Label(text="Sobre o App", font_size=30, bold=True, color=(1, 1, 1, 1), size_hint=(None, None), size=(200, 100))
        self.layout.add_widget(header_label)

        # Informações sobre a versão e o programador
        version_label = Label(text="Versão: 1.0.0", font_size=20, color=(1, 1, 1, 1))
        self.layout.add_widget(version_label)

        developer_label = Label(text="Programador: Oscar Namicano", font_size=20, color=(1, 1, 1, 1))
        self.layout.add_widget(developer_label)

        # Adicionar política de uso e advertência sobre conteúdo protegido por direitos autorais
        legal_warning = Label(
            text=(
                "Política de Uso: O aplicativo permite o download de conteúdo de fontes públicas.\n"
                "No entanto, o usuário é responsável pelo uso legal do conteúdo baixado.\n"
                "Não é permitido baixar material protegido por direitos autorais sem a devida autorização."
            ),
            font_size=18,
            color=(1, 1, 1, 1)
        )
        self.layout.add_widget(legal_warning)

        # Botão para voltar à tela anterior
        back_button = Button(text="Voltar", size_hint_y=None, height=50, background_normal='', background_color=(0.3, 0.5, 0.8, 1), color=(1, 1, 1, 1), font_size=18)
        back_button.bind(on_press=self.go_back)
        self.layout.add_widget(back_button)

        self.add_widget(self.layout)

    def go_back(self, instance):
        self.manager.current = "download"

# Classe principal do app
class DownloadApp(App):
    def build(self):
        self.downloaded_files = []  # Lista para armazenar os arquivos baixados
        self.screen_manager = ScreenManager()

        # Adiciona as telas ao ScreenManager
        self.download_screen = DownloadScreen(name="download")
        self.downloads_screen = DownloadsScreen(name="downloads")
        self.about_screen = AboutScreen(name="about")

        self.screen_manager.add_widget(self.download_screen)
        self.screen_manager.add_widget(self.downloads_screen)
        self.screen_manager.add_widget(self.about_screen)

        return self.screen_manager

if __name__ == '__main__':
    DownloadApp().run()
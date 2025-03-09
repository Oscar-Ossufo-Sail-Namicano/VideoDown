"""
THIS IS THE SAME THING AS THE MAIN CODE BUT USING PYTUBE MODULE
I DESCONTINUED IT BECAUSE I WAS FACING SOME ERROR WHITH THE
PYTUBE MODULE I THINK THAT WITH A LITTLE BIT OF TIME, LIKE 5 MIINUTES,
THE ERROR CAN BE SOLVED

"""

import os
import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.progressbar import ProgressBar
from kivy.uix.image import Image
from kivy.uix.filechooser import FileChooserIconView
from pytube import YouTube
from kivy.uix.switch import Switch
from kivy.uix.screenmanager import ScreenManager, Screen

kivy.require('2.0.0')  # Specify your kivy version

class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Layout principal
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Campo para inserir URL
        self.url_input = TextInput(hint_text="Cole a URL do vídeo", size_hint_y=None, height=40)
        self.layout.add_widget(self.url_input)
        
        # Botão para baixar vídeo
        self.download_button = Button(text="Baixar Vídeo", size_hint_y=None, height=50)
        self.download_button.bind(on_press=self.iniciar_download)
        self.layout.add_widget(self.download_button)
        
        # Exibição de título, miniatura e duração
        self.title_label = Label(text="Título do vídeo:")
        self.layout.add_widget(self.title_label)
        
        self.thumbnail_image = Image(size_hint_y=None, height=200)
        self.layout.add_widget(self.thumbnail_image)
        
        self.duration_label = Label(text="Duração:")
        self.layout.add_widget(self.duration_label)
        
        # Barra de progresso
        self.progress_bar = ProgressBar(max=100, size_hint_y=None, height=20)
        self.layout.add_widget(self.progress_bar)
        
        # Adicionando layout à tela
        self.add_widget(self.layout)

    def iniciar_download(self, instance):
        url = self.url_input.text
        if not url:
            self.title_label.text = "URL inválida!"
            return
        
        try:
            yt = YouTube(url, on_progress_callback=self.atualizar_progresso)
            self.title_label.text = f"Título: {yt.title}"
            self.duration_label.text = f"Duração: {yt.length // 60}m {yt.length % 60}s"
            self.thumbnail_image.source = yt.thumbnail_url
            self.iniciar_download_video(yt)
        except Exception as e:
            self.title_label.text = "Erro ao buscar vídeo."
            print(str(e))

    def atualizar_progresso(self, stream, chunk, bytes_remaining):
        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_remaining
        progress = (bytes_downloaded / total_size) * 100
        self.progress_bar.value = progress

    def iniciar_download_video(self, yt):
        stream = yt.streams.filter(progressive=True, file_extension="mp4").first()
        download_dir = os.path.expanduser('~')  # Padrão no diretório inicial
        stream.download(download_dir)

        self.title_label.text = f"Download Concluído!"
        self.progress_bar.value = 100


class MyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainScreen(name='main'))
        return sm


if __name__ == '__main__':
    MyApp().run()

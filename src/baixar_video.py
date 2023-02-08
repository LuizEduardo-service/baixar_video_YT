from pytube import YouTube
from tkinter.filedialog import askdirectory
from tkinter import messagebox
import os
import re

class GeradorDeVideoYT():
    def __init__(self, link: str) -> None:
        self.link = link
        self.resolucao = ["720p", "480p", "360p", "240p", "144p"]

    def valida_link(self):
        pass

    def dados_do_video(self):
        video = YouTube(self.link)
        ttl_video = video.title
        resolucao = video.streams.all()
        import ipdb;ipdb.set_trace()
        print(resolucao)

    def baixar_video(self):
        video = YouTube(self.link)
        video.streams.get_by_resolution("480p")
        t=video.streams.get_by_itag(22)
        caminho = askdirectory()
        if caminho:
            try:
                t.download(caminho)
            except Exception as e:
                messagebox.showerror('Erro', 'Não foi Possivel realizar o Download do arquivo!!\nVerifique e tente novamente.')

    def baixar_audio(self):
        video = YouTube(self.link)
        ttl_video = video.title
        
        caminho = askdirectory()
        if caminho:
            try:
                audio = video.streams.filter(only_audio=True).first()
                down_audio = audio.download(caminho)
                base, ext = os.path.splitext(down_audio)
                novo_arquivo = base + '.mp3'
                os.rename(down_audio, novo_arquivo)
            except Exception as e:
                messagebox.showerror('Erro', 'Não foi Possivel realizar o Download do arquivo!!\nVerifique e tente novamente.')

                

GeradorDeVideoYT('https://www.youtube.com/watch?v=v_3DZYJmtfE').dados_do_video()
from pytube import YouTube
from tkinter.filedialog import askdirectory
from tkinter import messagebox
import os
import re

class GeradorDeVideoYT():
    def __init__(self) -> None:
        pass
    def valida_link(self):
        pass

    def dados_do_video(self, link):
        try:
            video = YouTube(link)
            ttl_video = video.title
            img = video.thumbnail_url
            resolucao: list = [stream.resolution for stream in video.streams.filter(progressive=True).all()]
            return {'titulo': ttl_video, 'imagem': img, 'resolucao': resolucao}
            
        
        except Exception as e:
            messagebox.showerror('Erro', 'Não foi possivel localizar as informações!\nVerifique e tente novamente.')

    def baixar_video(self,link: str, resolucao: str):
        video = YouTube(link)
        t= video.streams.get_by_resolution(resolucao)
        # t=video.streams.get_by_itag(22)
        caminho = askdirectory()
        if caminho:
            try:
                t.download(caminho)
                messagebox.showinfo('Erro', 'Download Realizado com Sucesso!')
            except Exception as e:
                messagebox.showerror('Erro', 'Não foi Possivel realizar o Download do arquivo!!\nVerifique e tente novamente.\n{e}')

    def baixar_audio(self, link: str):
        video = YouTube(link)        
        caminho = askdirectory()
        if caminho:
            try:
                audio = video.streams.filter(only_audio=True).first()
                down_audio = audio.download(caminho)
                base, ext = os.path.splitext(down_audio)
                novo_arquivo = base + '.mp3'
                os.rename(down_audio, novo_arquivo)
                messagebox.showinfo('Erro', 'Download Realizado com Sucesso!')
            except Exception as e:
                messagebox.showerror('Erro', 'Não foi Possivel realizar o Download do arquivo!!\nVerifique e tente novamente.')

                
if __name__ == '__main__':
    saida = GeradorDeVideoYT().dados_do_video('https://www.youtube.com/watch?v=YYhqjUaRLzo')
    print(saida)
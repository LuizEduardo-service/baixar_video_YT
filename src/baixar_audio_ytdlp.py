from yt_dlp import YoutubeDL
from tkinter.filedialog import askdirectory
from tkinter import messagebox
import os

class BaixadorAudioYTDLP:
    def __init__(self):
        self.opcoes_audio = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'quiet': True,
            'no_warnings': True
        }

    def obter_info_video(self, url):
        """Obtém informações básicas do vídeo"""
        try:
            with YoutubeDL(self.opcoes_audio) as ydl:
                info = ydl.extract_info(url, download=False)
                return {
                    'titulo': info.get('title', 'Sem título'),
                    'duracao': info.get('duration', 0),
                    'thumbnail': info.get('thumbnail', ''),
                    'autor': info.get('uploader', 'Desconhecido')
                }
        except Exception as e:
            messagebox.showerror('Erro', f'Erro ao obter informações do vídeo: {str(e)}')
            return None

    def baixar_audio(self, url):
        """Baixa o áudio do vídeo em MP3"""
        caminho = askdirectory(title="Escolha onde salvar o arquivo MP3")
        if not caminho:
            return

        # Atualiza as opções com o caminho de saída
        self.opcoes_audio['outtmpl'] = os.path.join(caminho, '%(title)s.%(ext)s')

        try:
            with YoutubeDL(self.opcoes_audio) as ydl:
                ydl.download([url])
            messagebox.showinfo('Sucesso', 'Download do áudio concluído com sucesso!')
        except Exception as e:
            messagebox.showerror('Erro', f'Erro ao baixar o áudio: {str(e)}')

# Exemplo de uso
if __name__ == '__main__':
    baixador = BaixadorAudioYTDLP()
    # Exemplo de como obter informações do vídeo
    info = baixador.obter_info_video('https://www.youtube.com/watch?v=eO9dUp5goWo')
    if info:
        print(f"Título: {info['titulo']}")
        print(f"Duração: {info['duracao']} segundos")
        print(f"Autor: {info['autor']}")
    
    # Para baixar o áudio
    baixador.baixar_audio('https://www.youtube.com/watch?v=eO9dUp5goWo') 
from yt_dlp import YoutubeDL
from tkinter.filedialog import askdirectory, askopenfilename
from tkinter import messagebox, Toplevel, Label, ttk
import os
import json
import threading

class JanelaProgresso:
    def __init__(self, titulo="Download em Progresso"):
        self.janela = Toplevel()
        self.janela.title(titulo)
        self.janela.geometry("400x150")
        self.janela.resizable(False, False)
        
        # Centraliza a janela
        self.janela.update_idletasks()
        width = self.janela.winfo_width()
        height = self.janela.winfo_height()
        x = (self.janela.winfo_screenwidth() // 2) - (width // 2)
        y = (self.janela.winfo_screenheight() // 2) - (height // 2)
        self.janela.geometry(f'{width}x{height}+{x}+{y}')
        
        # Configura o estilo
        self.janela.configure(bg='#f0f0f0')
        
        # Label para o status
        self.status_label = Label(
            self.janela,
            text="Preparando download...",
            font=("Arial", 10),
            bg='#f0f0f0'
        )
        self.status_label.pack(pady=10)
        
        # Label para o nome do arquivo
        self.arquivo_label = Label(
            self.janela,
            text="",
            font=("Arial", 9),
            bg='#f0f0f0',
            wraplength=380
        )
        self.arquivo_label.pack(pady=5)
        
        # Barra de progresso
        self.progresso = ttk.Progressbar(
            self.janela,
            orient="horizontal",
            length=350,
            mode="determinate"
        )
        self.progresso.pack(pady=10)
        
        # Label para porcentagem
        self.porcentagem_label = Label(
            self.janela,
            text="0%",
            font=("Arial", 9),
            bg='#f0f0f0'
        )
        self.porcentagem_label.pack(pady=5)
        
        # Label para velocidade
        self.velocidade_label = Label(
            self.janela,
            text="",
            font=("Arial", 9),
            bg='#f0f0f0'
        )
        self.velocidade_label.pack(pady=5)

    def atualizar_progresso(self, d):
        if d['status'] == 'downloading':
            # Atualiza o nome do arquivo
            if 'filename' in d:
                nome_arquivo = os.path.basename(d['filename'])
                self.arquivo_label.config(text=nome_arquivo)
            
            # Atualiza a barra de progresso
            if 'total_bytes' in d and 'downloaded_bytes' in d:
                total = d['total_bytes']
                baixado = d['downloaded_bytes']
                porcentagem = (baixado / total) * 100
                self.progresso['value'] = porcentagem
                self.porcentagem_label.config(text=f"{porcentagem:.1f}%")
            
            # Atualiza a velocidade
            if 'speed' in d:
                velocidade = d['speed']
                if velocidade:
                    velocidade_mb = velocidade / (1024 * 1024)
                    self.velocidade_label.config(text=f"Velocidade: {velocidade_mb:.1f} MB/s")
            
            # Atualiza o status
            self.status_label.config(text="Baixando...")
            
        elif d['status'] == 'finished':
            self.status_label.config(text="Download concluído! Processando...")
            self.progresso['value'] = 100
            self.porcentagem_label.config(text="100%")
            self.velocidade_label.config(text="")

    def fechar(self):
        self.janela.destroy()

class GeradorDeVideoYT:
    def __init__(self):
        self.config_file = 'config.json'
        self.ffmpeg_path = self._carregar_configuracao()
        self.janela_progresso = None
        
        self.opcoes_audio = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'quiet': True,
            'no_warnings': True,
            'progress_hooks': [self._hook_progresso]
        }
        
        if self.ffmpeg_path:
            self.opcoes_audio['ffmpeg_location'] = self.ffmpeg_path

    def _hook_progresso(self, d):
        """Hook para atualizar a barra de progresso"""
        if self.janela_progresso:
            self.janela_progresso.janela.after(0, self.janela_progresso.atualizar_progresso, d)

    def _carregar_configuracao(self):
        """Carrega a configuração do arquivo JSON"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                    return config.get('ffmpeg_path', '')
            return ''
        except:
            return ''

    def _salvar_configuracao(self, ffmpeg_path):
        """Salva a configuração no arquivo JSON"""
        try:
            config = {'ffmpeg_path': ffmpeg_path}
            with open(self.config_file, 'w') as f:
                json.dump(config, f)
        except Exception as e:
            messagebox.showerror('Erro', f'Erro ao salvar configuração: {str(e)}')

    def configurar_ffmpeg(self):
        """Permite ao usuário selecionar o executável do FFmpeg"""
        mensagem = """Por favor, selecione o arquivo ffmpeg.exe.
        
Se você ainda não tem o FFmpeg:
1. Baixe em: https://github.com/BtbN/FFmpeg-Builds/releases
2. Baixe o arquivo ffmpeg-master-latest-win64-gpl.zip
3. Extraia e selecione o ffmpeg.exe da pasta bin"""
        
        messagebox.showinfo('Configuração FFmpeg', mensagem)
        
        ffmpeg_path = askopenfilename(
            title="Selecione o arquivo ffmpeg.exe",
            filetypes=[("Executável FFmpeg", "ffmpeg.exe")]
        )
        
        if ffmpeg_path:
            self.ffmpeg_path = ffmpeg_path
            self._salvar_configuracao(ffmpeg_path)
            self.opcoes_audio['ffmpeg_location'] = ffmpeg_path
            messagebox.showinfo('Sucesso', 'FFmpeg configurado com sucesso!')
            return True
        return False

    def _download_thread(self, url, opcoes, tipo):
        """Thread para realizar o download"""
        try:
            with YoutubeDL(opcoes) as ydl:
                ydl.download([url])
            self.janela_progresso.janela.after(0, lambda: messagebox.showinfo('Sucesso', f'Download do {tipo} concluído com sucesso!'))
        except Exception as e:
            self.janela_progresso.janela.after(0, lambda: messagebox.showerror('Erro', f'Erro ao baixar o {tipo}: {str(e)}'))
        finally:
            self.janela_progresso.janela.after(1000, self.janela_progresso.fechar)

    def baixar_video(self, url, resolucao):
        """Baixa o vídeo na resolução especificada"""
        if not self.ffmpeg_path:
            if not self.configurar_ffmpeg():
                return
                
        caminho = askdirectory(title="Escolha onde salvar o vídeo")
        if not caminho:
            return

        opcoes_video = {
            'format': f'bestvideo[height<={resolucao[:-1]}]+bestaudio/best[height<={resolucao[:-1]}]',
            'outtmpl': os.path.join(caminho, '%(title)s.%(ext)s'),
            'quiet': True,
            'no_warnings': True,
            'ffmpeg_location': self.ffmpeg_path,
            'progress_hooks': [self._hook_progresso]
        }

        self.janela_progresso = JanelaProgresso("Download de Vídeo")
        thread = threading.Thread(target=self._download_thread, args=(url, opcoes_video, "vídeo"))
        thread.start()

    def baixar_audio(self, url):
        """Baixa o áudio do vídeo em MP3"""
        if not self.ffmpeg_path:
            if not self.configurar_ffmpeg():
                return
                
        caminho = askdirectory(title="Escolha onde salvar o arquivo MP3")
        if not caminho:
            return

        self.opcoes_audio['outtmpl'] = os.path.join(caminho, '%(title)s.%(ext)s')
        
        self.janela_progresso = JanelaProgresso("Download de Áudio")
        thread = threading.Thread(target=self._download_thread, args=(url, self.opcoes_audio, "áudio"))
        thread.start()

    def valida_link(self, url):
        """Valida se o link do YouTube é válido"""
        if not self.ffmpeg_path:
            if not self.configurar_ffmpeg():
                return False
                
        try:
            with YoutubeDL(self.opcoes_audio) as ydl:
                ydl.extract_info(url, download=False)
            return True
        except:
            return False

    def dados_do_video(self, url):
        """Obtém informações básicas do vídeo"""
        if not self.ffmpeg_path:
            if not self.configurar_ffmpeg():
                return None
                
        try:
            with YoutubeDL(self.opcoes_audio) as ydl:
                info = ydl.extract_info(url, download=False)
                return {
                    'titulo': info.get('title', 'Sem título'),
                    'imagem': info.get('thumbnail', ''),
                    'resolucao': ['720p', '480p', '360p']
                }
        except Exception as e:
            messagebox.showerror('Erro', f'Erro ao obter informações do vídeo: {str(e)}')
            return None

# Exemplo de uso
if __name__ == '__main__':
    baixador = GeradorDeVideoYT()
    
    # Se o FFmpeg não estiver configurado, pedirá para configurar
    if not baixador.ffmpeg_path:
        baixador.configurar_ffmpeg()
    
    # Exemplo de como obter informações do vídeo
    info = baixador.dados_do_video('https://www.youtube.com/watch?v=eO9dUp5goWo')
    if info:
        print(f"Título: {info['titulo']}")
        print(f"Thumbnail: {info['imagem']}")
        print(f"Resoluções disponíveis: {info['resolucao']}")
    
    # Para baixar o áudio
    # baixador.baixar_audio('https://www.youtube.com/watch?v=eO9dUp5goWo')
    
    # Para baixar o vídeo
    # baixador.baixar_video('https://www.youtube.com/watch?v=eO9dUp5goWo', '720p') 
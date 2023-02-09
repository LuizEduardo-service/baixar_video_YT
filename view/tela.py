import os
from tkinter import *
from tkinter import ttk, messagebox,PhotoImage
import tkinter
from urllib.request import urlretrieve
from PIL import Image, ImageTk

from src.baixar_video import GeradorDeVideoYT

root = Tk()
class TelaPrincial():

    def __init__(self) -> None:
        self.root = root
        self.imagens_layout()
        self.configuracao_tela()
        self.componentes_tela()
        self.root.mainloop()

    def configuracao_tela(self):
        self.config_tela()

    def centralizar_tela(self, largura, altura):
        param = []
        largura_tela = self.root.winfo_screenwidth()
        altura_tela = self.root.winfo_screenheight()

        posX = (largura_tela/2) - (largura/2)
        posY = (altura_tela/2) - (altura/2)

        param.append(largura);param.append(altura);param.append(posX);param.append(posY)
        return param

    def config_tela(self):
        self.root.title('Baixar video')
        pos = self.centralizar_tela(650, 400)
        self.root.geometry("%dx%d+%d+%d" % (pos[0], pos[1], pos[2], pos[3]))
        self.root.resizable(0,0)  # type: ignore
        
    def imagens_layout(self):
        self.tela_base =  PhotoImage(file=os.getcwd() + '\\tela_inicial.png')
        self.label_image = Label(self.root,image=self.tela_base)
        self.label_image.place(x=0,y=0)

    def componentes_tela(self):
        
        self.var_link = StringVar()
        self.txt_link = Entry(self.root,textvariable=self.var_link)
        self.btn_pesquisar = Button(self.root,text='>>',cursor='hand2', relief='flat',command=self.pesquisar_link_video)
        self.txt_link.place(x=154,y=55,width=430, height=31)
        self.btn_pesquisar.place(x=584,y=55,width=36, height=31)


        self.btn_video = Button(self.root,text='Baixar Video',cursor='hand2', relief='flat', font=('Popins 10 bold'),command=self.baixar_video)
        self.cb_resolucao = ttk.Combobox(self.root,values=[],cursor='hand2', font=('Popins 10 bold'))
        self.btn_audio = Button(self.root,text='Baixar Audio',cursor='hand2', relief='flat', font=('Popins 10 bold'), command=self.baixar_audio)

        self.btn_video.place(x=463,y=154,width=157, height=31)
        self.cb_resolucao.place(x=463,y=198,width=157, height=31)
        self.btn_audio.place(x=463,y=319,width=157, height=31)

        self.var_ttl_video = StringVar()
        self.titulo_video = Label(self.root, text='Titulo do video',textvariable=self.var_ttl_video)
        self.tumbnail = Label(self.root, image= '')

        self.titulo_video.place(x=44,y=115,width=576, height=31)
        self.tumbnail.place(x=44,y=154,width=397, height=196)

    def carregar_thubmail(self, link_imagem: str = ''):
        try:
            urlretrieve(link_imagem,"capa.png")
            imagem = Image.open("capa.png")

            resize_imagem = imagem.resize((397, 196))
            self.tkinter_imagem = ImageTk.PhotoImage(resize_imagem)
            return  self.tkinter_imagem
        except Exception as e:
            messagebox.showerror('erro', f'{e}')

    def pesquisar_link_video(self):
        if self.var_link.get() != "":
            self.cb_resolucao.select_clear()
            self.var_ttl_video.set('')
            self.tumbnail.configure(image='')
            dados_video =GeradorDeVideoYT()
            self.dados = dados_video.dados_do_video(self.var_link.get())
            self.var_ttl_video.set(str(self.dados['titulo']))
            imagem_ = self.carregar_thubmail(self.dados['imagem'])
            self.tumbnail.configure(image=imagem_)
            self.cb_resolucao.configure(values=self.dados['resolucao'])
        else:
            messagebox.showwarning('Atenção', 'Link do video em branco!!!')

    def baixar_video(self):
        if self.var_link.get() != "":
            dados_video =GeradorDeVideoYT()
            dados_video.baixar_video(self.var_link.get(),self.cb_resolucao.get())

    def baixar_audio(self):
        if self.var_link.get() != "":
            dados_video =GeradorDeVideoYT()
            dados_video.baixar_audio(self.var_link.get())


if __name__ == '__main__':
    TelaPrincial()
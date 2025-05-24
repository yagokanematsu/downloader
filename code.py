# Necessário ffmpeg
import tkinter as tk
from tkinter import messagebox
import os
import yt_dlp  # pip install yt_dlp
import subprocess
import platform
import winreg

COR_FUNDO = "#4a4a4a"
COR_TEXTO = "white"
COR_BOTAO = "#014f88"
COR_BOTAO_MOUSE = "#037cd5"

# Obtém o caminho da pasta de Downloads do usuário
def obter_pasta_downloads():
    if platform.system() == "Windows":
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, 
                            r'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders') as key:
            downloads = winreg.QueryValueEx(key, '{374DE290-123F-4565-9164-39C4925E467B}')[0]
    else:  # Linux, macOS e outros
        downloads = os.path.join(os.path.expanduser('~'), 'Downloads')
    
    return downloads

def estilizar_botao(botao):
    botao.config(bg=COR_BOTAO, fg=COR_TEXTO, font=("Arial", 12), relief="raised", bd=3)
    botao.bind("<Enter>", lambda x: botao.config(bg=COR_BOTAO_MOUSE))
    botao.bind("<Leave>", lambda x: botao.config(bg=COR_BOTAO))

def baixar_mp3():
    def download_mp3():
        link = url.get()
        pasta_downloads = obter_pasta_downloads()
        
        # Define as opções para salvar na pasta de Downloads
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(pasta_downloads, '%(title)s.%(ext)s'),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([link])
        
        tk.messagebox.showinfo("Download Concluído", f"MP3 baixado na pasta Downloads")

    nova_janela = tk.Toplevel(aba, bg=COR_FUNDO)
    nova_janela.title("Baixar MP3")
    nova_janela.geometry("350x200")

    tk.Label(nova_janela, text="Digite a URL do vídeo:", bg=COR_FUNDO, fg=COR_TEXTO, font=("Arial", 12)).pack(pady=10)
    url = tk.Entry(nova_janela, width=40)
    url.pack(pady=5)

    botao_baixar = tk.Button(nova_janela, text="Baixar MP3", command=download_mp3)
    estilizar_botao(botao_baixar)
    botao_baixar.pack(pady=10)

    botao_fechar = tk.Button(nova_janela, text="Fechar", command=nova_janela.destroy)
    estilizar_botao(botao_fechar)
    botao_fechar.pack(pady=5)

def baixar_mp4():
    def download_mp4():
        link = url.get()
        pasta_downloads = obter_pasta_downloads()
        
        with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
            info = ydl.extract_info(link, download=False)
            titulo = info.get('title', 'video')
            titulo = titulo.replace(' ', '_').replace('/', '_').replace('\\', '_')
        
        # Caminho para arquivos temporários na pasta de Downloads
        video_temp = os.path.join(pasta_downloads, "video45.mp4")
        audio_temp = os.path.join(pasta_downloads, "audio45.mp3")
        nome_final = os.path.join(pasta_downloads, f"{titulo}.mp4")
        
        # Baixar vídeo e áudio separadamente
        video_opts = {
            'format': 'bestvideo',
            'outtmpl': video_temp
        }
        audio_opts = {
            'format': 'bestaudio',
            'outtmpl': audio_temp
        }
        
        with yt_dlp.YoutubeDL(video_opts) as ydl:
            ydl.download([link])
        with yt_dlp.YoutubeDL(audio_opts) as ydl:
            ydl.download([link])
        
        # Combinar vídeo e áudio
        comando_ffmpeg = ["ffmpeg", "-i", video_temp, "-i", audio_temp, "-c:v", "copy", "-c:a", "aac", 
                          "-strict", "experimental", nome_final, "-y"]
        
        subprocess.run(comando_ffmpeg, shell=True)
        
        # Limpar arquivos temporários
        try:
            os.remove(video_temp)
            os.remove(audio_temp)
        except:
            pass
        
        tk.messagebox.showinfo("Download Concluído", f"MP4 baixado na pasta Downloads")
    
    nova_janela = tk.Toplevel(aba, bg=COR_FUNDO)
    nova_janela.title("Baixar MP4")
    nova_janela.geometry("350x200")

    tk.Label(nova_janela, text="Digite a URL do vídeo:", bg=COR_FUNDO, fg=COR_TEXTO, font=("Arial", 12)).pack(pady=10)
    url = tk.Entry(nova_janela, width=40)
    url.pack(pady=5)

    botao_baixar = tk.Button(nova_janela, text="Baixar MP4", command=download_mp4)
    estilizar_botao(botao_baixar)
    botao_baixar.pack(pady=10)

    botao_fechar = tk.Button(nova_janela, text="Fechar", command=nova_janela.destroy)
    estilizar_botao(botao_fechar)
    botao_fechar.pack(pady=5)

aba = tk.Tk()
aba.title("Downloader")
aba.geometry("400x400")
aba.config(bg=COR_FUNDO)

a = tk.Label(aba, text="Baixe vídeos ou áudios\nYoutube\nTwitter\nInstagram", bg=COR_FUNDO, fg=COR_TEXTO, font=("Arial", 14, "bold")).pack(pady=20)

botao1 = tk.Button(aba, text="Baixar MP3", command=baixar_mp3, width=20, height=2)
estilizar_botao(botao1)
botao1.pack(pady=10)

botao2 = tk.Button(aba, text="Baixar MP4", command=baixar_mp4, width=20, height=2)
estilizar_botao(botao2)
botao2.pack(pady=10)

botao3 = tk.Button(aba, text="Fechar", command=aba.destroy, width=20, height=2)
estilizar_botao(botao3)
botao3.pack(pady=10)

tk.mainloop()

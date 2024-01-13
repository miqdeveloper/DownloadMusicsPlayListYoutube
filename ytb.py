from pytube import Playlist, cli
import pytube
from moviepy.editor import *
import concurrent.futures
import os
import hashlib
import glob

diretorio = "downloads/"

def deletar_arquivos_duplicados(diretorio):
    hash_arquivo = {}
    for dirpath, dirnames, filenames in os.walk(diretorio):
        for nome_arquivo in filenames:
            caminho_arquivo = os.path.join(dirpath, nome_arquivo)
            hash = hashlib.md5(open(caminho_arquivo, 'rb').read()).hexdigest()
            if hash not in hash_arquivo:
                hash_arquivo[hash] = caminho_arquivo
            else:
                if os.path.getsize(caminho_arquivo) > os.path.getsize(hash_arquivo[hash]):
                    os.remove(hash_arquivo[hash])
                    hash_arquivo[hash] = caminho_arquivo
                else:
                    os.remove(caminho_arquivo)

def progress_callback(stream, chunk, bytes_remaining):
        size = stream.filesize
        progress = int(((size - bytes_remaining) / size) * 100)
        print(progress)

def baixar_e_converter_video(url_video):
    video = pytube.YouTube(url_video, use_oauth=True, allow_oauth_cache=True, on_progress_callback=progress_callback)        
    try:
        stream = video.streams.get_highest_resolution()
        
        stream.download(output_path=diretorio)
       
    except Exception as e:
        print(f"Ocorreu um erro ao baixar ou converter {url_video}: {e}")
        pass

def convert_to_mp3(diretorio):
    for dirpath, dirname, filenames in os.walk(diretorio):
        print(dirname)
    # video_clip = VideoFileClip(os.path.join('downloads', f'{video.title}.mp4'))
    # video_clip.close()
    # audio_clip = video_clip.audio
    # audio_clip.write_audiofile(os.path.join('downloads', f'{video.title}.mp3'))
    # audio_clip.close()
    
    

def baixar_e_converter_playlist(url):
    playlist = Playlist(url)
    with concurrent.futures.ThreadPoolExecutor(max_workers=7) as executor:
        executor.map(baixar_e_converter_video, playlist.video_urls)
        
def baixar_e_converter_playlists_de_arquivo(arquivo_txt):
    with open(arquivo_txt, 'r') as arquivo:
        urls = arquivo.readlines()
        for url in urls:
            baixar_e_converter_playlist(url)
            #os.system("rm -rf downloads/*.mp4")
            #os.system("del /Q  downloads/*.mp4")

def remove_file(diretorio):
    arquivos_mp4 = glob.glob(os.path.join(diretorio, '*.mp4'))
    for arquivo in arquivos_mp4:
        os.remove(arquivo)

    print("Arquivos .mp4 removidos com sucesso!")

baixar_e_converter_playlists_de_arquivo("links.txt")
# deletar_arquivos_duplicados(diretorio)
# remove_file(diretorio)

convert_to_mp3(diretorio)
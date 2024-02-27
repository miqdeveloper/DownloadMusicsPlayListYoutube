from pytube import Playlist, cli
import pytube
from pydub import AudioSegment 
import concurrent.futures
import os, os.path
import hashlib
import glob


diretorio = "downloads/"
musics_ = []
erros = []


if not os.path.exists(diretorio) or not os.path.exists("erros.txt"):
    os.system("mkdir downloads")
    os.system("echo > erros.txt")

def warite_erros(erros):
    with open("erros.txt", "w") as files:
        for erro_url in erros:
            files.write(f"{erro_url}\n")
            
def remover_caracteres(texto):
  """
  Remove os caracteres () e / de uma string.

  Argumentos:
    texto: A string original.

  Retorno:
    A string sem os caracteres () e /.
  """
  return ''.join(c for c in texto if c not in '()/')
        
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

def baixar_e_converter_video(url_video):
    video = pytube.YouTube(url_video, use_oauth=True, allow_oauth_cache=True, on_progress_callback=cli.on_progress)        
    try:
        s = video.streams.get_by_itag(18)
        name = f"{video.author} - {s.title}.mp4"
        name = remover_caracteres(name)
        s.download(filename=name, output_path=diretorio, max_retries=5)
        print(f"Baixado -> {name}")
        convert_to_mp3(diretorio, name)
    except Exception as e:
        print(f"\n\nOcorreu um erro no arquivo {s.title} \n{e}")
        erros.append(url_video)
        os.remove(f"{diretorio}{name}")
        # print(diretorio+s.title+".mp4")
        pass
    warite_erros(erros)

def convert_to_mp3(diretorio, filename):
    try:
        name, ext = os.path.splitext(filename)
        input_file = os.path.join(diretorio, filename)
        output_file = os.path.join(diretorio, f"{name}.mp3")    
        audio_file = AudioSegment.from_file(input_file, format="mp4")
        audio_file.export(output_file, format="mp3")
        os.remove(input_file)
        print("Conversão concluída!")
    except Exception as e:
        print(e)
        pass
    
def baixar_e_converter_playlist(playlist):
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor: 
        for mus in playlist:        
            exe = executor.submit(baixar_e_converter_video, mus)      
        # thread = threading.Thread(target=baixar_e_converter_video, args=(mus,), daemon=True)
        # thread.start()
        # Process(target=baixar_e_converter_video, args=(mus,)).start()
        
    
def baixar_e_converter_playlists_de_arquivo(arquivo_txt):
    with open(arquivo_txt, 'r') as arquivo:
        urls = arquivo.readlines()
        for url in urls:
            if "list" in url:
                playlist = Playlist(url)
                baixar_e_converter_playlist(playlist)
            else:
                musics_.append(url)
            baixar_e_converter_playlist(musics_)
                

baixar_e_converter_playlists_de_arquivo("links.txt")
deletar_arquivos_duplicados(diretorio)


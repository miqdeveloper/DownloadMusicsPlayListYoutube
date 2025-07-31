import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
from os import path
# Número de threads simultâneas (ajuste conforme seu sistema)
MAX_WORKERS = 8

def download_audio(link: str):
    """
    Executa yt-dlp para extrair áudio em MP3 de um link de playlist ou vídeo.
    """
    cmd = [
        "./yt-dlp",
        "-x",
        "--audio-format", "mp3",
        "--audio-quality", "5",
        "--yes-playlist",
        "--ignore-errors",
        "-o", "%(playlist_title)s/%(playlist_index)03d - %(title)s.%(ext)s",
        link
    ]
    try:
        # subprocess.run é recomendado para chamadas simples de subprocessos :contentReference[oaicite:2]{index=2}
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)  # Imprime a saída padrão do comando
        print(result.stdout)
        print(f"[SUCESSO] {link}")
    except subprocess.CalledProcessError as e:
        print(f"[ERRO]   {link}\n  Código de saída: {e.returncode}\n  stderr: {e.stderr}")

def main():
    # Lê todos os links do arquivo, ignorando linhas vazias e espaços em branco
    if not path.exists("links.txt"):
        with open("links.txt", "w", encoding="utf-8") as f:
            f.write("")
            f.close()
        
    with open("links.txt", "r", encoding="utf-8") as f:
        links = [line.strip() for line in f if line.strip()]

    if not links:
        print("Nenhum link encontrado em links.txt.")
        return

    # Cria um pool de threads para executar downloads em paralelo
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        # Submete todas as tarefas ao pool
        future_to_link = {executor.submit(download_audio, link): link for link in links}
        # Opcional: iterar conforme cada download é concluído
        for future in as_completed(future_to_link):
            print(f"[INICIANDO] {future_to_link[future]}")
            link = future_to_link[future]
            # Qualquer exceção dentro de download_audio já é tratada lá, 
            # mas podemos capturar erros não previstos aqui
            try:
                print(future.result())
            except Exception as exc:
                print(f"[EXCEÇÃO] {link} gerou uma exceção: {exc}")

if __name__ == "__main__":
    main()

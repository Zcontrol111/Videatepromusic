import yt_dlp
from termcolor import colored

def listar_calidades(url, formato):
    ydl_opts = {
        'format': 'bestaudio' if formato == 'mp3' else 'bestvideo+bestaudio',
        'noplaylist': True,
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=False)
        formatos = info_dict['formats']
        
        calidades = []
        for f in formatos:
            if formato == 'mp3' and f.get('acodec') != 'none' and 'abr' in f:
                calidades.append((f['format_id'], f['abr'], f['ext'], f.get('acodec', 'unknown')))
            elif formato == 'mp4' and f.get('vcodec') != 'none' and f.get('acodec') != 'none':
                calidades.append((f['format_id'], f['height'], f['ext'], f.get('vcodec', 'unknown'), f.get('acodec', 'unknown')))
        
        return calidades

def descargar_video_o_audio(url, formato, format_id):
    ydl_opts = {
        'format': format_id,
        'outtmpl': '%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }] if formato == 'mp3' else {},
        'ffmpeg_location': '/data/data/com.termux/files/usr/bin/ffmpeg',
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def main():
    print(colored("Bienvenido a Videate Pro Music", "cyan", attrs=["bold"]))
    url = input(colored("Ingrese la URL del video de YouTube: ", "yellow"))
    formato = input(colored("¿Desea descargar en formato mp3 o mp4?: ", "yellow")).strip().lower()
    
    if formato not in ['mp3', 'mp4']:
        print(colored("Formato no válido, solo mp3 o mp4", "red"))
        return
    
    calidades = listar_calidades(url, formato)
    
    if formato == 'mp3':
        print(colored("\nOpciones de calidad de audio disponibles:", "green"))
        for idx, (format_id, abr, ext, acodec) in enumerate(calidades):
            print(f"{idx + 1}. {format_id} - {abr} kbps, {ext}, {acodec}")
    elif formato == 'mp4':
        print(colored("\nOpciones de calidad de video disponibles:", "green"))
        for idx, (format_id, height, ext, vcodec, acodec) in enumerate(calidades):
            print(f"{idx + 1}. {format_id} - {height}p, {ext}, {vcodec}, {acodec}")
    
    eleccion = int(input(colored("\nSeleccione el número de la calidad que desea: ", "yellow")))
    
    if 1 <= eleccion <= len(calidades):
        format_id = calidades[eleccion - 1][0]
        descargar_video_o_audio(url, formato, format_id)
        print(colored("\nDescarga completada.", "green"))
    else:
        print(colored("Selección no válida", "red"))

if __name__ == "__main__":
    main()
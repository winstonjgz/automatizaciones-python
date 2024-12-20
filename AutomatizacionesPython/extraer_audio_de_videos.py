import os
from moviepy import VideoFileClip

def extract_audio(input_folder, output_folder, progress_callback=None):
    os.makedirs(output_folder, exist_ok=True)

    videos = [f for f in os.listdir(input_folder) if f.lower().endswith(('.mp4', '.avi', '.mov', '.mkv'))]
    total_videos = len(videos)

    for index, filename in enumerate(videos, 1):
        input_path = os.path.join(input_folder, filename)
        if os.path.isfile(input_path) :
            try:
                #Carga el archivo de video
                video_clip = VideoFileClip(input_path)
                #Obtener la ruta de salida
                audio_output_path = os.path.join(output_folder, os.path.splitext(filename)[0])+ '.mp3'
                #Extrae el audio y lo guarda
                video_clip.audio.write_audiofile(audio_output_path)
                #Se cierra el videoclip
                video_clip.close()
                print(f"Audio extraido: {audio_output_path}")

                #Llamar a la funcion de progreso
                if progress_callback:
                    progress_callback(index, total_videos, filename)

            except Exception as e:
                print(f"Error al procesar {filename}: {e}")


import cv2
import os
import glob

# Calculamos las rutas a partir de la ubicación de este script.
# Así funciona aunque ejecutes el archivo desde la raíz del proyecto en VS Code.
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(script_dir, '..'))

# Carpeta donde están los vídeos
videos_folder = os.path.join(project_root, 'data', 'raw_videos')
# Carpeta donde se guardarán los frames
output_base_folder = os.path.join(project_root, 'data', 'extracted_frames')

# Crear carpeta base de frames si no existe
os.makedirs(output_base_folder, exist_ok=True)

# Buscamos tanto .mp4 como .MP4 para que encuentre tu archivo real.
video_files = glob.glob(os.path.join(videos_folder, '*.mp4'))
video_files += glob.glob(os.path.join(videos_folder, '*.MP4'))
video_files = sorted(set(video_files))

if not video_files:
    print(f'No se encontraron vídeos en: {videos_folder}')
    print('Comprueba que la carpeta data/raw_videos contiene archivos .mp4 o .MP4')

for video_path in video_files:
    # Nombre del vídeo sin extensión
    video_name = os.path.splitext(os.path.basename(video_path))[0]
    output_folder = os.path.join(output_base_folder, video_name)
    
    # Crear carpeta específica para este vídeo
    os.makedirs(output_folder, exist_ok=True)
    
    cap = cv2.VideoCapture(video_path)
    frame_count = 0
    saved_count = 0
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        # Guardar 1 de cada 3 frames
        if frame_count % 3 == 0:
            frame_path = os.path.join(output_folder, f'frame_{frame_count:04d}.png')

            # Volvemos a usar cv2.imwrite y comprobamos si el guardado tuvo éxito.
            if cv2.imwrite(frame_path, frame):
                saved_count += 1
            else:
                print(f'No se pudo guardar el frame: {frame_path}')
        frame_count += 1
    
    cap.release()
    print(f'Vídeo "{video_name}": {saved_count} frames guardados en {output_folder}')

print("Extracción completada.")
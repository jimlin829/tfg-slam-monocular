import os
import subprocess

# --- 1. Definir rutas ---
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INPUT_IMAGES = os.path.join(PROJECT_ROOT, "data", "extracted_frames", "video_cvc")
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "data", "processed", "colmap_output")

# IMPORTANTE: Apuntamos a la carpeta '1' que fue la que funcionó en tu reconstrucción
SPARSE_DIR = os.path.join(OUTPUT_DIR, "sparse", "1")
# Carpeta donde se guardará todo el proceso denso
DENSE_DIR = os.path.join(OUTPUT_DIR, "dense")

os.makedirs(DENSE_DIR, exist_ok=True)

def run_command(cmd):
    print(f"Ejecutando: {' '.join(cmd)}")
    subprocess.run(cmd, check=True)

print("Iniciando reconstrucción densa (MVS)...")

# --- PASO A: Undistort (Preparar imágenes) ---
# Elimina la distorsión de la lente de la cámara para que la geometría sea perfecta
run_command([
    "colmap", "image_undistorter",
    "--image_path", INPUT_IMAGES,
    "--input_path", SPARSE_DIR,
    "--output_path", DENSE_DIR,
    "--output_type", "COLMAP"
])

# --- PASO B: Patch Match Stereo (Mapas de profundidad) ---
# Aquí es donde la GPU trabaja al 100% calculando la profundidad píxel a píxel
run_command([
    "colmap", "patch_match_stereo",
    "--workspace_path", DENSE_DIR,
    "--workspace_format", "COLMAP",
    "--PatchMatchStereo.geom_consistency", "false", # Desactiva esto para ganar puntos a costa de algo de ruido
    "--PatchMatchStereo.max_image_size", "1000"      # Reduce el tamaño si tu GPU sufre
])

# --- PASO C: Stereo Fusion (Fusión final) ---
# Une todos los mapas de profundidad en un solo archivo 3D
PLY_OUTPUT = os.path.join(DENSE_DIR, "fused.ply")
run_command([
    "colmap", "stereo_fusion",
    "--workspace_path", DENSE_DIR,
    "--workspace_format", "COLMAP",
    "--input_type", "geometric",
    "--output_path", PLY_OUTPUT,
    "--StereoFusion.min_num_pixels", "2",    # Muy importante: bajar de 3 a 2
    "--StereoFusion.max_reproj_error", "5.0" # Aumentamos el margen de error
])

print(f"\nProceso finalizado. Nube de puntos densa está en: {PLY_OUTPUT}")
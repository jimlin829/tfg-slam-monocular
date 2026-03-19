import os
import subprocess

# Configuración de rutas
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INPUT_IMAGES = os.path.join(PROJECT_ROOT, "data", "extracted_frames", "video_cvc")
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "data", "processed", "colmap_output")
DATABASE_PATH = os.path.join(OUTPUT_DIR, "database.db")
SPARSE_DIR = os.path.join(OUTPUT_DIR, "sparse")

os.makedirs(SPARSE_DIR, exist_ok=True)

def run_command(cmd):
    print(f"Ejecutando: {' '.join(cmd)}")
    subprocess.run(cmd, check=True)

# --- PASO 1: Extracción de características ---
run_command([
    "colmap", "feature_extractor",
    "--database_path", DATABASE_PATH,
    "--image_path", INPUT_IMAGES,
    "--ImageReader.single_camera", "1" # Asumimos que es la misma cámara siempre
])

# --- PASO 2: Emparejamiento Secuencial ---
run_command([
    "colmap", "sequential_matcher",
    "--database_path", DATABASE_PATH,
    "--SequentialMatching.overlap", "10" # Compara con los 10 frames anteriores/posteriores
])

# --- PASO 3: Reconstrucción (Mapper) ---
run_command([
    "colmap", "mapper",
    "--database_path", DATABASE_PATH,
    "--image_path", INPUT_IMAGES,
    "--output_path", SPARSE_DIR,
    "--Mapper.ba_global_function_tolerance", "0.000001" # Mayor precisión en el ajuste
])

print("Proceso finalizado.")
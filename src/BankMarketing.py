import os
from dotenv import load_dotenv

# Cargar variables desde .env antes de importar kaggle
load_dotenv()

# Usar la ruta del archivo JSON desde la variable de entorno
kaggle_config_dir = os.getenv("KAGGLE_CONFIG_DIR")

if not kaggle_config_dir:
    raise ValueError("KAGGLE_CONFIG_DIR no está definida en el archivo .env")

if not os.path.exists(os.path.join(kaggle_config_dir, 'kaggle.json')):
    raise FileNotFoundError(f"No se encontró kaggle.json en la ruta: {kaggle_config_dir}")

# Definir la variable de entorno para que kaggle la encuentre
os.environ['KAGGLE_CONFIG_DIR'] = kaggle_config_dir

# Importar kaggle *después* de haber definido la ruta
import kaggle

# Autenticación
kaggle.api.authenticate()

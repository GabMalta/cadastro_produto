from pathlib import Path
import os

# Caminho do diretório onde o script está localizado
BASEDIR = Path(__file__).resolve().parent

PATH_MODULE = os.path.join(BASEDIR, 'modules')

print(PATH_MODULE)
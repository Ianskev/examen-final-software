import sys
import os

# Añadir el directorio src al path de Python
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

# Importar la aplicación Flask desde controller
from src.controller import app

if __name__ == '__main__':
    app.run(debug=True)

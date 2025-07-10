import sys
import os

# Directorio src al path de Python
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

# Se creo este app.py para no hacer cd src/controller.py ahora simplemente hacemos:
# python app.py o python3 app.py
from src.controller import app

if __name__ == '__main__':
    app.run(debug=True)

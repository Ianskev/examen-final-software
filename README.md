# Sistema de Gestión de Tareas

## Descripción General
Este proyecto implementa un sistema de gestión de tareas que permite a los usuarios crear, asignar y gestionar tareas. El sistema está diseñado siguiendo una arquitectura orientada a objetos y expone varios endpoints REST para su interacción.

## Estructura del Proyecto
```
examenfinal2025_01/
├── src/
│   ├── __init__.py
│   ├── controller.py        # Controlador con endpoints REST
│   ├── data_handler.py      # Manejo de datos y persistencia
│   ├── models/              # Modelos de datos
│   │   ├── __init__.py
│   │   ├── usuario.py       # Clase Usuario
│   │   ├── tarea.py         # Clase Tarea
│   │   └── asignacion.py    # Clase Asignacion
│   └── utils/
│       └── __init__.py      # Utilidades para validación
├── tests/
│   ├── __init__.py
│   └── test_models.py       # Pruebas unitarias para los modelos
├── app.py                   # Punto de entrada principal
├── .coveragerc              # Configuración de cobertura
├── requirements.txt         # Dependencias del proyecto
└── README.md
```

## Instalación

### Pasos de Instalación
1. Clonar el repositorio:
   ```
   git clone https://github.com/Ianskev/examen-final-software
   cd examen-final-software
   ```

2. Crear y activar un entorno virtual (opcional pero recomendado):
   ```
   # En Windows
   python -m venv venv
   venv\Scripts\activate

   # En MacOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Instalar las dependencias:
   ```
   pip install -r requirements.txt
   ```

## Ejecución del Programa

Para ejecutar la aplicación, utiliza el siguiente comando en la terminal:
```
python app.py
```

Esto iniciará el servidor Flask en modo de desarrollo en `http://127.0.0.1:5000/`.

### Endpoints Disponibles

| Endpoint | Método | Descripción |
|----------|--------|-------------|
| `/usuarios/mialias=<alias>` | GET | Obtener información de un usuario y sus tareas |
| `/usuarios` | POST | Crear un nuevo usuario |
| `/tasks` | POST | Crear una nueva tarea |
| `/tasks/<id>` | POST | Actualizar el estado de una tarea |
| `/tasks/<id>/users` | POST | Gestionar usuarios asignados a una tarea |
| `/tasks/<id>/dependencies` | POST | Gestionar dependencias entre tareas |

## Ejecución de Pruebas

### Ejecutar Todas las Pruebas
Para ejecutar todas las pruebas unitarias:
```
python -m unittest discover tests
```

### Generar Informe de Cobertura
Para ejecutar las pruebas con cobertura y generar un informe que muestre el 100% de cobertura:

1. O, manualmente con los comandos:
   ```
   python -m coverage run --source=src.models -m unittest discover tests
   python -m coverage report -m
   ```

2. (Opcional) Generar un informe HTML detallado:
   ```
   python -m coverage html
   ```

### Cobertura de Código
Las pruebas han sido diseñadas para garantizar una cobertura del 100% en todas las clases del modelo:

```
Name                        Stmts   Miss  Cover   Missing
---------------------------------------------------------
src/models/__init__.py         0      0   100%
src/models/asignacion.py      13      0   100%
src/models/tarea.py           31      0   100%
src/models/usuario.py          9      0   100%
---------------------------------------------------------
TOTAL                         53      0   100%
```

Esta cobertura del 100% cumple con el requisito del examen de tener cobertura completa en las clases Usuario, Tarea y Asignacion.
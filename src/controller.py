from flask import Flask, jsonify, request
from data_handler import DataHandler

app = Flask(__name__)
data_handler = DataHandler()

class TaskController:
    def __init__(self, data_handler):
        self.data_handler = data_handler

@app.route('/usuarios/mialias=<alias>', methods=['GET'])
def get_usuario(alias):
    usuario = data_handler.get_usuario_por_alias(alias)
    if not usuario:
        return jsonify({"error": "Usuario no encontrado"}), 404
        
    return jsonify(usuario.to_dict()), 200

@app.route('/usuarios', methods=['POST'])
def crear_usuario():
    data = request.json
    
    if not data or 'contacto' not in data or 'nombre' not in data:
        return jsonify({"error": "Datos incompletos. Se requiere contacto y nombre"}), 422
        
    resultado, respuesta = data_handler.crear_usuario(data['contacto'], data['nombre'])
    
    if not resultado:
        return jsonify({"error": respuesta}), 422
        
    return jsonify({"message": "Usuario creado exitosamente", "usuario": respuesta.get_user_info()}), 201

@app.route('/tasks', methods=['POST'])
def crear_tarea():
    data = request.json
    
    if not data or 'nombre' not in data or 'descripcion' not in data or 'usuario' not in data or 'rol' not in data:
        return jsonify({"error": "Datos incompletos. Se requieren nombre, descripcion, usuario y rol"}), 422
        
    resultado, respuesta = data_handler.crear_tarea(data['nombre'], data['descripcion'], data['usuario'], data['rol'])
    
    if not resultado:
        return jsonify({"error": respuesta}), 422
        
    return jsonify({"message": "Tarea creada exitosamente", "id": respuesta.id}), 201

@app.route('/tasks/<task_id>', methods=['POST'])
def actualizar_estado_tarea(task_id):
    data = request.json
    
    if not data or 'estado' not in data:
        return jsonify({"error": "Datos incompletos. Se requiere estado"}), 422
        
    resultado, mensaje = data_handler.cambiar_estado_tarea(task_id, data['estado'])
    
    if not resultado:
        if mensaje == "Tarea no encontrada":
            return jsonify({"error": mensaje}), 404
        return jsonify({"error": mensaje}), 422
        
    return jsonify({"message": mensaje}), 200

@app.route('/tasks/<task_id>/users', methods=['POST'])
def gestionar_usuario_tarea(task_id):
    data = request.json
    
    if not data or 'usuario' not in data or 'rol' not in data or 'accion' not in data:
        return jsonify({"error": "Datos incompletos. Se requiere usuario, rol y accion"}), 422
        
    resultado, mensaje = data_handler.gestionar_usuario_en_tarea(
        task_id, data['usuario'], data['rol'], data['accion']
    )
    
    if not resultado:
        if mensaje in ["Tarea no encontrada", "Usuario no encontrado"]:
            return jsonify({"error": mensaje}), 404
        return jsonify({"error": mensaje}), 422
        
    return jsonify({"message": mensaje}), 200

@app.route('/tasks/<task_id>/dependencies', methods=['POST'])
def gestionar_dependencia(task_id):
    data = request.json
    
    if not data or 'dependencytaskid' not in data or 'accion' not in data:
        return jsonify({"error": "Datos incompletos. Se requiere dependencytaskid y accion"}), 422
        
    resultado, mensaje = data_handler.gestionar_dependencia(
        task_id, data['dependencytaskid'], data['accion']
    )
    
    if not resultado:
        if mensaje in ["Tarea no encontrada", "Tarea dependiente no encontrada"]:
            return jsonify({"error": mensaje}), 404
        return jsonify({"error": mensaje}), 422
        
    return jsonify({"message": mensaje}), 200

if __name__ == '__main__':
    app.run(debug=True)
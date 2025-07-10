import json
import datetime
from models.usuario import Usuario
from models.tarea import Tarea
from models.asignacion import Asignacion


class DataHandler:
    def __init__(self, filename='data.json'):
        self.filename = filename
        self.tareas = []
        self.usuarios = []
        self.load_data()

    def save_data(self):
        data = {
            'tareas': [self._serialize_tarea(tarea) for tarea in self.tareas],
            'usuarios': [self._serialize_usuario(usuario) for usuario in self.usuarios]
        }
        with open(self.filename, 'w') as f:
            json.dump(data, f)

    def load_data(self):
        try:
            with open(self.filename, 'r') as f:
                data = json.load(f)

                # Cargar usuarios primero
                self.usuarios = []
                for user_data in data.get('usuarios', []):
                    usuario = Usuario(user_data['alias'], user_data['nombre'])
                    self.usuarios.append(usuario)

                # Cargar tareas y reconstruir referencias
                self.tareas = []
                for task_data in data.get('tareas', []):
                    tarea = Tarea(
                        task_data['nombre'],
                        task_data['descripcion'],
                        datetime.datetime.strptime(task_data['fecha_esperada_fin'], "%Y-%m-%d %H:%M:%S") if task_data.get('fecha_esperada_fin') else None,
                        task_data['estado']
                    )
                    tarea.id = task_data['id']  # Usar el ID guardado
                    tarea.dependencias = task_data.get('dependencias', [])

                    # Reconstruir asignaciones
                    for asignacion_data in task_data.get('usuarios_asignados', []):
                        usuario = self.get_usuario_por_alias(asignacion_data['usuario'])
                        if usuario:
                            asignacion = Asignacion(usuario, asignacion_data['rol'])
                            asignacion.fechaAsignacion = datetime.datetime.strptime(
                                asignacion_data['fecha_asignacion'],
                                "%Y-%m-%d %H:%M:%S"
                            )
                            tarea.usuariosAsignados.append(asignacion)
                            usuario.tareasAsociadas.append(tarea)

                    self.tareas.append(tarea)

        except (FileNotFoundError, json.JSONDecodeError):
            self.tareas = []
            self.usuarios = []

    def _serialize_tarea(self, tarea):
        return {
            'id': tarea.id,
            'nombre': tarea.nombre,
            'descripcion': tarea.descripcion,
            'estado': tarea.estado,
            'fecha_esperada_fin': tarea.fechaEsperadaFin.strftime("%Y-%m-%d %H:%M:%S") if tarea.fechaEsperadaFin else None,
            'usuarios_asignados': [
                {
                    'usuario': asignacion.usuarioAsignado.alias,
                    'rol': asignacion.rol,
                    'fecha_asignacion': asignacion.fechaAsignacion.strftime("%Y-%m-%d %H:%M:%S")
                } for asignacion in tarea.usuariosAsignados
            ],
            'dependencias': tarea.dependencias
        }

    def _serialize_usuario(self, usuario):
        return {
            'alias': usuario.alias,
            'nombre': usuario.nombre
        }

    def get_usuario_por_alias(self, alias):
        for usuario in self.usuarios:
            if usuario.alias == alias:
                return usuario
        return None

    def get_tarea_por_id(self, task_id):
        for tarea in self.tareas:
            if tarea.id == task_id:
                return tarea
        return None

    def crear_usuario(self, alias, nombre):
        if self.get_usuario_por_alias(alias):
            return False, "El alias ya está en uso"

        nuevo_usuario = Usuario(alias, nombre)
        self.usuarios.append(nuevo_usuario)
        self.save_data()
        return True, nuevo_usuario

    def crear_tarea(self, nombre, descripcion, alias_usuario, rol):
        usuario = self.get_usuario_por_alias(alias_usuario)
        if not usuario:
            return False, "Usuario no encontrado"

        nueva_tarea = Tarea(nombre, descripcion)

        try:
            asignacion = Asignacion(usuario, rol)
            nueva_tarea.usuariosAsignados.append(asignacion)
            usuario.tareasAsociadas.append(nueva_tarea)

            self.tareas.append(nueva_tarea)
            self.save_data()
            return True, nueva_tarea
        except ValueError as e:
            return False, str(e)

    def cambiar_estado_tarea(self, task_id, nuevo_estado):
        tarea = self.get_tarea_por_id(task_id)
        if not tarea:
            return False, "Tarea no encontrada"

        resultado, mensaje = tarea.cambiar_estado(nuevo_estado)
        if resultado:
            self.save_data()
        return resultado, mensaje

    def gestionar_usuario_en_tarea(self, task_id, alias_usuario, rol, accion):
        tarea = self.get_tarea_por_id(task_id)
        if not tarea:
            return False, "Tarea no encontrada"

        usuario = self.get_usuario_por_alias(alias_usuario)
        if not usuario:
            return False, "Usuario no encontrado"

        if accion == "adicionar":
            # Verificar si el usuario ya está asignado
            for asignacion in tarea.usuariosAsignados:
                if asignacion.usuarioAsignado.alias == alias_usuario:
                    return False, "El usuario ya está asignado a esta tarea"

            try:
                nueva_asignacion = Asignacion(usuario, rol)
                tarea.usuariosAsignados.append(nueva_asignacion)
                usuario.tareasAsociadas.append(tarea)
                self.save_data()
                return True, "Usuario asignado correctamente"
            except ValueError as e:
                return False, str(e)

        elif accion == "remover":
            for i, asignacion in enumerate(tarea.usuariosAsignados):
                if asignacion.usuarioAsignado.alias == alias_usuario:
                    tarea.usuariosAsignados.pop(i)
                    if tarea in usuario.tareasAsociadas:
                        usuario.tareasAsociadas.remove(tarea)
                    self.save_data()
                    return True, "Usuario removido correctamente"
            return False, "El usuario no está asignado a esta tarea"
        
        return False, "Acción no válida. Debe ser 'adicionar' o 'remover'"

    def gestionar_dependencia(self, task_id, dependency_id, accion):
        tarea = self.get_tarea_por_id(task_id)
        if not tarea:
            return False, "Tarea no encontrada"

        dependency_tarea = self.get_tarea_por_id(dependency_id)
        if not dependency_tarea:
            return False, "Tarea dependiente no encontrada"

        if accion == "adicionar":
            resultado, mensaje = tarea.agregar_dependencia(dependency_id)
        elif accion == "remover":
            resultado, mensaje = tarea.remover_dependencia(dependency_id)
        else:
            return False, "Acción no válida. Debe ser 'adicionar' o 'remover'"

        if resultado:
            self.save_data()
        return resultado, mensaje
import datetime
import uuid

class Tarea:
    def __init__(self, nombre, descripcion, fecha_esperada_fin=None, estado="Nueva"):
        self.id = str(uuid.uuid4())
        self.nombre = nombre
        self.descripcion = descripcion
        self.estado = estado
        self.fechaEsperadaFin = fecha_esperada_fin or datetime.datetime.now() + datetime.timedelta(days=7)
        self.usuariosAsignados = []
        self.dependencias = []  # Lista de IDs de tareas de las que depende esta tarea

    def cambiar_estado(self, nuevo_estado):
        estados_validos = ["Nueva", "Progreso", "Finalizada"]
        
        if nuevo_estado not in estados_validos:
            return False, f"Estado inválido. Debe ser uno de: {', '.join(estados_validos)}"
        
        # No permitir cambiar de Finalizada a Nueva
        if self.estado == "Finalizada" and nuevo_estado == "Nueva":
            return False, "No se puede cambiar una tarea Finalizada a estado Nueva"
            
        self.estado = nuevo_estado
        return True, "Estado actualizado correctamente"
        
    def agregar_dependencia(self, tarea_id):
        if tarea_id not in self.dependencias and tarea_id != self.id:
            self.dependencias.append(tarea_id)
            return True, "Dependencia agregada correctamente"
        return False, "La dependencia ya existe o es la misma tarea"
        
    def remover_dependencia(self, tarea_id):
        if tarea_id in self.dependencias:
            self.dependencias.remove(tarea_id)
            return True, "Dependencia removida correctamente"
        return False, "La dependencia no existe en esta tarea"
    
    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "descripcion": self.descripcion,
            "estado": self.estado,
            "fecha_esperada_fin": self.fechaEsperadaFin.strftime("%Y-%m-%d %H:%M:%S") if self.fechaEsperadaFin else None,
            "usuarios_asignados": [asignacion.to_dict() for asignacion in self.usuariosAsignados],
            "dependencias": self.dependencias
        }
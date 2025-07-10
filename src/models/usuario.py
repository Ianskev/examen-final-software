class Usuario:
    def __init__(self, alias, nombre):
        self.alias = alias
        self.nombre = nombre
        self.tareasAsociadas = []

    def get_user_info(self):
        return {
            "alias": self.alias,
            "nombre": self.nombre,
            "tareas_asignadas": [tarea.id for tarea in self.tareasAsociadas]
        }
    
    def to_dict(self):
        return {
            "alias": self.alias,
            "nombre": self.nombre,
            "tareas_asignadas": [
                {
                    "id": tarea.id,
                    "nombre": tarea.nombre,
                    "estado": tarea.estado,
                    "descripcion": tarea.descripcion,
                    "fecha_esperada_fin": tarea.fechaEsperadaFin.strftime("%Y-%m-%d %H:%M:%S") if tarea.fechaEsperadaFin else None
                } for tarea in self.tareasAsociadas
            ]
        }
import datetime

class Asignacion:
    def __init__(self, usuario_asignado, rol):
        self.usuarioAsignado = usuario_asignado
        self.rol = rol
        self.fechaAsignacion = datetime.datetime.now()
        
        # Validar el rol
        roles_validos = ["analisis", "diseño", "programacion", "infra"]
        if rol not in roles_validos:
            raise ValueError(f"Rol inválido. Debe ser uno de: {', '.join(roles_validos)}")

    def get_assignment_details(self):
        return {
            "usuario": self.usuarioAsignado.alias,
            "rol": self.rol,
            "fecha_asignacion": self.fechaAsignacion.strftime("%Y-%m-%d %H:%M:%S")
        }
        
    def to_dict(self):
        return {
            "usuario": self.usuarioAsignado.alias,
            "rol": self.rol,
            "fecha_asignacion": self.fechaAsignacion.strftime("%Y-%m-%d %H:%M:%S")
        }
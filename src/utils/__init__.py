def validar_rol(rol):
    """Valida que el rol sea uno de los permitidos"""
    roles_validos = ["analisis", "diseño", "programacion", "infra"]
    return rol in roles_validos

def validar_estado_tarea(estado):
    """Valida que el estado de la tarea sea uno de los permitidos"""
    estados_validos = ["Nueva", "Progreso", "Finalizada"]
    return estado in estados_validos
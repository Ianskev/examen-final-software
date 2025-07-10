import sys
import os
import unittest
import datetime
from unittest.mock import MagicMock

# Agregar el directorio src al path para poder importar los módulos
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from models.usuario import Usuario
from models.tarea import Tarea
from models.asignacion import Asignacion

class TestUsuario(unittest.TestCase):
    """Pruebas para la clase Usuario"""

    def test_usuario_creation_success(self):
        """
        CASO DE ÉXITO:
        Prueba que un usuario se cree correctamente y 
        sus métodos devuelvan la información esperada
        """
        # Arrange
        alias = "testuser"
        nombre = "Test User"

        # Act
        usuario = Usuario(alias, nombre)

        # Assert
        self.assertEqual(usuario.alias, alias)
        self.assertEqual(usuario.nombre, nombre)
        self.assertEqual(usuario.tareasAsociadas, [])
        
        # Verificar el método get_user_info
        user_info = usuario.get_user_info()
        self.assertEqual(user_info["alias"], alias)
        self.assertEqual(user_info["nombre"], nombre)
        self.assertEqual(user_info["tareas_asignadas"], [])

    def test_to_dict_with_tasks(self):
        """
        CASO DE ERROR 1:
        Prueba el método to_dict cuando hay un error al convertir la fecha
        """
        # Arrange
        usuario = Usuario("testuser", "Test User")
        
        # Mock de una tarea con error en la fecha
        tarea_mock = MagicMock()
        tarea_mock.id = "123"
        tarea_mock.nombre = "Tarea Test"
        tarea_mock.estado = "Nueva"
        tarea_mock.descripcion = "Descripción"
        # Simular que fechaEsperadaFin es None
        tarea_mock.fechaEsperadaFin = None
        
        usuario.tareasAsociadas = [tarea_mock]
        
        # Act & Assert
        # Verificar que no se produce error cuando fechaEsperadaFin es None
        try:
            result = usuario.to_dict()
            self.assertIsNone(result["tareas_asignadas"][0]["fecha_esperada_fin"])
        except Exception as e:
            self.fail(f"to_dict() generó una excepción inesperada: {e}")


class TestTarea(unittest.TestCase):
    """Pruebas para la clase Tarea"""

    def test_cambiar_estado_success(self):
        """
        CASO DE ÉXITO:
        Prueba que el estado de una tarea se pueda cambiar correctamente
        """
        # Arrange
        tarea = Tarea("Tarea Test", "Descripción de prueba")
        
        # Act
        resultado, _ = tarea.cambiar_estado("Progreso")
        
        # Assert
        self.assertTrue(resultado)
        self.assertEqual(tarea.estado, "Progreso")

    def test_cambiar_estado_finalizada_a_nueva_error(self):
        """
        CASO DE ERROR 2:
        Prueba que una tarea no se pueda cambiar de Finalizada a Nueva
        """
        # Arrange
        tarea = Tarea("Tarea Test", "Descripción de prueba", estado="Finalizada")
        
        # Act
        resultado, mensaje = tarea.cambiar_estado("Nueva")
        
        # Assert
        self.assertFalse(resultado)
        self.assertEqual(mensaje, "No se puede cambiar una tarea Finalizada a estado Nueva")
        self.assertEqual(tarea.estado, "Finalizada")  # El estado no debe cambiar

    def test_cambiar_estado_invalido(self):
        """
        Prueba que se valide correctamente un estado inválido
        """
        # Arrange
        tarea = Tarea("Tarea Test", "Descripción de prueba")
        
        # Act
        resultado, mensaje = tarea.cambiar_estado("Estado Inválido")
        
        # Assert
        self.assertFalse(resultado)
        self.assertIn("Estado inválido", mensaje)
        self.assertEqual(tarea.estado, "Nueva")  # El estado no debe cambiar
    
    def test_agregar_dependencia_success(self):
        """
        Prueba que se pueda agregar una dependencia correctamente
        """
        # Arrange
        tarea = Tarea("Tarea Test", "Descripción de prueba")
        otra_tarea_id = "123456"
        
        # Act
        resultado, mensaje = tarea.agregar_dependencia(otra_tarea_id)
        
        # Assert
        self.assertTrue(resultado)
        self.assertIn(otra_tarea_id, tarea.dependencias)
        self.assertEqual(mensaje, "Dependencia agregada correctamente")
        
    def test_agregar_dependencia_existente(self):
        """
        Prueba que no se puede agregar una dependencia que ya existe
        """
        # Arrange
        tarea = Tarea("Tarea Test", "Descripción de prueba")
        otra_tarea_id = "123456"
        tarea.dependencias.append(otra_tarea_id)
        
        # Act
        resultado, mensaje = tarea.agregar_dependencia(otra_tarea_id)
        
        # Assert
        self.assertFalse(resultado)
        self.assertEqual(mensaje, "La dependencia ya existe o es la misma tarea")
        self.assertEqual(len(tarea.dependencias), 1)  # No debe haber duplicados
    
    def test_agregar_dependencia_misma_tarea(self):
        """
        Prueba que una tarea no puede depender de sí misma
        """
        # Arrange
        tarea = Tarea("Tarea Test", "Descripción de prueba")
        
        # Act
        resultado, mensaje = tarea.agregar_dependencia(tarea.id)
        
        # Assert
        self.assertFalse(resultado)
        self.assertEqual(mensaje, "La dependencia ya existe o es la misma tarea")
        self.assertEqual(len(tarea.dependencias), 0)  # No debe agregarse
    
    def test_remover_dependencia_success(self):
        """
        Prueba que se pueda remover una dependencia correctamente
        """
        # Arrange
        tarea = Tarea("Tarea Test", "Descripción de prueba")
        otra_tarea_id = "123456"
        tarea.dependencias.append(otra_tarea_id)
        
        # Act
        resultado, mensaje = tarea.remover_dependencia(otra_tarea_id)
        
        # Assert
        self.assertTrue(resultado)
        self.assertNotIn(otra_tarea_id, tarea.dependencias)
        self.assertEqual(mensaje, "Dependencia removida correctamente")
    
    def test_remover_dependencia_inexistente(self):
        """
        Prueba que no se puede remover una dependencia que no existe
        """
        # Arrange
        tarea = Tarea("Tarea Test", "Descripción de prueba")
        otra_tarea_id = "123456"
        
        # Act
        resultado, mensaje = tarea.remover_dependencia(otra_tarea_id)
        
        # Assert
        self.assertFalse(resultado)
        self.assertEqual(mensaje, "La dependencia no existe en esta tarea")
    
    def test_to_dict(self):
        """
        Prueba que el método to_dict devuelva la representación correcta de la tarea
        """
        # Arrange
        tarea = Tarea("Tarea Test", "Descripción de prueba")
        usuario_mock = MagicMock()
        usuario_mock.alias = "testuser"
        
        asignacion = MagicMock()
        asignacion.to_dict.return_value = {
            "usuario": "testuser",
            "rol": "programacion",
            "fecha_asignacion": "2023-01-01 12:00:00"
        }
        
        tarea.usuariosAsignados = [asignacion]
        tarea.dependencias = ["123", "456"]
        
        # Act
        resultado = tarea.to_dict()
        
        # Assert
        self.assertEqual(resultado["id"], tarea.id)
        self.assertEqual(resultado["nombre"], "Tarea Test")
        self.assertEqual(resultado["descripcion"], "Descripción de prueba")
        self.assertEqual(resultado["estado"], "Nueva")
        self.assertIsNotNone(resultado["fecha_esperada_fin"])
        self.assertEqual(len(resultado["usuarios_asignados"]), 1)
        self.assertEqual(len(resultado["dependencias"]), 2)


class TestAsignacion(unittest.TestCase):
    """Pruebas para la clase Asignacion"""

    def test_asignacion_creation_success(self):
        """
        CASO DE ÉXITO:
        Prueba que una asignación se cree correctamente con rol válido
        """
        # Arrange
        usuario_mock = MagicMock()
        usuario_mock.alias = "testuser"
        rol = "programacion"
        
        # Act
        asignacion = Asignacion(usuario_mock, rol)
        
        # Assert
        self.assertEqual(asignacion.usuarioAsignado, usuario_mock)
        self.assertEqual(asignacion.rol, rol)
        self.assertIsInstance(asignacion.fechaAsignacion, datetime.datetime)

    def test_asignacion_rol_invalido_error(self):
        """
        CASO DE ERROR 3:
        Prueba que una asignación no se pueda crear con un rol inválido
        """
        # Arrange
        usuario_mock = MagicMock()
        rol_invalido = "rol_inexistente"
        
        # Act & Assert
        with self.assertRaises(ValueError) as context:
            Asignacion(usuario_mock, rol_invalido)
        
        # Verificar el mensaje de error
        self.assertIn("Rol inválido", str(context.exception))
    
    def test_get_assignment_details(self):
        """
        Prueba que el método get_assignment_details devuelva la información correcta
        """
        # Arrange
        usuario_mock = MagicMock()
        usuario_mock.alias = "testuser"
        rol = "programacion"
        
        asignacion = Asignacion(usuario_mock, rol)
        fecha_str = asignacion.fechaAsignacion.strftime("%Y-%m-%d %H:%M:%S")
        
        # Act
        detalles = asignacion.get_assignment_details()
        
        # Assert
        self.assertEqual(detalles["usuario"], "testuser")
        self.assertEqual(detalles["rol"], rol)
        self.assertEqual(detalles["fecha_asignacion"], fecha_str)
    
    def test_to_dict(self):
        """
        Prueba que el método to_dict devuelva la representación correcta de la asignación
        """
        # Arrange
        usuario_mock = MagicMock()
        usuario_mock.alias = "testuser"
        rol = "programacion"
        
        asignacion = Asignacion(usuario_mock, rol)
        fecha_str = asignacion.fechaAsignacion.strftime("%Y-%m-%d %H:%M:%S")
        
        # Act
        resultado = asignacion.to_dict()
        
        # Assert
        self.assertEqual(resultado["usuario"], "testuser")
        self.assertEqual(resultado["rol"], rol)
        self.assertEqual(resultado["fecha_asignacion"], fecha_str)


if __name__ == "__main__":
    unittest.main()

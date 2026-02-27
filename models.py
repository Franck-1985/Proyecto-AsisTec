import sqlite3
from datetime import datetime
import os

class Database:
    def __init__(self, db_name='asistencia.db'):
        # Crear directorio data si no existe
        data_dir = os.path.join(os.path.dirname(__file__), 'data')
        os.makedirs(data_dir, exist_ok=True)
        
        self.db_name = os.path.join(data_dir, db_name)
        self.init_database()
    
    def get_connection(self):
        """Obtener conexión a la base de datos"""
        conn = sqlite3.connect(self.db_name)
        conn.row_factory = sqlite3.Row  # Para acceder por nombre de columna
        return conn
    
    def init_database(self):
        """Inicializar tablas de la base de datos"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Tabla de estudiantes
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS estudiantes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                matricula TEXT UNIQUE NOT NULL,
                nombre TEXT NOT NULL,
                fecha_registro TEXT NOT NULL,
                activo INTEGER DEFAULT 1
            )
        ''')
        
        # Tabla de asistencias
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS asistencias (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                estudiante_id INTEGER NOT NULL,
                fecha TEXT NOT NULL,
                estado TEXT NOT NULL,
                hora_registro TEXT NOT NULL,
                FOREIGN KEY (estudiante_id) REFERENCES estudiantes (id),
                UNIQUE(estudiante_id, fecha)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def registrar_estudiante(self, matricula, nombre):
        """Registrar un nuevo estudiante"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            fecha_registro = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cursor.execute(
                "INSERT INTO estudiantes (matricula, nombre, fecha_registro) VALUES (?, ?, ?)",
                (matricula.upper(), nombre.upper(), fecha_registro)
            )
            conn.commit()
            return True, "✅ Estudiante registrado exitosamente"
        except sqlite3.IntegrityError:
            return False, "❌ Error: La matrícula ya existe"
        finally:
            conn.close()
    
    def obtener_estudiantes(self, solo_activos=True):
        """Obtener todos los estudiantes activos"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if solo_activos:
            cursor.execute("SELECT id, matricula, nombre FROM estudiantes WHERE activo = 1 ORDER BY nombre")
        else:
            cursor.execute("SELECT id, matricula, nombre FROM estudiantes ORDER BY nombre")
        
        estudiantes = cursor.fetchall()
        conn.close()
        return [dict(est) for est in estudiantes]
    
    def obtener_asistencias_hoy(self):
        """Obtener asistencias del día actual"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        fecha_hoy = datetime.now().strftime("%Y-%m-%d")
        cursor.execute('''
            SELECT e.id, e.matricula, e.nombre, a.estado
            FROM estudiantes e
            LEFT JOIN asistencias a ON e.id = a.estudiante_id AND a.fecha = ?
            WHERE e.activo = 1
            ORDER BY e.nombre
        ''', (fecha_hoy,))
        
        asistencias = cursor.fetchall()
        conn.close()
        return [dict(ast) for ast in asistencias]
    
    def registrar_asistencia(self, estudiante_id, estado):
        """Registrar asistencia de un estudiante"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            fecha = datetime.now().strftime("%Y-%m-%d")
            hora_registro = datetime.now().strftime("%H:%M:%S")
            
            cursor.execute('''
                INSERT OR REPLACE INTO asistencias (estudiante_id, fecha, estado, hora_registro)
                VALUES (?, ?, ?, ?)
            ''', (estudiante_id, fecha, estado, hora_registro))
            
            conn.commit()
            return True, f"✅ Asistencia registrada: {estado}"
        except Exception as e:
            return False, f"❌ Error: {str(e)}"
        finally:
            conn.close()
    
    def consultar_asistencias(self, fecha=None):
        """Consultar asistencias por fecha"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if fecha:
            cursor.execute('''
                SELECT e.matricula, e.nombre, a.fecha, a.estado, a.hora_registro
                FROM asistencias a
                JOIN estudiantes e ON a.estudiante_id = e.id
                WHERE a.fecha = ?
                ORDER BY e.nombre
            ''', (fecha,))
        else:
            cursor.execute('''
                SELECT e.matricula, e.nombre, a.fecha, a.estado, a.hora_registro
                FROM asistencias a
                JOIN estudiantes e ON a.estudiante_id = e.id
                ORDER BY a.fecha DESC, e.nombre
                LIMIT 100
            ''')
        
        asistencias = cursor.fetchall()
        conn.close()
        return [dict(ast) for ast in asistencias]
    
    def obtener_estadisticas(self):
        """Obtener estadísticas de asistencia"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Total de estudiantes activos
        cursor.execute("SELECT COUNT(*) FROM estudiantes WHERE activo = 1")
        total_estudiantes = cursor.fetchone()[0]
        
        # Asistencia hoy
        fecha_hoy = datetime.now().strftime("%Y-%m-%d")
        cursor.execute(
            "SELECT COUNT(*) FROM asistencias WHERE fecha = ? AND estado = 'presente'",
            (fecha_hoy,)
        )
        presentes_hoy = cursor.fetchone()[0]
        
        # Asistencia esta semana
        cursor.execute('''
            SELECT COUNT(DISTINCT fecha) FROM asistencias 
            WHERE fecha >= date('now', '-7 days')
        ''')
        dias_con_asistencia = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            'total_estudiantes': total_estudiantes,
            'presentes_hoy': presentes_hoy,
            'ausentes_hoy': max(0, total_estudiantes - presentes_hoy),
            'dias_con_asistencia': dias_con_asistencia
        }
    
    def eliminar_estudiante(self, estudiante_id):
        """Eliminar (desactivar) un estudiante"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "UPDATE estudiantes SET activo = 0 WHERE id = ?",
                (estudiante_id,)
            )
            conn.commit()
            return True, "✅ Estudiante eliminado"
        except Exception as e:
            return False, f"❌ Error: {str(e)}"
        finally:
            conn.close()

from flask import Flask, render_template, request, redirect, url_for, flash
from models import Database
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'asistec_dev_key_2024')

# Configuración
PORT = int(os.environ.get('PORT', 5000))
DEBUG = os.environ.get('FLASK_ENV', 'development') == 'development'

# Inicializar base de datos
db = Database()

@app.route('/')
def index():
    """Página principal"""
    estadisticas = db.obtener_estadisticas()
    return render_template('index.html', estadisticas=estadisticas)

@app.route('/registrar_estudiante', methods=['GET', 'POST'])
def registrar_estudiante():
    """Registrar un nuevo estudiante"""
    if request.method == 'POST':
        matricula = request.form['matricula'].strip()
        nombre = request.form['nombre'].strip().upper()
        
        if matricula and nombre:
            success, message = db.registrar_estudiante(matricula, nombre)
            flash(message, 'success' if success else 'error')
            if success:
                return redirect(url_for('index'))
        else:
            flash('Por favor complete todos los campos', 'error')
    
    return render_template('registrar_estudiante.html')

@app.route('/tomar_asistencia', methods=['GET', 'POST'])
def tomar_asistencia():
    """Tomar asistencia del día"""
    if request.method == 'POST':
        estudiante_id = request.form['estudiante_id']
        estado = request.form['estado']
        
        success, message = db.registrar_asistencia(estudiante_id, estado)
        flash(message, 'success' if success else 'error')
        return redirect(url_for('tomar_asistencia'))
    
    estudiantes = db.obtener_estudiantes()
    fecha_actual = datetime.now().strftime("%d/%m/%Y")
    asistencias_hoy = db.obtener_asistencias_hoy()
    
    return render_template('tomar_asistencia.html', 
                         estudiantes=estudiantes,
                         asistencias_hoy=asistencias_hoy,
                         fecha_actual=fecha_actual)

@app.route('/consultar_asistencias', methods=['GET', 'POST'])
def consultar_asistencias():
    """Consultar asistencias registradas"""
    asistencias = []
    fecha_consulta = None
    
    if request.method == 'POST':
        fecha_consulta = request.form['fecha']
        asistencias = db.consultar_asistencias(fecha_consulta)
    else:
        asistencias = db.consultar_asistencias()
    
    return render_template('consultar_asistencias.html', 
                         asistencias=asistencias,
                         fecha_consulta=fecha_consulta)

@app.route('/estudiante/<int:id>/eliminar', methods=['POST'])
def eliminar_estudiante(id):
    """Eliminar un estudiante"""
    success, message = db.eliminar_estudiante(id)
    flash(message, 'success' if success else 'error')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT, debug=DEBUG)

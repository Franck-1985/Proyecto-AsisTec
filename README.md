# Proyecto-AsisTec
El proyecto AsisTec consiste en el desarrollo de una aplicación básica para el registro de asistencia, diseñada para facilitar el control de entradas y salidas de estudiantes de manera rápida y ordenada.    
# AsisTec - Sistema de Control de Asistencia

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.9+-green)
![Flask](https://img.shields.io/badge/flask-2.3.3-red)
![License](https://img.shields.io/badge/license-MIT-orange)

## 📋 Descripción

**AsisTec** es una aplicación web simple y eficiente para el registro y control de asistencia de estudiantes. Diseñada para reemplazar las listas de papel tradicionales, ofrece una solución digital rápida, confiable y fácil de usar.

### 🎯 Características Principales

- ✅ **Registro de Estudiantes**: Gestión completa con matrícula única
- ✅ **Toma de Asistencia**: Marcar presentes/ausentes con fecha automática
- ✅ **Consulta Histórica**: Visualizar asistencias por fecha
- ✅ **Estadísticas en Tiempo Real**: Dashboard con métricas importantes
- ✅ **Interfaz Responsive**: Funciona en computadoras, tablets y móviles
- ✅ **Base de Datos SQLite**: Persistencia de datos sin configuración compleja

## 🚀 Demo en Vivo

Puedes probar la aplicación aquí:
- **Render**: [https://asistec.onrender.com](https://asistec.onrender.com)
- **Codespaces**: Click en "Code" → "Codespaces" → "Create codespace"

## 📸 Capturas de Pantalla

| Página Principal | Toma de Asistencia |
|-----------------|-------------------|
| ![Inicio](https://via.placeholder.com/400x250) | ![Asistencia](https://via.placeholder.com/400x250) |

## 💻 Tecnologías Utilizadas

- **Backend**: Python 3.9 + Flask
- **Frontend**: HTML5, CSS3, JavaScript
- **Base de Datos**: SQLite3
- **Despliegue**: Render / GitHub Codespaces

## 🛠️ Instalación y Uso

### Opción 1: GitHub Codespaces (Recomendada)

1. Haz clic en el botón "Code" del repositorio
2. Selecciona la pestaña "Codespaces"
3. Click en "Create codespace on main"
4. Espera 2 minutos mientras se configura
5. ¡La aplicación se abrirá automáticamente!

### Opción 2: Instalación Local

```bash
# Clonar repositorio
git clone https://github.com/tu-usuario/AsisTec.git
cd AsisTec

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar aplicación
python app.py

# Abrir navegador en http://localhost:5000

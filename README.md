# 🤖 Py-LLM: AI Code Assistant

Este proyecto es un agente de IA construido con el SDK de Google GenAI y Python. Utiliza Function Calling para permitir que un modelo de lenguaje interactúe directamente con tu sistema de archivos de forma segura y controlada.

## 🌟 Características

- Capacidades del Agente:
  - Listar archivos y directorios.
  - Leer contenido de archivos de texto.
  - Escribir y crear archivos nuevos.
  - Ejecutar scripts de Python y capturar su salida real (STDOUT/STDERR).
- Seguridad (Sandboxing): El agente está restringido a operar exclusivamente dentro del directorio ./calculator. No puede acceder a archivos fuera de esta ruta gracias a la inyección forzada del working_directory.

---

## 🛠️ Configuración Inicial

1. Instalar dependencias:
   Asegúrate de tener uv instalado y ejecuta:
   uv sync

2. Variables de Entorno:
   Crea un archivo .env en la raíz del proyecto y añade tu API Key de Google AI Studio:
   GEMINI_API_KEY=tu_clave_de_api_aqui

3. Preparar el Sandbox:
   Crea la carpeta donde el agente tiene permiso para trabajar:
   mkdir calculator

---

## 📂 Estructura del Proyecto

.
├── main.py # Lógica principal y conexión con Gemini
├── prompts.py # Instrucciones del sistema (System Prompt)
├── .gitignore # Archivos excluidos de Git
├── functions/ # Herramientas (Tools) del agente
│ ├── call_function.py # Orquestador y despachador de funciones
│ ├── get_files_info.py # Herramienta: Listar archivos
│ ├── get_file_content.py# Herramienta: Leer archivos
│ ├── write_file.py # Herramienta: Crear/Editar archivos
│ └── run_python_file.py # Herramienta: Ejecutar Python
└── calculator/ # El "Sandbox" (área de trabajo del agente)

---

## 🚀 Ejemplos de Uso

Ejecuta el asistente pasando tu comando como argumento entre comillas:

- Listar archivos en el sandbox:
  uv run main.py "Muestra qué hay en la carpeta raíz"

- Leer un archivo específico con salida detallada:
  uv run main.py "Lee el contenido de main.py" --verbose

- Crear y probar código automáticamente:
  uv run main.py "Crea un script que sume 2+2 y ejecútalo"

---

## ⚠️ Cuotas y Límites (Error 429)

Si utilizas el Tier Gratuito, el modelo gemini-2.5-flash tiene un límite estricto de 20 peticiones diarias.

Si recibes un error RESOURCE_EXHAUSTED:

1. Espera al próximo ciclo de cuota (se reinicia diariamente).
2. O cambia el modelo en main.py a gemini-1.5-flash-002, que ofrece un límite mucho más amplio (1,500 peticiones diarias) y es ideal para desarrollo continuo.

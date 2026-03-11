"""
Run a python file
"""

import os
import subprocess


def run_python_file(working_directory, file_path, args=None):
    try:
        abs_working_dir = os.path.abspath(working_directory)
        target_path = os.path.normpath(os.path.join(abs_working_dir, file_path))

        if os.path.commonpath([abs_working_dir, target_path]) != abs_working_dir:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(target_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        # 4. Construir comando
        command = ["python", target_path]
        if args:
            command.extend(args)

        # 5. Ejecutar subproceso
        # Usamos cwd=abs_working_dir para que el script se ejecute "dentro" de la carpeta calculator
        result = subprocess.run(
            command,
            cwd=abs_working_dir,
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
        )

        # 6. Construir respuesta
        output_parts = []

        if result.returncode != 0:
            output_parts.append(f"Process exited with code {result.returncode}")

        if not result.stdout and not result.stderr:
            output_parts.append("No output produced")
        else:
            if result.stdout:
                output_parts.append(f"STDOUT:\n{result.stdout}")
            if result.stderr:
                output_parts.append(f"STDERR:\n{result.stderr}")

        return "\n".join(output_parts)

    except subprocess.TimeoutExpired:
        return "Error: executing Python file: process timed out after 30 seconds"
    except Exception as e:
        return f"Error: executing Python file: {e}"

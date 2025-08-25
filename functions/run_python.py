import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=[]):
    abs_working_dir = os.path.abspath(working_directory)
    target_dir = os.path.abspath(os.path.join(working_directory, file_path))
    if not target_dir.startswith(abs_working_dir):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(target_dir):
        return f'Error: File "{file_path}" not found.'
    if not target_dir.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'
    try:
        cmd = ["python3", file_path, *args]
        completed_process = subprocess.run(cmd, timeout=30, capture_output=True, cwd=abs_working_dir, text=True,)
        if not completed_process.stdout and not completed_process.stderr:
            return "No output produced."
        final_output = [f"STDOUT: {completed_process.stdout.strip()}", f"STDERR: {completed_process.stderr.strip()}"]
        if completed_process.returncode != 0:
            final_output.append(f"Process exited with code {completed_process.returncode}")
        return "\n".join(final_output)
    except Exception as e:
        return f"Error: executing Python file: {e}"

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file in the specified working directory with optional arguments.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the Python file to execute, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="Optional arguments to pass to the Python script.",
            ),
        },
    ),
)
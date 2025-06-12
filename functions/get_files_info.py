import os

def get_files_info(working_directory, directory=None):
    abs_working_directory = os.path.abspath(working_directory)
    target_directory = abs_working_directory
    if directory:
        target_directory = os.path.abspath(os.path.join(working_directory, directory))
    if not target_directory.startswith(abs_working_directory):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(target_directory):
        return f'Error: "{directory}" is not a directory'
    try:
        final = []
        contents = list(os.listdir(target_directory))
        for content in contents:
            filepath = os.path.join(target_directory, content)
            final.append(f"- {content}: file_size={os.path.getsize(filepath)} bytes, is_dir={os.path.isdir(filepath)}")
        return "\n".join(final)
    except Exception as e:
        return f"Error: {str(e)}"
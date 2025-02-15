import os
from pathlib import Path
from typing import List

def read_file(path: str) -> str:
    """
    Read and return the entire content of the file at the given path.
    
    Args:
        path (str): The file path.
        
    Returns:
        str: Contents of the file.
        
    Raises:
        FileNotFoundError: If the file does not exist.
        IOError: For other I/O errors.
    """
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def write_file(path: str, content: str, mode: str = "w") -> None:
    """
    Write the given content to a file at the specified path.
    
    Args:
        path (str): The file path.
        content (str): The content to write.
        mode (str, optional): File open mode; defaults to "w" (write). 
                              Use "a" to append.
        
    Raises:
        IOError: If an error occurs during writing.
    """
    with open(path, mode, encoding="utf-8") as f:
        f.write(content)

def list_files(directory: str) -> List[str]:
    """
    List the names of all files in the specified directory.
    
    Args:
        directory (str): The directory path.
        
    Returns:
        List[str]: A list of file names present in the directory.
        
    Raises:
        NotADirectoryError: If the provided path is not a directory.
    """
    p = Path(directory)
    if not p.is_dir():
        raise NotADirectoryError(f"{directory} is not a valid directory")
    return [file.name for file in p.iterdir() if file.is_file()]
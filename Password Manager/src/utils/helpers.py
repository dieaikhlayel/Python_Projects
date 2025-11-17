import os
import string
import random
from typing import Any, Dict
from pathlib import Path

def generate_random_string(length: int = 16) -> str:
    """Generate a random string for various purposes"""
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

def safe_delete_file(file_path: str) -> bool:
    """Safely delete a file with error handling"""
    try:
        path = Path(file_path)
        if path.exists():
            path.unlink()
        return True
    except Exception as e:
        print(f"Error deleting file {file_path}: {e}")
        return False

def get_file_size(file_path: str) -> int:
    """Get file size in bytes"""
    try:
        return Path(file_path).stat().st_size
    except Exception:
        return 0

def format_file_size(size_bytes: int) -> str:
    """Format file size in human-readable format"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} TB"

def deep_update_dict(target: Dict[Any, Any], update: Dict[Any, Any]) -> Dict[Any, Any]:
    """Recursively update a dictionary"""
    for key, value in update.items():
        if isinstance(value, dict) and key in target and isinstance(target[key], dict):
            deep_update_dict(target[key], value)
        else:
            target[key] = value
    return target

def ensure_directory(path: str) -> Path:
    """Ensure a directory exists, create if it doesn't"""
    path_obj = Path(path)
    path_obj.mkdir(parents=True, exist_ok=True)
    return path_obj
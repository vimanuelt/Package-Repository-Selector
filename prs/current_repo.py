# current_repo.py

import os
from prs.config_manager import ConfigManager

def read_file_content(file_path):
    """Read and return the content of a file."""
    try:
        with open(file_path, "r") as f:
            return f.read().strip()
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return None

def determine_current_repo():
    """Compare content of GhostBSD.conf with other GhostBSD.conf.* files to find the active repo."""
    repo_dir = "/usr/local/etc/pkg/repos/"
    current_conf = os.path.join(repo_dir, "GhostBSD.conf")

    if not os.path.exists(current_conf):
        print(f"{current_conf} does not exist.")
        return None

    current_content = read_file_content(current_conf)
    if not current_content:
        print(f"Failed to read content of {current_conf}.")
        return None

    for fname in os.listdir(repo_dir):
        if fname.startswith("GhostBSD.conf.") and fname != "GhostBSD.conf":
            other_path = os.path.join(repo_dir, fname)
            other_content = read_file_content(other_path)
            if current_content == other_content:
                return fname.replace("GhostBSD.conf.", "").capitalize()

    return "Default"

def write_to_config(current_repo):
    """Store the detected repo name in memory (no file)."""
    cfg = ConfigManager.get_instance()
    cfg.set("RepositoryCurrent", current_repo if current_repo else "Unknown")

if __name__ == "__main__":
    current = determine_current_repo()
    write_to_config(current)
    print(f"[current_repo.py] Current repo: {current}")


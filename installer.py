import os
import sys
import platform
import subprocess

def install_dependencies():
    """Install the dependencies from requirements.txt."""
    try:
        print("Installing dependencies...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("Dependencies installed successfully!")
    except subprocess.CalledProcessError:
        print("Error installing dependencies. Please check your environment and try again.")
        sys.exit(1)



def install():
    """Set up the 'rain' command."""
    project_dir = os.path.dirname(os.path.abspath(__file__))
    player_path = os.path.join(project_dir, "player.py")
    system = platform.system()

    install_dependencies()

    if system == "Windows":
        install_windows(player_path)
    elif system in ("Linux", "Darwin"):  # Darwin = macOS
        install_unix(player_path)
    else:
        print(f"Unsupported OS: {system}")
        sys.exit(1)


def install_windows(player_path):
    """Create a .bat file and add it to PATH on Windows."""
    bat_path = os.path.expanduser(r"~\rain.bat")
    with open(bat_path, "w") as bat_file:
        bat_file.write(f'@echo off\nstart "" pythonw "{player_path}" %*\nexit')

    print(f"Created {bat_path}")

    # Add to PATH
    print("Adding to PATH...")
    os.system(f'setx PATH "%PATH%;{os.path.dirname(bat_path)}"')
    print("Installation complete! You can now use 'rain' from the terminal.")


def install_unix(player_path):
    """Create a symbolic link in /usr/local/bin or add to PATH on Unix-based systems."""
    link_path = "/usr/local/bin/rain"
    try:
        os.symlink(player_path, link_path)
        os.chmod(player_path, 0o755)  # Ensure the script is executable
        print(f"Created symbolic link: {link_path}")
        print("Installation complete! You can now use 'rain' from the terminal.")
    except PermissionError:
        print("Permission denied: Run the installer with sudo.")
        sys.exit(1)
    except FileExistsError:
        print(f"{link_path} already exists. Overwriting...")
        os.remove(link_path)
        os.symlink(player_path, link_path)
        print(f"Symbolic link updated: {link_path}")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "install":
        install()
    else:
        print("Usage: python installer.py install")
import subprocess
import sys

# Dictionary mapping import names to pip install names
required_packages = {
    'argparse': 'argparse',
    'spotipy': 'spotipy',
    'importlib': 'importlib',
    'bs4': 'beautifulsoup4',  # Import name 'bs4', pip install name 'beautifulsoup4'
    'json': 'json',
    'pandas': 'pandas',
    'dotenv': 'python-dotenv',
    'requests': 'requests',
    'datetime': 'datetime',
    'os': 'os',
}

def install_missing_packages(packages):
    for import_name, install_name in packages.items():
        try:
            # Try to import the package
            __import__(import_name)
        except ImportError:
            # If the package is not installed, install it via pip
            print(f"Installing missing package: {install_name}")
            subprocess.check_call([sys.executable, "-m", "pip", "install", install_name])

if __name__ == "__main__":
    # Install missing packages
    install_missing_packages(required_packages)
    
    # Now the rest of your code can safely run, knowing the required packages are installed
    print("All required packages are installed and ready.")

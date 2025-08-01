import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.lcpi.main import app

def main():
    app()

if __name__ == "__main__":
    main()
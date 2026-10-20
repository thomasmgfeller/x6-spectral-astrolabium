"""Separate numerical-platform check; strict verify.py remains available."""
from verify import main

if __name__ == '__main__':
    main(portable=True)

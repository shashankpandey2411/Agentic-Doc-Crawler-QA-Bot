#!/usr/bin/env python3
import sys
from utils.cli.interface import main

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting...")
        sys.exit(0) 
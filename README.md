# TER_M1 Repository

## Overview
This repository contains LaTeX source files and Python scripts for the TER_M1 project. It includes:
- LaTeX files for generating the project report
- Python files for testing and validation
- Automated build and execution through `start.sh`

## Repository Structure
```
.
├── LaTeX/                        # LaTeX files for the report
│   ├── build/                    # Build artifacts for LaTeX compilation
│   ├── src/                      # Source files for the LaTeX report
│   ├── logs/                     # Logs from LaTeX compilation
│   ├── pdfs/                     # Generated PDF documents
│   └── run.py                    # Python script to automate LaTeX compilation, don't run directly
├── Python/                       # Python testing and utility scripts
│   ├── main.py                   # Main Python script for testing and validation
└── start.sh                      # Main entry point for all operations
```

## Prerequisites
- LaTeX distribution (TeX Live or MiKTeX)
- Python 3.x
- Bash shell

## Quick Start
All operations can be executed through the main entry script:
```bash
./start.sh
```

This script provides access to:
- Building the LaTeX report
```bash
./start.sh latex
```
- Running Python tests
```bash
./start.sh python
```

## Project Structure
- **LaTeX Files**: Generate the project report documentation
- **Python Files**: Handle testing, validation, and auxiliary tasks


## License
Licensed under [CC-BY-SA-4.0](LICENSE).

## Author
- Ivan Lejeune

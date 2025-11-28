# DCP Inspector (Python Version)

This is a Python conversion of the original Ruby-based `dcp_inspect` tool for inspecting and validating Digital Cinema Packages (DCP).

## Original Project Information
- Original author: Wolfgang Woehl
- Original project: https://github.com/wolfgangw/backports
- License: GNU General Public License v3.0

## Features

This Python version maintains the core functionality of the original Ruby tool:

- Finds and checks all DCPs in a filesystem tree
- Runs schema validation on all infrastructure files and DCSubtitle
- Checks and verifies signatures
- Reports detailed composition information
- Deep-inspects compositions with type consistency and completeness checks
- Checks presence and sanity of DCSubtitle resources
- Reports in detail all errors encountered

## Requirements

- Python 3.7+
- External tools:
  - asdcplib and its CLI tools (for MXF file inspection)
  - XML Schema Definition (XSD) files for validation (optional)

## Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Install asdcplib tools (for MXF inspection):
```bash
# On Ubuntu/Debian
sudo apt-get install asdcplib-tools

# On macOS with Homebrew
brew install asdcplib

# Or build from source: http://www.cinecert.com/asdcplib/
```

## Usage

```bash
python dcp_inspect.py [options] <path_to_dcp_directory>
```

### Options

- `--nh`, `--no-hash`: No asset hash checks
- `--hl`, `--hash-limit`: Limit asset hash checks to assets smaller than limit (e.g., 700KB, 50MB or 1GB)
- `--ni`, `--no-image-analysis`: No image analysis (not yet implemented)
- `--na`, `--no-audio-analysis`: No audio analysis
- `--no-schema`: Skip schema checks
- `-s`, `--as-asset-store`: Simulate asset store by merging all collected AM dictionaries
- `-l`, `--logfile`: Write full report to logfile at path
- `--la`, `--logfile-append`: Append full report to logfile at path
- `--autolog`: Write full report to $DCP_INSPECT_DIR
- `-L`, `--overwrite-logfile`: Overwrite logfile (default: do not overwrite if logfile exists)
- `-v`, `--verbosity`: Use quiet, errors, hints, siginfo, info, debug or cpl (comma-separated)
- `-d`, `--debug`: Run in debugger
- `-h`, `--help`: Display help

## Project Structure

```
dcp_inspect_py/
├── dcp_inspect.py          # Main application
├── requirements.txt        # Python dependencies
├── README.md             # This file
├── lib/                  # Core functionality modules
│   ├── xml_utils.py      # XML validation utilities
│   ├── crypto_utils.py   # Cryptographic utilities
│   └── mxf_utils.py      # MXF inspection utilities
└── constants/            # Constant definitions
    └── strings.py        # String constants
```

## Implementation Status

This is a partial conversion of the original Ruby code. Some features may not be fully implemented yet, including:

- Complete asset hash validation with CPL parsing
- Advanced image analysis
- Full certificate chain validation
- Some specific error handling cases

## License

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

See the original project for the complete license text.
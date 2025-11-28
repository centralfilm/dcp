# dcp_inspect Installation and Usage Guide

This package contains a compiled executable version of `dcp_inspect` - a Digital Cinema Package inspector and validator.

## Installation

To install the `dcp_inspect` executable on Ubuntu, run the installation script:

```bash
./install_dcp_inspect.sh
```

This will copy the executable to `/usr/local/bin/` and make it available system-wide.

## Manual Installation

Alternatively, you can manually install the executable:

```bash
sudo cp dist/dcp_inspect /usr/local/bin/
sudo chmod +x /usr/local/bin/dcp_inspect
```

## Usage

After installation, you can use `dcp_inspect` from anywhere in your system:

```bash
# Show help
dcp_inspect --help

# Inspect a DCP directory
dcp_inspect /path/to/dcp_directory

# Inspect without hash checks (faster)
dcp_inspect --nh /path/to/dcp_directory

# Limit hash checks to smaller files
dcp_inspect --hl 100MB /path/to/dcp_directory

# Write output to a log file
dcp_inspect -l report.log /path/to/dcp_directory
```

## Features

- Will find and check all DCPs in a filesystem tree
- Runs schema validation on all infrastructure files and DCSubtitle
- Checks and verifies signatures
- Reports detailed composition information
- Deep-inspects compositions with type consistency and completeness checks
- Checks presence and sanity of DCSubtitle resources
- Reports in detail all errors encountered

## About

This executable was created using PyInstaller from the Python version of the original Ruby dcp_inspect tool.
#!/bin/bash

# Script to install dcp_inspect executable on Ubuntu

set -e  # Exit on any error

echo "Installing dcp_inspect..."

# Copy the executable to a system directory
sudo cp /workspace/dcp_inspect_py/dist/dcp_inspect /usr/local/bin/
sudo chmod +x /usr/local/bin/dcp_inspect

echo "dcp_inspect has been installed successfully!"
echo "You can now run dcp_inspect from anywhere in your system."
echo ""
echo "Example usage:"
echo "  dcp_inspect --help"
echo "  dcp_inspect /path/to/dcp_directory"
"""
MXF (Material Exchange Format) utilities for DCP inspection
"""
import subprocess
import re
from pathlib import Path
from typing import Dict, List, Optional, Any


class MxfInspector:
    """Class for inspecting MXF files using external tools"""
    
    def __init__(self):
        # Check if asdcplib tools are available
        self.asdcplib_available = self._check_asdcplib_availability()
    
    def _check_asdcplib_availability(self) -> bool:
        """
        Check if asdcplib tools are available in the system
        
        Returns:
            True if asdcplib tools are available, False otherwise
        """
        try:
            result = subprocess.run(['asdcp-unwrap', '-V'], 
                                  capture_output=True, text=True, timeout=5)
            return result.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return False
    
    def get_asdcplib_version(self) -> Optional[tuple]:
        """
        Get version of asdcplib tools
        
        Returns:
            Tuple of (major, minor, patchlevel) or None if not available
        """
        if not self.asdcplib_available:
            return None
            
        try:
            result = subprocess.run(['asdcp-unwrap', '-V'], 
                                  capture_output=True, text=True, timeout=5)
            version_match = re.search(r'(\d+)\.(\d+)\.(\d+)', result.stdout)
            if version_match:
                major, minor, patchlevel = map(int, version_match.groups())
                return (major, minor, patchlevel)
        except Exception:
            pass
            
        return None
    
    def is_asdcplib_version_supported(self) -> bool:
        """
        Check if asdcplib version is supported
        
        Returns:
            True if version is supported, False otherwise
        """
        version = self.get_asdcplib_version()
        if not version:
            return False
            
        major, minor, patchlevel = version
        return major == 1  # As per original Ruby code
    
    def inspect_mxf(self, mxf_path: str) -> Optional[Dict[str, str]]:
        """
        Inspect MXF file using asdcplib tools
        
        Args:
            mxf_path: Path to MXF file
            
        Returns:
            Dictionary with inspection results or None if inspection failed
        """
        if not self.asdcplib_available:
            print("Warning: asdcplib tools not available, cannot inspect MXF files")
            return None
            
        try:
            # Run asdcp-unwrap to get MXF info
            result = subprocess.run(['asdcp-unwrap', '--info', mxf_path], 
                                  capture_output=True, text=True, timeout=30)
            
            if result.returncode != 0:
                # Check for specific error conditions
                if "SeekToRIP failed" in result.stderr:
                    return None
                elif "File open failure" in result.stderr:
                    return None
                elif "essence type is" in result.stdout:
                    # This is a special case mentioned in the original code
                    pass  # Continue processing
            
            # If there are errors but we still got some output, process it
            output = result.stdout
            
            if not output.strip():
                return None
            
            # Parse the output into key-value pairs
            # The output format is like: "Key: value"
            lines = output.split('\n')
            parsed_data = {}
            
            for line in lines:
                line = line.strip()
                if ':' in line:
                    key, value = line.split(':', 1)
                    key = key.strip()
                    value = value.strip()
                    parsed_data[key] = value
            
            # Determine essence type based on the first entry
            essence_type = self._determine_essence_type(parsed_data)
            if essence_type:
                parsed_data['EssenceType'] = essence_type
            
            return parsed_data
            
        except subprocess.TimeoutExpired:
            print(f"Timeout while inspecting MXF file: {mxf_path}")
            return None
        except Exception as e:
            print(f"Error inspecting MXF file {mxf_path}: {str(e)}")
            return None
    
    def _determine_essence_type(self, parsed_data: Dict[str, str]) -> Optional[str]:
        """
        Determine essence type from parsed MXF data
        
        Args:
            parsed_data: Dictionary with parsed MXF data
            
        Returns:
            Essence type string or None
        """
        # Check the first value in the parsed data for essence type
        first_value = next(iter(parsed_data.values()), "").lower()
        
        from constants.strings import MStr
        
        essence_types = {
            'stereoscopic_pictures': MStr.Stereoscopic_pictures,
            'pictures': MStr.Pictures,
            'mpeg2': MStr.Mpeg2,
            'audio': MStr.Audio,
            'atmos': MStr.Atmos,
            'timed_text': MStr.Timed_text
        }
        
        for key, value in essence_types.items():
            if key in first_value or value.lower() in first_value:
                return value
                
        return None


def create_pipe() -> Optional[str]:
    """
    Create a named pipe (FIFO) for processing
    
    Returns:
        Path to the created pipe or None if creation failed
    """
    import tempfile
    import os
    
    try:
        # Create a unique temporary filename
        temp_dir = "/tmp"
        pipe_name = f"dcp_inspect_{os.getpid()}_{hash(tempfile.mktemp()) & 0xffffffff:x}"
        pipe_path = os.path.join(temp_dir, pipe_name)
        
        # Create the FIFO
        os.mkfifo(pipe_path)
        return pipe_path
    except Exception as e:
        print(f"Error creating pipe: {str(e)}")
        return None


def remove_pipe(pipe_path: str) -> bool:
    """
    Remove a named pipe
    
    Args:
        pipe_path: Path to the pipe to remove
        
    Returns:
        True if removal was successful, False otherwise
    """
    try:
        os.unlink(pipe_path)
        return True
    except Exception as e:
        print(f"Error removing pipe {pipe_path}: {str(e)}")
        return False
"""
STL utilities for ASCII export to work with streamlit-stl
"""

import tempfile
import os
import numpy as np

# Try to import build123d
try:
    import build123d as b3d
    BUILD123D_AVAILABLE = True
except ImportError:
    BUILD123D_AVAILABLE = False
    print("⚠️ build123d not available. STL export will not work.")

def export_ascii_stl(part, filename):
    """
    Export a build123d Part to ASCII STL format for streamlit-stl compatibility
    
    Args:
        part: build123d Part object
        filename: Output filename
        
    Returns:
        bool: True if successful, False otherwise
    """
    if not BUILD123D_AVAILABLE:
        print("❌ build123d not available for STL export")
        return False
        
    try:
        # Handle different object types
        if hasattr(part, 'wrapped') or hasattr(part, 'export_step'):
            # This is a build123d Part object
            actual_part = part
            
            # Use build123d to export to binary first, then convert to ASCII
            with tempfile.NamedTemporaryFile(delete=False, suffix=".stl") as tmp_binary:
                b3d.export_stl(actual_part, tmp_binary.name)
                
                # Read binary STL and convert to ASCII
                try:
                    import trimesh
                    mesh = trimesh.load(tmp_binary.name)
                    mesh.export(filename, file_type='stl_ascii')
                    
                    # Verify it's ASCII format
                    with open(filename, 'rb') as f:
                        header = f.read(80)
                        if header.startswith(b'solid'):
                            return True
                        else:
                            print("Warning: Exported file is not in ASCII format")
                            return False
                except ImportError:
                    print("Cannot convert to ASCII without trimesh")
                    return False
                except Exception as e:
                    print(f"Trimesh conversion failed: {e}")
                    return False
                finally:
                    try:
                        os.unlink(tmp_binary.name)
                    except:
                        pass
        else:
            # This is an unexpected object type
            print(f"Unexpected object type: {type(part)}")
            return False
            
    except Exception as e:
        print(f"Failed to create STL for streamlit: {e}")
        return False

def export_stl(part, filename):
    """Export part to STL format"""
    try:
        return export_ascii_stl(part, filename)
    except Exception as e:
        print(f"STL export failed: {e}")
        return False

def export_step(part, filename):
    """Export part to STEP format"""
    try:
        # Handle different object types
        if hasattr(part, 'wrapped') or hasattr(part, 'export_step'):
            # This is a build123d Part object
            if BUILD123D_AVAILABLE:
                actual_part = part
                actual_part.export_step(filename)
                return True
            else:
                print("build123d object but build123d not available")
                return False
        else:
            print("STEP export not supported for this object type")
            return False
    except Exception as e:
        print(f"STEP export failed: {e}")
        return False

def create_stl_for_streamlit(part):
    """
    Create an ASCII STL file suitable for streamlit-stl viewer
    
    Args:
        part: build123d Part object
        
    Returns:
        str: Path to the ASCII STL file, or None if failed
    """
    if not BUILD123D_AVAILABLE:
        print("❌ Cannot create STL for streamlit: build123d not available")
        return None
        
    try:
        # Create temporary ASCII STL file
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".stl")
        temp_file.close()
        
        if export_ascii_stl(part, temp_file.name):
            return temp_file.name
        else:
            # Clean up if failed
            try:
                os.unlink(temp_file.name)
            except:
                pass
            return None
    except Exception as e:
        print(f"Failed to create STL for streamlit: {e}")
        return None

def verify_stl_format(filename):
    """
    Verify if an STL file is in ASCII format (compatible with streamlit-stl)
    
    Args:
        filename: Path to STL file
        
    Returns:
        bool: True if ASCII format, False if binary or invalid
    """
    try:
        with open(filename, 'rb') as f:
            header = f.read(80)
            return header.startswith(b'solid')
    except:
        return False

def check_dependencies():
    """Check if required dependencies are available"""
    issues = []
    
    if not BUILD123D_AVAILABLE:
        issues.append("❌ build123d not available - STL export and 3D preview will not work")
    
    return issues

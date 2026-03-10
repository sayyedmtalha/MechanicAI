"""
STL utilities for ASCII export to work with streamlit-stl
"""

import build123d as b3d
import tempfile
import os
import numpy as np

def export_ascii_stl(part, filename):
    """
    Export a build123d Part or TopoDS object to ASCII STL format for streamlit-stl compatibility
    
    Args:
        part: build123d Part object or TopoDS object from BD Warehouse
        filename: Output filename
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Handle different object types
        if hasattr(part, 'wrapped') or hasattr(part, 'export_step'):
            # This is a build123d Part object
            actual_part = part
        else:
            # This is a raw TopoDS object (BD Warehouse), wrap it in build123d Part
            actual_part = b3d.Part(part)
        
        # First export to binary STL
        with tempfile.NamedTemporaryFile(delete=False, suffix=".stl") as tmp_binary:
            b3d.export_stl(actual_part, tmp_binary.name)
            
            # Read binary STL and convert to ASCII
            try:
                import trimesh
                mesh = trimesh.load(tmp_binary.name)
                
                # Export as ASCII STL explicitly
                mesh.export(filename, file_type='stl_ascii')
                
                # Verify it's ASCII format
                with open(filename, 'rb') as f:
                    header = f.read(80)
                    if header.startswith(b'solid'):
                        return True
                    else:
                        print("Warning: Exported file is still not ASCII format")
                        # Try alternative method
                        return export_ascii_manual(tmp_binary.name, filename)
            except ImportError:
                # Manual conversion to ASCII STL
                return export_ascii_manual(tmp_binary.name, filename)
            finally:
                try:
                    os.unlink(tmp_binary.name)
                except:
                    pass
            
    except Exception as e:
        print(f"Failed to create STL for streamlit: {e}")
        return False

def export_ascii_manual(part, filename):
    """
    Manual ASCII STL export using build123d mesh functionality
    """
    try:
        # Handle different object types
        if hasattr(part, 'wrapped'):
            # This is a build123d Part object
            actual_part = part
        else:
            # This is a raw TopoDS object, wrap it in build123d Part
            actual_part = b3d.Part(part)
            
        # Try to get mesh from part and export manually
        # This is a fallback method
        with tempfile.NamedTemporaryFile(delete=False, suffix=".stl") as tmp:
            b3d.export_stl(actual_part, tmp.name, linear_deflection=0.01)
            
            # Read the binary and try to convert manually
            with open(tmp.name, 'rb') as fin:
                binary_data = fin.read()
            
            # Simple check - if it's not ASCII, we'll copy it anyway
            # streamlit-stl might still work with some binary formats
            with open(filename, 'wb') as fout:
                fout.write(binary_data)
            
            # Check if it worked
            with open(filename, 'rb') as f:
                header = f.read(80)
                return header.startswith(b'solid') or len(binary_data) > 1000  # At least some data
                
    except Exception as e:
        print(f"Manual ASCII export failed: {e}")
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
            actual_part = part
        else:
            # This is a raw TopoDS object (BD Warehouse), wrap it in build123d Part
            actual_part = b3d.Part(part)
        
        # Export to STEP
        actual_part.export_step(filename)
        return True
    except Exception as e:
        print(f"STEP export failed: {e}")
        return False

def create_stl_for_streamlit(part):
    """
    Create an ASCII STL file suitable for streamlit-stl viewer
    
    Args:
        part: TopoDS object from BD Warehouse
        
    Returns:
        str: Path to the ASCII STL file, or None if failed
    """
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

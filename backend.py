import streamlit as st
from smolagents import LiteLLMModel
from litellm import completion
import build123d as b3d
import math
import os

# Import gggears for professional gear generation
try:
    from gggears.src.py_gearworks.wrapper import (
        SpurGear, HelicalGear, BevelGear, CycloidGear,
        SpurRingGear, HelicalRingGear, InvoluteRack, HelicalRack
    )
    GGGEARS_AVAILABLE = True
except ImportError:
    GGGEARS_AVAILABLE = False

# Import bd_warehouse for professional fastener generation
try:
    from bd_warehouse.fastener import (
        HexHeadScrew, HexNut, PlainWasher, SocketHeadCapScrew,
        CounterSunkScrew, PanHeadScrew, ButtonHeadScrew,
        CheeseHeadScrew, DomedCapNut, ChamferedWasher,
        InternalToothLockWasher, SquareNut, SetScrew
    )
    from bd_warehouse.bearing import (
        Bearing, SingleRowAngularContactBallBearing, SingleRowCappedDeepGrooveBallBearing,
        SingleRowCylindricalRollerBearing, SingleRowDeepGrooveBallBearing,
        SingleRowTaperedRollerBearing
    )
    from bd_warehouse.pipe import Pipe, PipeSection
    from bd_warehouse.thread import (
        AcmeThread, IsoThread, MetricTrapezoidalThread,
        PlasticBottleThread, Thread, TrapezoidalThread
    )
    from bd_warehouse.flange import (
        BlindFlange, Flange, LappedFlange, SlipOnFlange,
        SocketWeldFlange, WeldNeckFlange
    )
    BD_WAREHOUSE_AVAILABLE = True
except ImportError as e:
    print(f"BD Warehouse import failed: {e}")
    BD_WAREHOUSE_AVAILABLE = False


# ==========================================
# GGGEARS PROFESSIONAL GEAR FUNCTIONS
# ==========================================

def create_spur_gear(module, num_teeth, face_width, bore_diameter=0, pressure_angle=20):
    """Create professional spur gear using gggears library"""
    if not GGGEARS_AVAILABLE:
        return None
    
    try:
        gear = SpurGear(
            number_of_teeth=num_teeth,
            module=module,
            pressure_angle=math.radians(pressure_angle),
            height=face_width
        )
        
        part = gear.build_part()
        
        if bore_diameter > 0:
            bore = b3d.Cylinder(radius=bore_diameter/2, height=face_width)
            part = part - bore
        
        return part
        
    except Exception as e:
        print(f"Spur gear creation failed: {e}")
        return None


def create_helical_gear(module, num_teeth, helix_angle_deg, face_width, bore_diameter=0, pressure_angle=20):
    """Create professional helical gear using gggears library"""
    if not GGGEARS_AVAILABLE:
        return None
    
    try:
        gear = HelicalGear(
            number_of_teeth=num_teeth,
            module=module,
            pressure_angle=math.radians(pressure_angle),
            helix_angle=math.radians(helix_angle_deg),
            height=face_width
        )
        
        part = gear.build_part()
        
        if bore_diameter > 0:
            bore = b3d.Cylinder(radius=bore_diameter/2, height=face_width)
            part = part - bore
        
        return part
        
    except Exception as e:
        print(f"Helical gear creation failed: {e}")
        return None


def create_bevel_gear(module, num_teeth, cone_angle_deg, face_width, bore_diameter=0, pressure_angle=20):
    """Create professional bevel gear using gggears library"""
    if not GGGEARS_AVAILABLE:
        return None
    
    try:
        gear = BevelGear(
            number_of_teeth=num_teeth,
            module=module,
            pressure_angle=math.radians(pressure_angle),
            cone_angle=math.radians(cone_angle_deg),
            height=face_width
        )
        
        part = gear.build_part()
        
        if bore_diameter > 0:
            bore = b3d.Cylinder(radius=bore_diameter/2, height=face_width)
            part = part - bore
        
        return part
        
    except Exception as e:
        print(f"Bevel gear creation failed: {e}")
        return None


def create_cycloid_gear(module, num_teeth, face_width, bore_diameter=0):
    """Create cycloid gear using gggears library"""
    if not GGGEARS_AVAILABLE:
        return None
    
    try:
        gear = CycloidGear(
            number_of_teeth=num_teeth,
            module=module,
            height=face_width
        )
        
        part = gear.build_part()
        
        if bore_diameter > 0:
            bore = b3d.Cylinder(radius=bore_diameter/2, height=face_width)
            part = part - bore
        
        return part
        
    except Exception as e:
        print(f"Cycloid gear creation failed: {e}")
        return None


def create_spur_ring_gear(module, num_teeth, face_width, bore_diameter=0, pressure_angle=20):
    """Create spur ring gear (internal teeth) using gggears library"""
    if not GGGEARS_AVAILABLE:
        return None
    
    try:
        gear = SpurRingGear(
            number_of_teeth=num_teeth,
            module=module,
            pressure_angle=math.radians(pressure_angle),
            height=face_width
        )
        
        part = gear.build_part()
        
        if bore_diameter > 0:
            bore = b3d.Cylinder(radius=bore_diameter/2, height=face_width)
            part = part - bore
        
        return part
        
    except Exception as e:
        print(f"Spur ring gear creation failed: {e}")
        return None


def create_helical_ring_gear(module, num_teeth, helix_angle_deg, face_width, bore_diameter=0, pressure_angle=20):
    """Create helical ring gear using gggears library"""
    if not GGGEARS_AVAILABLE:
        return None
    
    try:
        gear = HelicalRingGear(
            number_of_teeth=num_teeth,
            module=module,
            pressure_angle=math.radians(pressure_angle),
            helix_angle=math.radians(helix_angle_deg),
            height=face_width
        )
        
        part = gear.build_part()
        
        if bore_diameter > 0:
            bore = b3d.Cylinder(radius=bore_diameter/2, height=face_width)
            part = part - bore
        
        return part
        
    except Exception as e:
        print(f"Helical ring gear creation failed: {e}")
        return None


def create_rack_gear(module, num_teeth, face_width, height=5, pressure_angle=20):
    """Create involute rack gear using gggears library"""
    if not GGGEARS_AVAILABLE:
        return None
    
    try:
        rack = InvoluteRack(
            number_of_teeth=num_teeth,
            module=module,
            pressure_angle=math.radians(pressure_angle),
            height=height
        )
        
        part = rack.build_part()
        return part
        
    except Exception as e:
        print(f"Rack creation failed: {e}")
        return None


def create_helical_rack_gear(module, num_teeth, helix_angle_deg, face_width, height=5, pressure_angle=20):
    """Create helical rack gear using gggears library"""
    if not GGGEARS_AVAILABLE:
        return None
    
    try:
        rack = HelicalRack(
            number_of_teeth=num_teeth,
            module=module,
            pressure_angle=math.radians(pressure_angle),
            helix_angle=math.radians(helix_angle_deg),
            height=height
        )
        
        part = rack.build_part()
        return part
        
    except Exception as e:
        print(f"Helical rack creation failed: {e}")
        return None


# ==========================================
# BD_WAREHOUSE PROFESSIONAL FASTENER FUNCTIONS
# ==========================================

def create_hex_bolt(size, length, fastener_type="iso4014"):
    """Create professional hex bolt using bd_warehouse"""
    if not BD_WAREHOUSE_AVAILABLE:
        return None
    
    try:
        # Convert size to BD Warehouse format (add pitch if not present)
        if '-' not in size and size.startswith('M'):
            # Add standard pitch for common sizes
            pitch_map = {
                'M1.6': '0.35', 'M2': '0.4', 'M2.5': '0.45', 'M3': '0.5',
                'M3.5': '0.6', 'M4': '0.7', 'M5': '0.8', 'M6': '1',
                'M8': '1.25', 'M10': '1.5', 'M12': '1.75', 'M14': '2',
                'M16': '2', 'M18': '2.5', 'M20': '2.5', 'M22': '2.5',
                'M24': '3', 'M27': '3', 'M30': '3.5', 'M33': '3.5',
                'M36': '4', 'M39': '4', 'M42': '4.5', 'M45': '4.5',
                'M48': '5', 'M52': '5', 'M56': '5.5', 'M60': '5.5', 'M64': '6'
            }
            if size in pitch_map:
                size = f"{size}-{pitch_map[size]}"
        
        bolt = HexHeadScrew(size=size, length=length, fastener_type=fastener_type)
        return b3d.Part(bolt.wrapped)  # Wrap TopoDS in build123d Part
    except Exception as e:
        print(f"Bolt creation failed: {e}")
        return None

def create_hex_nut(size, fastener_type="iso4032"):
    """Create professional hex nut using bd_warehouse"""
    if not BD_WAREHOUSE_AVAILABLE:
        return None
    
    try:
        # Format size with pitch if not provided
        if '-' not in size and size.startswith('M'):
            pitch_map = {'M3': '0.5', 'M4': '0.7', 'M5': '0.8', 'M6': '1', 
                        'M8': '1.25', 'M10': '1.5', 'M12': '1.75', 'M16': '2', 'M20': '2.5'}
            pitch = pitch_map.get(size, '1.25')
            size_with_pitch = f"{size}-{pitch}"
        else:
            size_with_pitch = size
        
        nut = HexNut(size=size_with_pitch, fastener_type=fastener_type)
        return b3d.Part(nut.wrapped)  # Wrap TopoDS in build123d Part
    except Exception as e:
        print(f"Hex nut creation failed: {e}")
        return None

def create_washer(size, fastener_type="iso7089"):
    """Create professional washer using bd_warehouse"""
    if not BD_WAREHOUSE_AVAILABLE:
        return None
    
    try:
        washer = PlainWasher(size=size, fastener_type=fastener_type)
        return b3d.Part(washer.wrapped)  # Wrap TopoDS in build123d Part
    except Exception as e:
        print(f"Washer creation failed: {e}")
        return None

def create_socket_screw(size, length, fastener_type="iso4762"):
    """Create professional socket head cap screw using bd_warehouse"""
    if not BD_WAREHOUSE_AVAILABLE:
        return None
    
    try:
        # Format size with pitch if not provided
        if '-' not in size and size.startswith('M'):
            pitch_map = {'M3': '0.5', 'M4': '0.7', 'M5': '0.8', 'M6': '1', 
                        'M8': '1.25', 'M10': '1.5', 'M12': '1.75', 'M16': '2', 'M20': '2.5'}
            pitch = pitch_map.get(size, '1.25')
            size_with_pitch = f"{size}-{pitch}"
        else:
            size_with_pitch = size
        
        screw = SocketHeadCapScrew(size=size_with_pitch, length=length, fastener_type=fastener_type)
        return b3d.Part(screw.wrapped)  # Wrap TopoDS in build123d Part
    except Exception as e:
        print(f"Socket screw creation failed: {e}")
        return None

def create_counter_sunk_screw(size, length, fastener_type="iso10642"):
    """Create professional counter-sunk screw using bd_warehouse"""
    if not BD_WAREHOUSE_AVAILABLE:
        return None
    
    try:
        # Format size with pitch if not provided
        if '-' not in size and size.startswith('M'):
            pitch_map = {'M3': '0.5', 'M4': '0.7', 'M5': '0.8', 'M6': '1.0', 
                        'M8': '1.25', 'M10': '1.5', 'M12': '1.75', 'M16': '2.0', 'M20': '2.5'}
            pitch = pitch_map.get(size, '1.25')
            size_with_pitch = f"{size}-{pitch}"
        else:
            size_with_pitch = size
        
        screw = CounterSunkScrew(size=size_with_pitch, length=length, fastener_type=fastener_type)
        return b3d.Part(screw.wrapped)  # Wrap TopoDS in build123d Part
    except Exception as e:
        print(f"Counter-sunk screw creation failed: {e}")
        return None


# ==========================================
# BD WAREHOUSE COMPREHENSIVE COMPONENT FUNCTIONS
# ==========================================

def create_bearing(bearing_type="ball", size="M8-16-4"):
    """Create professional bearing using bd_warehouse"""
    if not BD_WAREHOUSE_AVAILABLE:
        return None
    
    try:
        if bearing_type == "ball":
            bearing = SingleRowDeepGrooveBallBearing(
                size=size
            )
        elif bearing_type == "angular_contact":
            bearing = SingleRowAngularContactBallBearing(
                size=size
            )
        elif bearing_type == "cylindrical":
            bearing = SingleRowCylindricalRollerBearing(
                size=size
            )
        elif bearing_type == "tapered":
            bearing = SingleRowTaperedRollerBearing(
                size=size
            )
        else:
            bearing = SingleRowDeepGrooveBallBearing(
                size=size
            )
        
        return b3d.Part(bearing.wrapped)  # Wrap TopoDS in build123d Part
    except Exception as e:
        print(f"Bearing creation failed: {e}")
        return None

def create_iso_thread(diameter, pitch, length, thread_type="external"):
    """Create professional ISO thread using bd_warehouse"""
    if not BD_WAREHOUSE_AVAILABLE:
        return None
    
    try:
        thread = IsoThread(
            major_diameter=diameter,
            pitch=pitch,
            length=length,
            external=(thread_type == "external")
        )
        return b3d.Part(thread.wrapped)  # Wrap TopoDS in build123d Part
    except Exception as e:
        print(f"ISO thread creation failed: {e}")
        return None

def create_acme_thread(diameter, pitch, length, thread_type="external"):
    """Create professional ACME thread using bd_warehouse"""
    if not BD_WAREHOUSE_AVAILABLE:
        return None
    
    try:
        thread = AcmeThread(
            major_diameter=diameter,
            pitch=pitch,
            length=length,
            external=(thread_type == "external")
        )
        return b3d.Part(thread.wrapped)  # Wrap TopoDS in build123d Part
    except Exception as e:
        print(f"ACME thread creation failed: {e}")
        return None

def create_pipe(nps, material="steel"):
    """Create professional pipe section using bd_warehouse"""
    if not BD_WAREHOUSE_AVAILABLE:
        return None
    
    try:
        pipe_section = PipeSection(
            nps=nps,
            material=material,
            identifier="40"  # Schedule 40 identifier
        )
        return b3d.Part(pipe_section.wrapped)  # Wrap TopoDS in build123d Part
    except Exception as e:
        print(f"Pipe creation failed: {e}")
        return None

def create_pipe_section(nps, material="steel", identifier="40"):
    """Create professional pipe section using bd_warehouse"""
    if not BD_WAREHOUSE_AVAILABLE:
        return None
    
    try:
        pipe_section = PipeSection(
            nps=nps,
            material=material,
            identifier=identifier
        )
        return b3d.Part(pipe_section.wrapped)  # Wrap TopoDS in build123d Part
    except Exception as e:
        print(f"Pipe section creation failed: {e}")
        return None

def create_flange(nps, flange_type="slip_on", pressure_class=150):
    """Create professional flange using bd_warehouse"""
    if not BD_WAREHOUSE_AVAILABLE:
        return None
    
    try:
        # Convert string pressure_class to integer if needed
        if isinstance(pressure_class, str):
            pressure_class = int(pressure_class)
        
        if flange_type == "slip_on":
            flange = SlipOnFlange(
                nps=nps,
                flange_class=pressure_class
            )
        elif flange_type == "weld_neck":
            flange = WeldNeckFlange(
                nps=nps,
                flange_class=pressure_class
            )
        elif flange_type == "blind":
            flange = BlindFlange(
                nps=nps,
                flange_class=pressure_class
            )
        elif flange_type == "lapped":
            flange = LappedFlange(
                nps=nps,
                flange_class=pressure_class
            )
        elif flange_type == "socket_weld":
            flange = SocketWeldFlange(
                nps=nps,
                flange_class=pressure_class
            )
        else:
            flange = SlipOnFlange(
                nps=nps,
                flange_class=pressure_class
            )
        
        return b3d.Part(flange.wrapped)  # Wrap TopoDS in build123d Part
    except Exception as e:
        print(f"Flange creation failed: {e}")
        return None

def create_mechanical_assembly(bearing_type="ball", pipe_size="2", flange_type="slip_on"):
    """Create a simple mechanical assembly using BD Warehouse components"""
    if not BD_WAREHOUSE_AVAILABLE:
        return None
    
    try:
        # Create a simple assembly with just one component
        bearing = create_bearing(bearing_type=bearing_type, size="M8-16-4")
        if bearing:
            # Just return the bearing as a simple assembly
            return bearing
        
        return None
    except Exception as e:
        print(f"Mechanical assembly creation failed: {e}")
        return None


# ==========================================
# EXECUTION
# ==========================================

def execute_user_code(code: str):
    """Execute CAD generation code"""
    
    # Clean the code - remove markdown code blocks, imports, and clean up
    import re
    
    # Manual approach to remove markdown code blocks
    # Split by lines and remove lines with ```
    lines = code.split('\n')
    clean_lines = []
    in_code_block = False
    
    for line in lines:
        stripped = line.strip()
        
        # Handle code block markers (handle both `python and ```python)
        if stripped.startswith('```python') or stripped.startswith('`python'):
            in_code_block = True
            continue
        elif stripped.startswith('```') and in_code_block:
            in_code_block = False
            continue
        elif stripped.startswith('```') and not in_code_block:
            # Skip opening ``` without python
            continue
        elif stripped.startswith('`') and not in_code_block and stripped != '`':
            # Skip single backtick lines
            continue
        
        # Skip python: marker
        if stripped.startswith('python:'):
            continue
        
        # Skip empty lines and comments at the start
        if not stripped or stripped.startswith('#'):
            continue
        
        # Skip import statements for modules we provide
        if stripped.startswith('import build123d') or stripped.startswith('from build123d') or stripped.startswith('import math'):
            continue
        
        # Skip any remaining markdown markers
        if stripped.startswith('```') or stripped.startswith('python') or stripped == '`':
            continue
        
        clean_lines.append(line)
    
    code = "\n".join(clean_lines)
    
    # Create namespace with available functions and modules
    namespace = {
        'b3d': b3d,
        'math': math,
        # Gear functions
        'create_spur_gear': create_spur_gear,
        'create_helical_gear': create_helical_gear,
        'create_bevel_gear': create_bevel_gear,
        'create_cycloid_gear': create_cycloid_gear,
        'create_spur_ring_gear': create_spur_ring_gear,
        'create_helical_ring_gear': create_helical_ring_gear,
        'create_rack_gear': create_rack_gear,
        'create_helical_rack_gear': create_helical_rack_gear,
        # Fastener functions (BD Warehouse)
        'create_hex_bolt': create_hex_bolt,
        'create_hex_nut': create_hex_nut,
        'create_washer': create_washer,
        'create_socket_screw': create_socket_screw,
        'create_counter_sunk_screw': create_counter_sunk_screw,
        # Comprehensive BD Warehouse functions
        'create_bearing': create_bearing,
        'create_pipe': create_pipe,
        'create_pipe_section': create_pipe_section,
        'create_iso_thread': create_iso_thread,
        'create_acme_thread': create_acme_thread,
        'create_flange': create_flange,
        '__builtins__': __builtins__,
    }
    
    try:
        # First, check if the code creates a 'part' variable
        if 'part =' not in code:
            return None, "❌ Error: Code must create a 'part' variable. Please ensure your code ends with 'part = create_[function]([parameters])'"
        
        # Execute the code
        exec(code, namespace)
        
        # Check if part variable was created
        if 'part' not in namespace:
            return None, "❌ Execution failed: No 'part' variable created. Make sure your code creates a variable named 'part'."
        
        # Get the part
        part = namespace.get('part')
        if part is None:
            return None, "❌ Error: 'part' variable was created but is None."
        
        return part, None
        
    except Exception as e:
        error_msg = f"❌ Code execution failed: {str(e)}"
        # Add helpful suggestions for common errors
        if "NameError" in str(e):
            error_msg += "\n💡 Tip: Make sure all variables are defined before use."
        elif "TypeError" in str(e):
            error_msg += "\n💡 Tip: Check function parameter types and values."
        elif "ValueError" in str(e):
            error_msg += "\n💡 Tip: Check if parameter values are within valid ranges."
        
        return None, error_msg
    

def setup_agent(brain_choice: str):
    """Setup LLM model using LiteLLMModel"""
    
    if "Gemini" in brain_choice:
        model_id = "gemini/gemini-2.0-flash-exp"
        api_key = st.secrets.get("GEMINI_API_KEY", "")
    else:
        model_id = "groq/llama-3.3-70b-versatile"
        api_key = st.secrets.get("GROQ_API_KEY", "")
    
    if not api_key:
        st.error("Missing API key")
        return None
    
    try:
        if "Gemini" in brain_choice:
            model = LiteLLMModel(
                model_id=model_id,
                api_key=api_key,
                api_base="https://generativelanguage.googleapis.com/v1beta"
            )
        else:
            model = LiteLLMModel(model_id=model_id, api_key=api_key)
        
        # Store model_id and api_key for later use in generate_gear_code
        model._stored_model_id = model_id
        model._stored_api_key = api_key
        return model
    except Exception as e:
        st.error(f"Model error: {str(e)}")
        return None


def generate_cad_code(model, request: str) -> str:
    """Generate CAD code from text request using LiteLLMModel"""
    
    prompt = f"""You are a CAD code generator. Generate Python code to create 3D parts using build123d and BD Warehouse.

IMPORTANT: Use build123d (imported as 'b3d') and the available functions below for component creation.

Available functions (USE THESE EXACTLY):

GEAR FUNCTIONS (GGGEARS):
- create_spur_gear(module, num_teeth, face_width, bore_diameter=0) - Creates a spur gear
- create_helical_gear(module, num_teeth, helix_angle_deg, face_width, bore_diameter=0) - Creates a helical gear
- create_bevel_gear(module, num_teeth, cone_angle_deg, face_width, bore_diameter=0) - Creates a bevel gear
- create_cycloid_gear(module, num_teeth, face_width, bore_diameter=0) - Creates a cycloid gear
- create_spur_ring_gear(module, num_teeth, face_width, bore_diameter=0) - Creates a spur ring gear (internal teeth)
- create_helical_ring_gear(module, num_teeth, helix_angle_deg, face_width, bore_diameter=0) - Creates a helical ring gear
- create_rack_gear(module, num_teeth, face_width, height=5) - Creates a rack gear
- create_helical_rack_gear(module, num_teeth, helix_angle_deg, face_width, height=5) - Creates a helical rack gear

FASTENER FUNCTIONS (BD Warehouse):
- create_hex_bolt(size, length, fastener_type="iso4014") - Creates professional hex bolt (size like "M8", length in mm)
- create_hex_nut(size, fastener_type="iso4032") - Creates professional hex nut (size like "M8")
- create_washer(size, fastener_type="iso7089") - Creates professional washer (size like "M8")
- create_socket_screw(size, length, fastener_type="iso4762") - Creates socket head cap screw
- create_counter_sunk_screw(size, length, fastener_type="iso10642") - Creates counter-sunk screw

IMPORTANT: Create ONLY individual components, NOT assemblies!

BEARING FUNCTIONS (BD Warehouse):
- create_bearing(bearing_type="ball", size="M8-16-4") - Creates professional bearings
  Types: "ball", "angular_contact", "cylindrical", "tapered"
  Size format: "M8-16-4" (metric-size-inner_diameter-width)
  For simple requests like "size 20", use "M20-40-8" as reasonable default

PIPE FUNCTIONS (BD Warehouse):
- create_pipe(nps, material="steel") - Creates professional pipe sections
- create_pipe_section(nps, material="steel") - Creates pipe sections

THREAD FUNCTIONS (BD Warehouse):
- create_iso_thread(diameter, pitch, length, thread_type="external") - Creates ISO threads
- create_acme_thread(diameter, pitch, length, thread_type="external") - Creates ACME threads

FLANGE FUNCTIONS (BD Warehouse):
- create_flange(nps, flange_type="slip_on", pressure_class="150") - Creates professional flanges
  Types: "slip_on", "weld_neck", "blind", "lapped", "socket_weld"
  Pressure classes: "150", "300", "400", "600", "900", "1500", "2500"

You also have access to build123d (as 'b3d') and math module for other operations.

CRITICAL REQUIREMENTS:
1. You MUST create a variable called 'part' that contains final 3D part
2. Use ONLY the functions listed above for component creation - NEVER use other CAD libraries directly
3. Return ONLY Python code, no explanations or markdown
4. If the request is unclear, make reasonable assumptions
5. **MANDATORY: Include PARAM comments for EVERY parameter to enable sliders**
   Format: "parameter_name = value  # PARAM (min, max)"
6. **ALWAYS END YOUR CODE WITH: `part = create_[function]([parameters])` - THE PART VARIABLE MUST BE CREATED**
7. **BEARING REQUESTS: For simple requests like "bearing size 20", you MUST:**
   - Extract the number (20) from the request
   - Convert to proper format: "M20-40-8" (use reasonable defaults for inner diameter and width)
   - Example: "A ball bearing size 20" → bearing_size = "M20-40-8"
   - ALWAYS create the 'part' variable: `part = create_bearing(bearing_type="ball", size="M20-40-8")`
   - NEVER forget to assign the function result to 'part'
   Examples:
   - size = "M8"  # PARAM ("M3", "M20")
   - length = 30  # PARAM (10, 100)
   - bearing_type = "ball"  # PARAM ("ball", "angular_contact", "cylindrical", "tapered")
   - bearing_size = "M8-16-4"  # PARAM ("M3-10-4", "M10-35-11")

FINAL EXAMPLE CODE PATTERNS:
For hex bolt: 
size = "M8"  # PARAM ("M3", "M20")
length = 30  # PARAM (10, 100)
part = create_hex_bolt(size=size, length=length)

For hex nut:
size = "M8"  # PARAM ("M3", "M20")
part = create_hex_nut(size=size)

For washer:
size = "M8"  # PARAM ("M3", "M20")
part = create_washer(size=size)

For socket screw:
size = "M8"  # PARAM ("M3", "M20")
length = 30  # PARAM (10, 100)
part = create_socket_screw(size=size, length=length)

For bearing:
bearing_type = "ball"  # PARAM ("ball", "angular_contact", "cylindrical", "tapered")
bearing_size = "M8-16-4"  # PARAM ("M3-10-4", "M10-35-11") 
part = create_bearing(bearing_type=bearing_type, size=bearing_size)

For spur gear:
module = 2  # PARAM (1, 5)
num_teeth = 20  # PARAM (10, 50)
face_width = 10  # PARAM (5, 20)
part = create_spur_gear(module=module, num_teeth=num_teeth, face_width=face_width)

For pipe:
nps = "2"  # PARAM ("0.5", "12")
part = create_pipe(nps=nps)

For flange:
nps = "2"  # PARAM ("0.5", "12")
pressure_class = "150"  # PARAM ("150", "300", "400", "600", "900", "1500", "2500")
part = create_flange(nps=nps, pressure_class=pressure_class)

For thread:
diameter = 8  # PARAM (3, 20)
pitch = 1.25  # PARAM (0.5, 3)
length = 30  # PARAM (10, 100)
part = create_iso_thread(diameter=diameter, pitch=pitch, length=length)

IMPORTANT: YOUR CODE MUST END WITH A LINE THAT STARTS WITH "part = "

User request: {request}

Generate Python code:"""
    
    try:
        # Access stored model_id and api_key from the model
        model_id = getattr(model, '_stored_model_id', None)
        api_key = getattr(model, '_stored_api_key', None)
        
        if not model_id or not api_key:
            # Fallback: try to access model attributes directly
            model_id = getattr(model, 'model_id', None)
            api_key = getattr(model, 'api_key', None)
        
        if not model_id or not api_key:
            return f"ERROR: Could not access model_id or api_key from LiteLLMModel"
        
        # Use litellm completion directly for text generation
        response = completion(
            model=model_id,
            messages=[{"role": "user", "content": prompt}],
            api_key=api_key,
            temperature=0.3  # Lower temperature for more consistent code generation
        )
        
        return response.choices[0].message.content
    except Exception as e:
        import traceback
        return f"ERROR: {str(e)}\n{traceback.format_exc()}"

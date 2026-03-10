import streamlit as st
import json
import tempfile
import re
from backend import setup_agent, execute_user_code, generate_cad_code
from param_utils import extract_params, update_code_with_params
from stl_utils import create_stl_for_streamlit, verify_stl_format, check_dependencies

# Check dependencies and show warnings
dependency_issues = check_dependencies()
if dependency_issues:
    for issue in dependency_issues:
        st.error(issue)
    st.warning("🔧 The app will run in limited mode without full 3D functionality.")

try:
    from streamlit_stl import stl_from_file
    STREAML_STL_AVAILABLE = True
except ImportError:
    STREAML_STL_AVAILABLE = False
    st.warning("⚠️ streamlit-stl not installed. 3D viewer will not work.")

# ==========================================
# PAGE CONFIG & STYLING
# ==========================================

st.set_page_config(
    page_title="MechanicAI | Text to CAD Agent",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for dark mode classic styling
st.markdown("""
<style>
    /* Dark mode theme */
    .stApp {
        background: #0a1f0a;
        color: #e0e0e0;
    }
    
    .main-header {
        background: linear-gradient(90deg, #1a3d1a 0%, #2d5a2d 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin-bottom: 1.5rem;
        text-align: center;
        color: #ffffff;
        border: 2px solid #3a6b3a;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.5);
    }
    
    .gear-card {
        background: #1a2d1a;
        padding: 1.5rem;
        border-radius: 15px;
        border: 2px solid #3a6b3a;
        margin-bottom: 1rem;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.5);
    }
    
    .chat-container {
        background: #1a2d1a;
        border-radius: 15px;
        padding: 1.5rem;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.5);
        border: 2px solid #3a6b3a;
    }
    
    .viewer-container {
        background: #1a2d1a;
        border-radius: 15px;
        padding: 1.5rem;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.5);
        border: 2px solid #3a6b3a;
    }
    
    .param-slider {
        margin: 0.5rem 0;
    }
    
    .stSlider > div[data-baseweb="slider"] {
        margin: 0.5rem 0;
    }
    
    .success-message {
        background: #1a3d1a;
        color: #90ee90;
        padding: 1rem;
        border-radius: 10px;
        border: 2px solid #3a6b3a;
    }
    
    .export-buttons {
        display: flex;
        gap: 0.5rem;
        justify-content: center;
        flex-wrap: wrap;
    }
    
    /* Dark mode for streamlit components */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > select {
        background: #2d4a2d;
        color: #e0e0e0;
        border: 1px solid #3a6b3a;
    }
    
    .stButton > button {
        background: #2d5a2d;
        color: #ffffff;
        border: 1px solid #3a6b3a;
        font-weight: bold;
    }
    
    .stButton > button:hover {
        background: #3a6b3a;
        border-color: #4a7b4a;
    }
    
    .stButton > button[kind="primary"] {
        background: #3a6b3a;
        color: #ffffff;
        border: 1px solid #4a7b4a;
    }
    
    .stButton > button[kind="primary"]:hover {
        background: #4a7b4a;
        border-color: #5a8b5a;
    }
    
    .stSlider > div[data-baseweb="slider"] > div {
        background: #2d4a2d;
    }
    
    .stSelectbox > div > div > div {
        background: #2d4a2d;
        color: #e0e0e0;
    }
    
    .stExpander {
        background: #1a2d1a;
        border: 1px solid #3a6b3a;
    }
    
    .stProgress > div > div > div > div {
        background: #3a6b3a;
    }
    
    /* Sidebar dark mode - very dark green */
    .css-1d391kg {
        background: #051505;
    }
    
    .css-1lcbmhc {
        background: #0a1f0a;
        border: 2px solid #1a3d1a;
    }
    
    .stSidebar {
        background: #051505;
    }
    
    .stSidebar .stMarkdown {
        color: #e0e0e0;
    }
    
    /* Sidebar sliders - make them visible */
    .stSidebar .stSlider {
        margin: 1rem 0;
    }
    
    .stSidebar .stSlider > div[data-baseweb="slider"] {
        background: #1a3d1a;
        border: 1px solid #3a6b3a;
        border-radius: 5px;
        padding: 0.5rem;
    }
    
    .stSidebar .stSlider > div > div > div {
        background: #3a6b3a;
    }
    
    .stSidebar .stSlider [data-baseweb="slider-handle"] {
        background: #5a8b5a;
        border: 2px solid #6a9b6a;
    }
    
    .stSidebar .stButton > button {
        margin-top: 1rem;
    }
    
    /* Headers and text */
    h1, h2, h3, h4, h5, h6 {
        color: #90ee90;
    }
    
    .stSubheader {
        color: #90ee90;
    }
    
    /* Code blocks */
    .stCode {
        background: #0d1f0d;
        border: 1px solid #3a6b3a;
    }
    
    /* Info/warning/error messages */
    .stInfo {
        background: #1a3d1a;
        border-left: 4px solid #3a6b3a;
    }
    
    .stWarning {
        background: #3d3d1a;
        border-left: 4px solid #6b6b3a;
    }
    
    .stError {
        background: #3d1a1a;
        border-left: 4px solid #6b3a3a;
    }
    
    .stSuccess {
        background: #1a3d1a;
        border-left: 4px solid #3a6b3a;
        color: #90ee90;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# SESSION STATE
# ==========================================

if "history" not in st.session_state:
    st.session_state.history = []
if "last_code" not in st.session_state:
    st.session_state.last_code = None
if "generated_part" not in st.session_state:
    st.session_state.generated_part = None
if "agent" not in st.session_state:
    st.session_state.agent = None
if "brain_choice" not in st.session_state:
    st.session_state.brain_choice = "Groq Llama 3.3"

# ==========================================
# MODERN LAYOUT
# ==========================================

# Main Header
st.markdown("""
<div class="main-header">
    <h1>🏭 MechanicAI | Text to CAD Agent</h1>
    <p style="font-size: 1.2rem; margin: 0.5rem 0;">
        Transform natural language descriptions into professional mechanical components using AI
    </p>
    <p style="font-size: 1rem; opacity: 0.9; margin: 0;">
        Generate gears, fasteners, bearings, pipes, threads, flanges, and complete assemblies
    </p>
</div>
""", unsafe_allow_html=True)

# Main layout columns
col_chat, col_viewer = st.columns([1.2, 1], gap="large")

# ==========================================
# LEFT COLUMN: CHAT
# ==========================================

with col_chat:
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    
    # AI Model Selection
    st.subheader("🤖 AI Assistant")
    brain_choice = st.selectbox(
        "Choose AI Model:",
        ["Groq Llama 3.3", "Gemini 2.5 Flash"],
        index=0,
        key="brain_selector"
    )
    
    if brain_choice != st.session_state.brain_choice:
        st.session_state.brain_choice = brain_choice
        st.session_state.agent = None
        st.rerun()
    
    # Chat Input
    st.subheader("💬 Design Request")
    user_input = st.text_area(
        "Describe your mechanical component:",
        placeholder="Example: Create an M8 hex bolt with 30mm length, or a ball bearing size 10, or a 2-inch pipe section",
        height=100,
        key="user_request"
    )
    
    # Generate Button
    if st.button("🚀 Generate Component", type="primary", use_container_width=True):
        if user_input.strip():
            if not st.session_state.agent:
                agent = setup_agent(brain_choice)
                if agent:
                    st.session_state.agent = agent
                else:
                    st.error("❌ Failed to setup AI agent")
                    st.stop()
            
            # Generate code
            with st.spinner("🔄 Generating mechanical component design..."):
                generated_code = generate_cad_code(st.session_state.agent, user_input)
                
                if generated_code and not generated_code.startswith("ERROR"):
                    # Execute code
                    part, exec_result = execute_user_code(generated_code)
                    
                    if part:
                        st.session_state.generated_part = part
                        st.session_state.last_code = generated_code
                        
                        # Add to history
                        st.session_state.history.append({
                            "request": user_input,
                            "code": generated_code,
                            "result": "success"
                        })
                        
                        st.success("✅ Component generated successfully!")
                        st.rerun()
                    else:
                        st.error(f"❌ Execution failed: {exec_result}")
                else:
                    st.error(f"❌ Code generation failed: {generated_code}")
        else:
            st.warning("⚠️ Please enter a design request")
    
    # Chat History
    if st.session_state.history:
        st.subheader("📜 Design History")
        for i, item in enumerate(reversed(st.session_state.history[-5:])):
            with st.expander(f"Request {i+1}: {item['request'][:50]}...", expanded=False):
                st.code(item['code'], language='python')
    
    st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# RIGHT COLUMN: 3D VIEWER
# ==========================================

with col_viewer:
    if st.session_state.generated_part:
        st.markdown('<div class="viewer-container">', unsafe_allow_html=True)
        
        # 3D Viewer
        st.subheader("🔍 3D Component Preview")
        
        # Display the 3D model
        try:
            part_to_show = st.session_state.generated_part
            
            if STREAML_STL_AVAILABLE and part_to_show:
                ascii_stl_path = create_stl_for_streamlit(part_to_show)
                
                if ascii_stl_path:
                    # Use a metallic color that stands out against dark background
                    stl_from_file(file_path=ascii_stl_path, color="#C0C0C0", height=400)
                else:
                    st.error("❌ Failed to create 3D preview")
            elif not STREAML_STL_AVAILABLE:
                st.warning("⚠️ 3D viewer not available (streamlit-stl missing)")
                if part_to_show:
                    st.info("📦 Component created successfully! Use download buttons below to get STL file.")
                else:
                    st.error("❌ No component to display")
            else:
                st.error("❌ Failed to create 3D preview")
        except Exception as e:
            st.error(f"❌ 3D display error: {str(e)[:200]}")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Export Section
        st.markdown('<div class="gear-card">', unsafe_allow_html=True)
        st.subheader("💾 Export Options")
        
        col_export1, col_export2 = st.columns(2)
        
        with col_export1:
            # STL Export
            try:
                if st.session_state.generated_part:
                    stl_path = tempfile.NamedTemporaryFile(delete=False, suffix=".stl").name
                    success = export_stl(st.session_state.generated_part, stl_path)
                    
                    if success:
                        with open(stl_path, "rb") as f:
                            st.download_button(
                                "📥 Download STL",
                                data=f.read(),
                                file_name="component.stl",
                                mime="application/octet-stream",
                                use_container_width=True
                            )
                        os.unlink(stl_path)
                    else:
                        st.caption("STL export failed")
            except Exception as e:
                st.caption(f"STL export error: {str(e)[:100]}")
        
        with col_export2:
            # STEP Export
            try:
                if st.session_state.generated_part:
                    step_path = tempfile.NamedTemporaryFile(delete=False, suffix=".step").name
                    success = export_step(st.session_state.generated_part, step_path)
                    
                    if success:
                        with open(step_path, "rb") as f:
                            st.download_button(
                                "📥 Download STEP",
                                data=f.read(),
                                file_name="component.step",
                                mime="application/octet-stream",
                                use_container_width=True
                            )
                        os.unlink(step_path)
                    else:
                        st.caption("STEP export failed")
            except Exception as e:
                st.caption(f"STEP export error: {str(e)[:100]}")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
    else:
        # Welcome screen
        st.markdown('<div class="viewer-container">', unsafe_allow_html=True)
        st.markdown("""
        <div style="text-align: center; padding: 2rem;">
            <h2 style="color: #90ee90;">🎨 Welcome to MechanicAI | Text to CAD Agent</h2>
            <p style="color: #e0e0e0;">Start by describing your mechanical component requirements in the chat panel</p>
            <div style="background: #1a3d1a; padding: 1.5rem; border-radius: 15px; margin: 1.5rem 0; border: 2px solid #3a6b3a;">
                <h4 style="color: #90ee90;">💡 Component Examples:</h4>
                <ul style="text-align: left; color: #e0e0e0;">
                    <li>"Create an M8 hex bolt with 30mm length"</li>
                    <li>"Make a ball bearing size 10"</li>
                    <li>"Design a 2-inch pipe section"</li>
                    <li>"Create a slip-on flange size 2"</li>
                    <li>"Generate a 20-tooth spur gear with module 2"</li>
                    <li>"Make a complete mechanical assembly"</li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# SIDEBAR: PARAMETERS
# ==========================================

with st.sidebar:
    if st.session_state.generated_part and st.session_state.last_code:
        st.markdown('<div class="gear-card">', unsafe_allow_html=True)
        st.subheader("⚙️ Component Parameters")
        
        # Extract and display parameters
        params = extract_params(st.session_state.last_code)
        
        if params:
            st.write("**Adjust parameters and click 'Update Component':**")
            
            # Create sliders for each parameter
            new_values = {}
            rerun_needed = False
            
            for param_name, param_info in params.items():
                current_value = param_info["value"]
                min_val = param_info["min"]
                max_val = param_info["max"]
                param_type = param_info["type"]
                
                # Create slider with better styling
                if param_type == "int":
                    new_value = st.slider(
                        f"{param_name.replace('_', ' ').title()}",
                        min_value=int(min_val),
                        max_value=int(max_val),
                        value=int(current_value),
                        step=1,
                        key=f"param_{param_name}",
                        help=f"Range: {min_val} - {max_val}"
                    )
                else:
                    new_value = st.slider(
                        f"{param_name.replace('_', ' ').title()}",
                        min_value=float(min_val),
                        max_value=float(max_val),
                        value=float(current_value),
                        step=0.1,
                        format="%.2f",
                        key=f"param_{param_name}",
                        help=f"Range: {min_val} - {max_val}"
                    )
                
                if new_value != current_value:
                    new_values[param_name] = new_value
                    rerun_needed = True
            
            # Update button
            if rerun_needed and st.button("🔄 Update Component", type="primary", use_container_width=True):
                with st.spinner("🔄 Updating component..."):
                    # Update code with new parameter values
                    updated_code = update_code_with_params(st.session_state.last_code, new_values)
                    st.session_state.last_code = updated_code
                    
                    # Re-execute
                    part, exec_result = execute_user_code(updated_code)
                    
                    if part:
                        st.session_state.generated_part = part
                        st.success("✅ Component updated successfully!")
                        st.rerun()
                    else:
                        st.error(f"❌ Update failed: {exec_result}")
        else:
            st.info("ℹ️ No adjustable parameters found in current design")
        
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        # Show placeholder in sidebar
        st.markdown('<div class="gear-card">', unsafe_allow_html=True)
        st.subheader("⚙️ Component Parameters")
        st.info("👈 Generate a component first to see adjustable parameters")
        st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# FOOTER
# ==========================================

st.divider()

st.markdown("""
<div style="text-align: center; color: #90ee90; padding: 1.5rem; background: #1a2d1a; border-radius: 15px; border: 2px solid #3a6b3a;">
    <strong>🏭 MechanicAI | Text to CAD Agent</strong> | 
    Powered by BD Warehouse + gggears + build123d + AI | 
    Transform text into industrial-grade 3D mechanical components
</div>
""", unsafe_allow_html=True)

import streamlit as st
import requests
import os
from datetime import datetime

# Configure page
st.set_page_config(page_title="Terminal", layout="wide", initial_sidebar_state="collapsed")

# Custom CSS for realistic terminal look
st.markdown("""
<style>
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display: none;}

    /* Main app styling */
    .stApp {
        background-color: #0c0c0c;
        padding: 0;
        margin: 0;
    }

    /* Terminal container */
    .terminal-container {
        background-color: #0c0c0c;
        color: #cccccc;
        font-family: 'Courier New', Consolas, monospace;
        font-size: 14px;
        height: 100vh;
        display: flex;
        flex-direction: column;
        overflow: hidden;
        padding: 0;
        margin: 0;
    }

    /* Terminal header */
    .terminal-header {
        background-color: #1e1e1e;
        color: #cccccc;
        font-family: 'Courier New', Consolas, monospace;
        padding: 8px 15px;
        font-size: 12px;
        border-bottom: 1px solid #3e3e3e;
        flex-shrink: 0;
    }

    /* Terminal output area */
    .terminal-output {
        background-color: #0c0c0c;
        color: #cccccc;
        font-family: 'Courier New', Consolas, monospace;
        font-size: 14px;
        padding: 15px;
        flex-grow: 1;
        overflow-y: auto;
        overflow-x: hidden;
        white-space: pre-wrap;
        word-wrap: break-word;
        line-height: 1.5;
    }

    /* Auto-scroll to bottom */
    .terminal-output::-webkit-scrollbar {
        width: 10px;
    }

    .terminal-output::-webkit-scrollbar-track {
        background: #1e1e1e;
    }

    .terminal-output::-webkit-scrollbar-thumb {
        background: #3e3e3e;
        border-radius: 5px;
    }

    .terminal-output::-webkit-scrollbar-thumb:hover {
        background: #555;
    }

    /* Terminal input area */
    .terminal-input-area {
        background-color: #0c0c0c;
        padding: 10px 15px;
        border-top: 1px solid #1e1e1e;
        flex-shrink: 0;
    }

    /* Prompt text */
    .prompt-text {
        color: #4ec9b0;
        font-weight: bold;
    }

    .success-text {
        color: #4ec9b0;
    }

    .error-text {
        color: #f48771;
    }

    .info-text {
        color: #569cd6;
    }

    .warning-text {
        color: #dcdcaa;
    }

    /* Style the input */
    div[data-testid="stTextInput"] {
        margin: 0;
        padding: 0;
    }

    div[data-testid="stTextInput"] > div {
        margin: 0;
        padding: 0;
    }

    div[data-testid="stTextInput"] input {
        background-color: #0c0c0c;
        color: #cccccc;
        font-family: 'Courier New', Consolas, monospace;
        font-size: 14px;
        border: none;
        padding: 0;
        margin: 0;
        outline: none;
        box-shadow: none;
    }

    div[data-testid="stTextInput"] input:focus {
        border: none;
        outline: none;
        box-shadow: none;
    }

    div[data-testid="stTextInput"] label {
        display: none;
    }

    /* Hide form submit button */
    .stFormSubmitButton {
        display: none;
    }

    /* Style buttons */
    .stButton button {
        background-color: #1e1e1e;
        color: #cccccc;
        font-family: 'Courier New', Consolas, monospace;
        font-size: 12px;
        border: 1px solid #3e3e3e;
        padding: 5px 10px;
    }

    .stButton button:hover {
        background-color: #2e2e2e;
        border-color: #4ec9b0;
    }

    /* Cursor blink effect */
    .cursor {
        display: inline-block;
        width: 8px;
        height: 14px;
        background-color: #cccccc;
        animation: blink 1s step-end infinite;
        margin-left: 2px;
    }

    @keyframes blink {
        0%, 50% { opacity: 1; }
        51%, 100% { opacity: 0; }
    }

    /* Spacing adjustments */
    .block-container {
        padding: 0 !important;
        max-width: none !important;
    }

    .element-container {
        margin: 0 !important;
        padding: 0 !important;
    }
</style>

<script>
    // Auto-scroll to bottom when content updates
    function scrollToBottom() {
        const output = document.querySelector('.terminal-output');
        if (output) {
            output.scrollTop = output.scrollHeight;
        }
    }

    // Execute on load and after updates
    document.addEventListener('DOMContentLoaded', scrollToBottom);
    setTimeout(scrollToBottom, 100);
    setTimeout(scrollToBottom, 500);
</script>
""", unsafe_allow_html=True)

# Initialize session state
if 'history' not in st.session_state:
    st.session_state.history = []
    # Welcome message
    st.session_state.history.append('<span class="info-text">Terminal Emulator v1.0</span>')
    st.session_state.history.append('<span class="info-text">Type your commands below. Use "clear" to clear the terminal.</span>')
    st.session_state.history.append('')

if 'current_folder' not in st.session_state:
    st.session_state.current_folder = "root"

# API Configuration
API_URL = os.getenv("API_URL", "http://localhost:8000")

# Function to get current folder
def get_current_folder():
    try:
        response = requests.post(f"{API_URL}/execute", json={"command": "current"}, timeout=5)
        if response.status_code == 200:
            result = response.json().get("result", "")
            if result.startswith("Current folder: "):
                return result.replace("Current folder: ", "")
        return "root"
    except:
        return st.session_state.current_folder

# Terminal header
st.markdown('<div class="terminal-header">Terminal - user@localhost</div>', unsafe_allow_html=True)

# Display terminal output with history
output = ""
for entry in st.session_state.history:
    output += entry + "\n"

# Add auto-scroll script
st.markdown(f'''
<div class="terminal-output" id="terminal-output">
{output}
</div>
<script>
    const output = document.getElementById('terminal-output');
    if (output) {{
        output.scrollTop = output.scrollHeight;
    }}
</script>
''', unsafe_allow_html=True)

# Terminal input area with current folder in prompt
current_folder = get_current_folder()
timestamp = datetime.now().strftime("%H:%M:%S")

# Input section with prompt
with st.form(key="command_form", clear_on_submit=True):
    # Display prompt inline with input
    prompt_html = f'<span class="prompt-text">[{timestamp}] {current_folder}$</span> '

    col1, col2 = st.columns([20, 1])
    with col1:
        st.markdown(f'<div style="display: inline-block;">{prompt_html}</div>', unsafe_allow_html=True)
        command = st.text_input("cmd", placeholder="", key="command_input", label_visibility="collapsed")
    with col2:
        execute = st.form_submit_button("⏎")

# Process command
if execute and command:
    # Update timestamp for the actual execution
    timestamp = datetime.now().strftime("%H:%M:%S")
    current_folder = st.session_state.current_folder

    # Add command to history with prompt
    st.session_state.history.append(f'<span class="prompt-text">[{timestamp}] {current_folder}$</span> {command}')

    # Handle clear command locally
    if command.strip().lower() == "clear":
        st.session_state.history = []
        st.rerun()

    # Execute command via API
    try:
        response = requests.post(f"{API_URL}/execute", json={"command": command}, timeout=5)
        if response.status_code == 200:
            result = response.json().get("result", "Command executed successfully")
            st.session_state.history.append(f'<span class="success-text">{result}</span>')

            # Update current folder
            st.session_state.current_folder = get_current_folder()
        else:
            error_msg = f"Error: HTTP {response.status_code}"
            st.session_state.history.append(f'<span class="error-text">{error_msg}</span>')
    except requests.exceptions.Timeout:
        st.session_state.history.append(f'<span class="error-text">Error: Request timeout</span>')
    except requests.exceptions.ConnectionError:
        st.session_state.history.append(f'<span class="error-text">Error: Cannot connect to API at {API_URL}</span>')
    except requests.exceptions.RequestException as e:
        st.session_state.history.append(f'<span class="error-text">Error: {str(e)}</span>')

    # Add empty line for spacing
    st.session_state.history.append('')

    st.rerun()

# Small utility buttons in bottom corner (optional)
col1, col2, col3 = st.columns([10, 1, 1])
with col2:
    if st.button("🗑️", help="Clear terminal"):
        st.session_state.history = []
        st.rerun()
with col3:
    if st.button("🔄", help="Refresh"):
        st.session_state.current_folder = get_current_folder()
        st.rerun()

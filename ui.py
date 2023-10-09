import streamlit as st
import pyperclip

def set_page():
    st.set_page_config(layout="wide")
    st.title("GPT 3.5 Document Summarization")

def input_output_columns():
    col1, col2 = st.columns([5, 5])
    input_text_initial_value = st.session_state.get('input_text', "")
    input_text = col1.text_area("Input", value=input_text_initial_value, key="input_text_area", height=500)
    run_button = col1.button("Run")
    if 'output_text' not in st.session_state:
        st.session_state['output_text'] = ""
    output_text = col2.text_area("Output", value=st.session_state['output_text'], key="output_text_area", disabled=False, height=500)
    return input_text, run_button, output_text, col2

def sidebar_config():
    st.sidebar.title("Setup")
    with st.sidebar.form(key='config_form'):
        with st.expander("File Selection"):
            uploaded_file = st.file_uploader("Select File:", type=['pdf','txt'])

        with st.expander("LLM Model Options"):
            model = st.radio("Choose LLM version:", ("gpt 3.5 turbo ($0.03)", "text davinci 003 ($0.35)"),disabled=False)
            openai_api_key = st.text_input("Enter OpenAI API Key:",type="password")

        with st.expander("Text Splitting Config"):
            #method = st.radio("Choose method:", ("Map Reduce", "Refine"), index=1)
            chunk_size = st.number_input("Chunk size:", value=10000)
            chunk_overlap = st.number_input("Chunk overlap:", value=500)

        with st.expander("Prompts"):
            basic_prompt = st.text_area("Basic prompt:", value="Provide a detailed summary of the following:")        
            refine_prompt = st.text_area("Refine prompt:", value="Given the new context, refine the original summary into a one page summary.")
            
        # Submit button
        submit_button = st.form_submit_button("Apply")
    return model, chunk_size, chunk_overlap, refine_prompt, basic_prompt, uploaded_file, submit_button, openai_api_key

def copy_to_clipboard_button(col2):
    if col2.button('Copy to Clipboard'):
        pyperclip.copy(st.session_state.get('output_text', ""))
        col2.success('Text copied to clipboard!')

import streamlit as st
import ui
import logic
import file_handling

def main():
    ui.set_page()
    input_text, run_button, output_text, col2 = ui.input_output_columns()
    chunk_size, chunk_overlap, refine_prompt, basic_prompt, uploaded_file, submit_button, openai_api_key = ui.sidebar_config()
    
    if submit_button:
        try:
            essay = file_handling.read_uploaded_file(uploaded_file)
            st.session_state['input_text'] = essay
            st.rerun()
        except Exception as e:
            st.error(f"Error reading file: {str(e)}")
    
    if run_button:
        with st.spinner('Processing...'):
            try:
                result_text = logic.run_logic(uploaded_file, input_text, chunk_size, chunk_overlap, basic_prompt, refine_prompt, openai_api_key)
                st.session_state['output_text'] = result_text
                st.rerun()
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

    ui.copy_to_clipboard_button(col2)

if __name__ == "__main__":
    main()

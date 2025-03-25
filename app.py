import streamlit as st
import agent
from content_etl import save_code_to_file as sctf
from content_etl import extract_code as ec
from content_etl import extract_from_buffer_file as ebf
from content_etl import extract_from_possible_file as epf
from prompt import code_debugger_prompts as cdp
from prompt import find_content as fc
from prompt import format_fixers as ff
import time

@st.cache_resource(show_spinner=False)
def load_agent():
    return agent

def fix_format(file,exception):
    agent = load_agent()
    with open(file, 'r',encoding='utf-8') as f:
        data = f.read()
    response= agent.code_gem_debugger(ff.fix_format(data,exception,file_type="json"))
    with open(file, 'w', encoding='utf-8') as f:
        f.write(ec(response, 'json'))

def code_debugger(code, error):
    try:
        agent = load_agent()
        response = agent.code_gem_debugger(cdp.code_with_explanation(code, error))
        st.write(response)
        with open(r'responses\correct_code.json', 'w', encoding='utf-8') as f:
            f.write(ec(response, 'json'))

        try:
            data=ebf(r'responses\correct_code.json')
    
        except Exception as e:
            fix_format(r'responses\correct_code.json',e)
            data=ebf(r'responses\correct_code.json')
        
        return data
        
    except Exception as e:
        st.error(f"An error occurred while debugging the code: {e}")
        return None

    

def file_finder(files_list, error, excluded_files):
    try:
        agent = load_agent()
        possible_file = agent.code_gem_debugger(fc.find_appropriate_file(files_list, error, excluded_files))
        with open(r'responses\possible_file.json', 'w', encoding='utf-8') as f:
            f.write(ec(possible_file, 'json'))
        try:
            data=epf(r'responses\possible_file.json')
        except Exception as e:
            fix_format(r'responses\possible_file.json',e)
            data=epf(r'responses\possible_file.json')
        
        return data
    except Exception as e:
        st.error(f"An error occurred while finding the possible file: {e}")
        return None

if 'response' not in st.session_state:
    st.session_state['response'] = None
if 'code_file_name' not in st.session_state:
    st.session_state['code_file_name'] = None
if 'excluded_files' not in st.session_state:
    st.session_state['excluded_files'] = []

st.title('ML-Model Debugger 🗨️🔗💻...')
option = st.sidebar.selectbox('Select the Agent', ['Model Debugger','code Debugger'])

if option == 'code Debugger':
    st.sidebar.write("\n ")
    st.sidebar.write("\n ")
    st.sidebar.header('Code Debugger')

    st.write("*To implement changes in the file check the checkbox before submitting*")
    st.write("\n")
    implement_changes = st.checkbox('Implement Changes')
    code_file = st.sidebar.file_uploader('Upload the code file', accept_multiple_files=False)
    error = st.text_input('Enter your error', placeholder='Optional')

    if st.button('Submit'):
        with st.spinner("Generating response..."):
            try:
                time.sleep(2)

                code = code_file.read().decode('utf-8')
                code_data = code_debugger(code, error)
                if code_data:
                    st.header("Explanation 📝")
                    st.write(code_data["explanation"])

                    st.header("Corrected Code 🛠️")
                    st.write(f"```{code_data['file_type']}\n{ec(code_data['corrected_code'])}\n```")

                    if code_data['suggestions'] is not None:
                        st.header("Suggestions 💡")
                        st.write(code_data["suggestions"])

                    if implement_changes and code_data["error_flag"]:
                        sctf(code_file.name, ec(code_data["corrected_code"], code_data["file_type"]))
                        st.success(f"Changes have been implemented to {code_file.name}")
            except Exception as e:
                st.error(f"An error occurred while processing the code: {e}")

elif option == 'Model Debugger':
    st.sidebar.write("\n ")
    st.sidebar.write("\n ")
    st.sidebar.header('Model Debugger')
    code_files = st.sidebar.file_uploader('Upload the code files', accept_multiple_files=True)
    st.write("** *Refresh page and Re-Upload before submitting again* **")
    st.write("*To implement changes in the file check the checkbox before submitting*")
    st.write("\n")
    implement_changes = st.checkbox('Implement Changes')

    error = st.text_input('Enter your error')

    placeholder = st.empty()

    if st.button('submit'):
        with st.spinner("Generating response..."):
            try:

                time.sleep(2)

                files = [code_file.name for code_file in code_files]
                file_dict = {file_name: index for index, file_name in enumerate(files)}
                possible_file = file_finder(files, error, st.session_state['excluded_files'])
                if possible_file:
                    file_name = possible_file['most_probable_file']
                    code = code_files[file_dict[file_name]].read().decode('utf-8')
                    placeholder.write(f"Most probable file to contain given error is {file_name}")
                    st.session_state['excluded_files'].append(file_name)
                    code_data = code_debugger(code, error)
                    if code_data:
                        while not code_data["error_flag"]:
                            placeholder.write(f"No errors found in {file_name}")

                            possible_file = file_finder(files, error, st.session_state['excluded_files'])
                            if possible_file:
                                file_name = possible_file['most_probable_file']
                                code = code_files[file_dict[file_name]].read().decode('utf-8')
                                placeholder.write(f"Most probable file to contain given error is {file_name}")
                                st.session_state['excluded_files'].append(file_name)
                                code_data = code_debugger(code, error)
                                
                        placeholder.write(f"Errors found in {file_name}")
                        time.sleep(3)
                        placeholder.empty()

                        st.header("Explanation 📝")
                        st.write(code_data["explanation"])

                        st.header("Corrected Code 🛠️")
                        st.write(f"```{code_data['file_type']}\n{ec(code_data['corrected_code'])}\n```")

                        if code_data['suggestions'] is not None:
                            st.header("Suggestions 💡")
                            st.write(code_data["suggestions"])

                        if implement_changes and code_data["error_flag"]:
                            sctf(code_files[file_dict[file_name]].name, ec(code_data["corrected_code"], code_data["file_type"]))
                            st.success(f"Changes have been implemented to {code_files[file_dict[file_name]].name}")
            except Exception as e:
                st.error(f"An error occurred while processing the files: {e}")

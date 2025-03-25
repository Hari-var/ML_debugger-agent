import agent
from content_etl import extract_code as ec
from content_etl import extract_from_possible_file as epf
from content_etl import extract_from_buffer_file as ebf
from prompt import code_debugger_prompts as cdp
from prompt import find_content as fc
from prompt import format_fixers as ff
import file_structure_retriver as fsr



def load_agent():
    return agent

def fix_format(file,exception):
    agent = load_agent()
    with open(file, 'r',encoding='utf-8') as f:
        data = f.read()
    response= agent.code_gem_debugger(ff.fix_format(data,exception,file_type="json"))
    with open(file, 'w', encoding='utf-8') as f:
        f.write(ec(response, 'json'))

def debug_code(code_file_path,error):
    with open(code_file_path, 'r', encoding='utf-8') as f:
        code=f.read()
    response=agent.code_gem_debugger(cdp.code_with_explanation(code,error))
    with open(r'responses\buffer.json','w') as f:
        f.write(ec(response,'json'))
    try:
        data=ebf(r'responses\buffer.json')

    except Exception as e:
        fix_format(r'responses\buffer.json',e)
        data=ebf(r'responses\buffer.json')

    return data

def find_possible_file(structure,error,excluded_files):
    possible_file_structure=agent.code_gem_debugger(fc.find_appropriate_file_structure(structure,error,excluded_files))
    with open(r'responses\possible_file_structure.json','w') as f:
        f.write(ec(possible_file_structure,'json'))
    
    try:
        data=epf(r'responses\possible_file.json')
    except Exception as e:
        fix_format(r'responses\possible_file.json',e)
        data=epf(r'responses\possible_file.json')

    return data

def code_debugger():
    code_file_path =input('Enter the path of the code file: ')
    error=input('\nEnter the error: ')
    code_data=debug_code(code_file_path,error)
    print("\n******  CORRECTED CODE ********\n")
    print(code_data['corrected_code'])
    print("\n\n******  EXPLANATION ********\n")
    print(code_data['explanation'])
    print("\n\n******  SUGGESTIONS ********\n")
    print(code_data['suggestions'])

    print("\n\nwould you like to implement the changes?")
    implement_changes=input("Enter y/n: ")
    if implement_changes.lower()=='y':
        with open(code_file_path, 'w') as f:
            f.write((code_data['corrected_code'],code_data["file_type"]))
        print(f"\n\n****** Successfully implemented the changes to {code_file_path} ******\n\nn")
    
    else:
        print("\n\n")

def model_debugger():
    folder_path=input('Enter the path of the folder: ')
    error=input('\nEnter the error: ')
    structure=fsr.directory_contents(folder_path)
    excluded_files=[]

    possible_file=find_possible_file(structure,error,excluded_files)
    file_name=possible_file['most_probable_file']
    print(f"\nMost probable file to contain given error is {file_name}\n")

    excluded_files.append(file_name)

    code_data=debug_code(folder_path+'\\'+file_name,error)
    while not code_data['error_flag']:
    # for i in range(5):
        print(f"No errors found in {file_name}\n")
        possible_file=find_possible_file(structure,error,excluded_files)
        file_name=possible_file['most_probable_file']
        print(f"Most probable file to contain given error is {file_name}\n")
        excluded_files.append(file_name)
        code_data=debug_code(folder_path+'\\'+file_name,error)

    print(f"Errors found in {file_name}\n")
    print("\n******  CORRECTED CODE ********\n")
    print(code_data['corrected_code'])
    print("\n\n******  EXPLANATION ********\n")
    print(code_data['explanation'])
    print("\n\n******  SUGGESTIONS ********\n")
    print(code_data['suggestions'])

    print("\n\nwould you like to implement the changes?")
    implement_changes=input("Enter y/n: ")
    if implement_changes.lower()=='y':
        with open(folder_path+'\\'+file_name, 'w') as f:
            f.write(ec(code_data['corrected_code'],code_data["file_type"]))
        print(f"\n\n****** Successfully implemented the changes to {folder_path+'\\'+file_name} ******\n\n")
    else:
        print("\n\n")

if __name__ == "__main__":
    while True:
        option = input('Select the Agent:\n1 -> Code Debugger\n2-> Model Debugger\n\n**q to quit**\n\n')
        if option.lower() in ['1','code debugger']:
            code_debugger()
            # print('Code Debugger')
        elif option.lower() in ['2','model debugger']:
            model_debugger()
            # print('Model Debugger')
        elif option == 'q':
            exit()
        else:
            print('Invalid option. Please try again.\n\n')
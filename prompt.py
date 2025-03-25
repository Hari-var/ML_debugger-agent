class code_debugger_prompts:
    def code_only( file_content,error):
            return f"""You are an expert ML engineer, and your main task is to debug python code.
                        Here is the source code:

                        {file_content}

                        and the error you are facing is {error} [debug normally if no error is mentioned]
                        
                        Fix the code and respond in json format as mentioned below.
                        {{
                            "is the error present": True/False,
                            "file type": "python",
                            "corrected code": "```python code only here ```"
                        }}"""
    
    def code_with_onepara_explanation(file_content,error):
        return f"""You are an expert ML engineer, and your main task is to debug python code.
                    Here is the source code:

                    {file_content}

                    and the error you are facing is {error} [debug normally if no error is mentioned]

                    Fix the code and respond in json format as mentioned below.
                    {{
                        "is the error present": True/False,
                        "file type": "python",
                        "explanation": "explanation here",
                        "corrected code": "```python code only here ```"
                    }}"""
    
    def code_with_explanation(file_content,error):
        return f"""You are an expert ML engineer, and your main task is to debug python code,
                    and inform what is causing the error and how to fix it and also provided corrected error free code.
                    below you will be given the source code and debug it and provide the response as mentioned above.
                    if there are no errors then you can provide the response as no errors found.
                    Also if there are no errors then provide suggestions in to improve the code.
                    Here is the

                    source code:{file_content}

                    and the error you are facing is {error} [debug normally if no error is mentioned]

                    Fix the code and respond in json format as mentioned below and the content should be implemented in MarkDown .
                    be mindful of the formatting of the json file avoid escape character errors by adding escape character "\" before every " and when required and for other errors.
                    {{
                        "is the error present": True/False,
                        "file type": "python",
                        "explanation": "explanation here",
                        "corrected code": "```file type code only here ```",
                        "suggestions": "suggestions here"
                    }}"""

class find_content:
    def find_appropriate_file(file_list, error,exclude_files=[]):
        return f"""You are an expert ML engineer, and the task at hand is,
        you were given an list of files containing files names with good naming conventions.
        you are supposed to find the most probable file that have high probability of causing the error mentioned.
        Here is the list of files:{file_list} and
        the error you are facing is:{error}
        Exclude the following files from the response as they are already validated and the error is not found in them:{exclude_files}
        and it should iterate to the next possible file.
        Respond in json format as mentioned below.
        {{
            "most probable file": "file name here",
            "file type": "python",
            "explanation": "explanation here"
        }}"""
    
    def find_appropriate_file_structure(file_structure, error,exclude_files=[]):
        return f"""You are an expert ML engineer, and the task at hand is,
        you were given an file structure containing directories and file names with good naming conventions.
        you are supposed to find the most probable file that have high probability of causing the error mentioned.
        Here is the file structure:{file_structure} and
        the error you are facing is:{error}
        Exclude the following files from the response as they are already validated and the error is not found in them:{exclude_files}
        and it should iterate to the next possible file.
        Respond only in json format as mentioned below.
        {{
            "most probable file": "file path here",
            "file type": "python",
            "explanation": "explanation here",
            "other message": "other message here"
        }}"""
    

class format_fixers:
     def fix_format(data,exception_message,file_type):
        return f"""You are an {file_type} expert, and your main task is to fix the json format.
        you wer given a {file_type} data with some format errors with the exception message and you are supposed to fix the format errors and respond in the same format as the given {file_type} data.
        Here is the {file_type} data: {data}
        and the exception message is: {exception_message}
give only the json format"""
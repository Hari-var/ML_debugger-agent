import json

def save_code_to_file(file,code,file_type="python"):
	with open(file, 'w',encoding='utf-8') as f:
		f.write(code)

def extract_code(response, file_type="python"):
	response = response.strip().strip(f"```{file_type}").strip().strip("```").strip()
	return response
		
def extract_from_buffer_file(json_file_path):
	with open(json_file_path, 'r',encoding='utf-8') as file:
		data = json.load(file)
	
	error_flag = data.get('is the error present', None)
	corrected_code = data.get('corrected code', None)
	explanation = data.get('explanation', None)
	file_type = data.get('file type', None)
	suggestions = data.get('suggestions', None)
	
	return {
		"error_flag": error_flag,
		"file_type": file_type,
		"corrected_code": corrected_code,
		"explanation": explanation,
        "suggestions": suggestions
	}


def extract_from_possible_file(json_file_path):
    with open(json_file_path, 'r',encoding='utf-8') as file:
        data = json.load(file)
    file_type = data.get('file type', None)

    explanation = data.get('explanation', None)
    most_probable_file = data.get('most probable file', None)
    other_message = data.get('other message', None)

    return {
		"most_probable_file": most_probable_file,
		"file_type": file_type,
		"explanation": explanation,
		"other_message": other_message
	}

if __name__ == "__main__":
	data=extract_from_buffer_file("buffer.json")
	save_code_to_file("ML_code.py",data["corrected_code"],data["file_type"])
	

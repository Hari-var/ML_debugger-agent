from huggingface_hub import InferenceClient
import os
from google import generativeai as genai  # Correct import alias
import os
import anthropic
from transformers import pipeline


def code_hf_debugger(prompt):
    client = InferenceClient(
        provider="novita",
        api_key=os.environ["hugging_face_API"]
    )
    print(os.environ["hugging_face_API"])  #Good for debugging

    try:
        response = client.post(prompt=prompt, model="deepseek-ai/DeepSeek-V3", max_tokens=100)
        return response
    except Exception as e:
        print(f"Error during Hugging Face inference: {e}")
        return None


def code_gem_debugger(prompt):
    API_KEY = os.environ["gemini_API3"]
    genai.configure(api_key=API_KEY)  # Configure the gemini ai
    model = genai.GenerativeModel("gemini-2.0-pro-exp-02-05") # Correct way to get the model
    try:
        response = model.generate_content(prompt) # Correct way to generate content.
        return response.text
    except Exception as e:
        print(f"Error during Gemini inference: {e}")
        return None
    
'''def code_ai21_debugger(prompt):
    response = client.chat.completions.create(
        model="jamba-large",  # Latest model
        messages=[ChatMessage(   # Single message with a single prompt
            role="user",
            content="Write a product title for a sports T-shirt to be published on an online retail platform. Include the following keywords: activewear, gym, dryfit."
    )],
        temperature=0.8,
        max_tokens=200 # You can also mention a max length in the prompt "limit responses to twenty words"
    )'''
def code_claude_debugger(prompt):

    client = anthropic.Anthropic(
        # defaults to os.environ.get("ANTHROPIC_API_KEY")
        api_key=os.environ["claude_API"],
    )
    message = client.messages.create(
        model="Claude 3 Haiku",
        max_tokens=1024,
        messages=[
            {"role": "user", "content": "Hello, Claude"}
        ]
    )
    return (message.content)


if __name__ == "__main__":
    print(code_claude_debugger("print(x for x in range(10))"))

def deepseek_coder_base(prompt):

    messages = [
        {"role": "user", "content": prompt},
    ]
    pipe = pipeline("text-generation", 
                    model="deepseek-ai/DeepSeek-Coder-V2-Base", 
                    trust_remote_code=True)
    return pipe(messages)

import boto3
import base64
import json
import re

from IPython.display import Markdown, display
import docx
from IPython.display import Markdown, display
import os
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import time
import streamlit as st

import botocore
config = botocore.config.Config(read_timeout=900, connect_timeout=900, retries={"max_attempts": 1})
session = boto3.Session()
bedrock_runtime = session.client("bedrock-runtime", config=config, region_name='us-east-1')


class Analyticsfunction:
    def __init__(self):
        pass

    def convert_image_to_base64(self, image_path):
        self.image_path = image_path
        with open(self.image_path, "rb") as image_file:
            image_bytes = image_file.read()
            base64_string = base64.b64encode(image_bytes).decode('utf-8')
        return base64_string

    def call_claude_sonet(self, base64_string, question):
        self.question = question
        self.base64_string = base64_string

        prompt_config = {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 4096,
                "temperature": 0.0,
                "top_k": 250,
                "top_p": 1,
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image",
                                "source": {
                                    "type": "base64",
                                    "media_type": "image/png",
                                    "data": base64_string,
                                },
                            },
                            {"type": "text", "text": question},
                        ],
                    }
                ],
            }


        body = json.dumps(prompt_config)
        modelId = "anthropic.claude-3-sonnet-20240229-v1:0"
        accept = "application/json"
        contentType = "application/json"


        response = bedrock_runtime.invoke_model(body=body, modelId=modelId, accept=accept, contentType=contentType)
        response_body = json.loads(response.get("body").read())
        results = response_body.get("content")[0].get("text")
        return results
    
    def call_claude_sonet_text(self, question):
        self.question = question
        prompt_config = {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 3000,
                "temperature": 0.7,
                "top_k": 50,
                "top_p": 0.9,
                "messages": [
                    {
                        "role": "user",
                        "content": [
                        
                            {"type": "text", 
                             "text": question},
                        ],
                    }
                ],
            }


        body = json.dumps(prompt_config)
        modelId = "anthropic.claude-3-sonnet-20240229-v1:0"
        accept = "application/json"
        contentType = "application/json"


        response = bedrock_runtime.invoke_model(body=body, modelId=modelId, accept=accept, contentType=contentType)
        response_body = json.loads(response.get("body").read())
        results = response_body.get("content")[0].get("text")
        #out = display(Markdown(results))
        return results
    

    def claude2(self, question):
        self.question = question

        modelId = "anthropic.claude-v2:1"  # change this to use a different version from the model provider
        accept = "application/json"
        contentType = "application/json"
        
        body = json.dumps({"prompt": self.question, "max_tokens_to_sample": 1000, "temperature": 0.8})

        response = bedrock_runtime.invoke_model(body=body, modelId=modelId, accept=accept, contentType=contentType)
        response_body = json.loads(response.get("body").read())
        #print(response_body.get("completion"))
        return response_body.get("completion")
    


    
class mathquestion(Analyticsfunction):
    def __init__(self):
        pass

    def extract_python_code(self, input_text, output_file):
        self.input_text = input_text
        self.output_file = output_file
        # Regular expression pattern to match Python code blocks
        python_pattern = r'```python\n(.*?)```'
        # Find all Python code blocks using regex
        python_blocks = re.findall(python_pattern, self.input_text, re.DOTALL)
        # Write Python code blocks to the output file
        with open(self.output_file, 'w') as f:
            for code_block in python_blocks:
                f.write(code_block.strip() + '\n\n')

            
    def detect_shape(self, question):
        self.question = question
        
        prompt = f'''Human: find out the math image shape from question and in one word only
        some example of question and asnwer is given below
        question = "ABCDEF is a hexagon (six-sided polygon). Find the value of AB+BC+CD+DE+AF+FE+AE "
        answer = "hexagon"

        question = "If the adjacent sides of a parallelogram are 3i+2j and -i+4j+2k, find the area of the       parallelogram."
        answer = "parallelogram"

        <question>
        {self.question}
        </question>
        please answer only the type of shape example of shape like hexagon, traingle, circle. plane, line 
        response must be one word only

        Assistant:'''
        body = json.dumps({"prompt": prompt})

        text = self.call_claude_sonet_text(body) 
        return text
    
    
    def create_image(self, question):
        self.question = question
        shape  = self.detect_shape(self.question)
        prompt = f'''Human: write simple python code to draw {shape} for generating image for the {question} using seaborn for visualisation
                    1. Save plot as {shape}.jpg, plot context/question at top.create small image
                    2. context into the image at top. 
                    3. draw correct shape for {shape}
                    4. complete all edges and align properly for {shape}
                    5. Label each edge with (e.g., A, B, etc.) for better understanding.
                    6. import all necessary libraries and functions.
                    7. write code to draw {shape}
                    8. code should be 100% accurate
    
                    Assistant:'''
     
   
        body = json.dumps({"prompt": prompt})
        text = self.call_claude_sonet_text(body)
        #print(text)
        #text = claude2(prompt)
        image = f'{shape}'
        output_file = "main.py"
        self.extract_python_code(text, output_file)
        time.sleep(4)
        #display(Markdown(text))
        os.system("python3 main.py")
        time.sleep(5)
          # Wait for 5 seconds to allow the image to be generated
        img = mpimg.imread(shape+".jpg")
        # Display the image on Streamlit UI
        # plt.imshow(img)
        # plt.axis('off')  # Hide axis ticks and labels
        # plt.show()
        st.image(img, caption=question, use_column_width=True)

    def getText(self, filename):
        self.filename = filename
        doc = docx.Document(self.filename)
        fullText = []
        for para in doc.paragraphs:
            fullText.append(para.text)
        return '\n'.join(fullText)
    
    
    # def question_answer_generation_image(self,image, note):
    #     self.note = note
    #     self.image = image

    #     base64 = self.convert_image_to_base64(self.image)
    #     body = json.dumps({"prompt": note, "max_tokens_to_sample": 1000, "temperature": 0.8})
    #     text = self.call_claude_sonet(base64, body)
    #     display(Markdown(text))
    
    
    def question_answer_generation(self, note):
        self.note = note
        text = self.call_claude_sonet_text(self.note)
        display(Markdown(text))
        return text
    

    def create_summary(self, note):
        self.note = note

        prompt = f'''Human: create summary of the document in 1000 words.These are education related video, during summarisation please dont change the original context. 
        <book>
        {self.note}
        </book>

        Assistant:'''

        body = json.dumps({"prompt": prompt})
        text = self.call_claude_sonet_text(body)
        display(Markdown(text))
        return text
    




import boto3
import base64
import json
bedrock_runtime = boto3.client('bedrock-runtime',region_name='us-east-1')


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


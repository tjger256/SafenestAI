import boto3
import json
from botocore.exceptions import ClientError

MODEL_ID = "anthropic.claude-3-5-sonnet-20240620-v1:0"

IMAGE_NAME = "AI Processes/image0.jpg"

bedrock_runtime = boto3.client("bedrock-runtime", region_name="us-east-1")

with open(IMAGE_NAME, "rb") as f:
    image = f.read()

#user_message = "Is this baby in danger? Give a danger level between 1-5. Output in JSON."


ml_prompt = f"""
    Examine this picture and check for dangerous enviromental factors
    Evaulate each of the dangerous enviormental factors on their threat to the baby
    Give a score between 1-10 representing the probability of the baby sustaining an injury from the enviroment
    Also make the output sound as if you're talking to the baby's parents.
    For "Enviromental_Factors" we want to generate one for each of the dangerous factors found in the picture. 
    Answer strictly in the following JSON format. Do not change the keys. Just return the JSON string.
    - {json.dumps({
    "risk_probability": "Probability of the baby sustaining an injury from the enviroment (value from 1 to 10)",
    "assessment":"Basic assessment given the probability and the baby's enviroment. Should recommend to fix",
    "Enviromental_Factors" : [ {
        "Factor_Name": "This is the name of the enviromental factor",
        "Threat_Summary": "summary of the danger this factor poses to the baby",
        "Preventitaive action": [
            {
            "task": "name of the task",
            "task_description": "detailed description of the action to be taken to eliminate or reduce threat of the enviromental factor",
            },
            "..."
        ]
    }, "..."
    ]
})} 
    """

messages = [
    {
        "role": "user",
        "content": [
            {"image": {"format": "png", "source": {"bytes": image}}},
            {"text": ml_prompt},
        ],
    }
]

response = bedrock_runtime.converse(
    modelId=MODEL_ID,
    messages=messages,
)
response_text = type(response["output"]["message"]["content"][0]["text"])
print(response_text)



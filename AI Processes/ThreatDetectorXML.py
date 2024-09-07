import boto3
import json
from xml.dom.minidom import parseString
import xml.etree.ElementTree as ET
from botocore.exceptions import ClientError

MODEL_ID = "anthropic.claude-3-5-sonnet-20240620-v1:0"
IMAGE_NAME = "AI Processes/image0.jpg"

bedrock_runtime = boto3.client("bedrock-runtime", region_name="us-east-1")

with open(IMAGE_NAME, "rb") as f:
    image = f.read()

ml_prompt = """
Assess the picture and identify potential hazards that could impact the baby, including factors such as:
Choking, Electrical shock, Hard Falling (e.g., falling from a high table or chair), Suffocation, and Sharp Objects (e.g., knife, saw).
For each hazard, provide a rating from 1 (lowest) to 5 (highest) to indicate the level of risk to the baby in the picture.
The output will only be in XML format, containing only the results without any explanation.
Here is an example of the output:
<hazard_assessment>
    <choking>5</choking>
    <electrical_shock>5</electrical_shock>
    <hard_falling>1</hard_falling>
    <suffocation>3</suffocation>
    <sharp_objects>1</sharp_objects>
</hazard_assessment>
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
response_text = response["output"]["message"]["content"][0]["text"]

# Ensure the response text is wrapped in a single root element
if not response_text.strip().startswith("<hazard_assessment>"):
    wrapped_response_text = f"<hazard_assessment>{response_text}</hazard_assessment>"
else:
    wrapped_response_text = response_text

# Parse the wrapped_response_text into an XML element using xml.dom.minidom
try:
    dom = parseString(wrapped_response_text)
      # This confirms the type as xml.dom.minidom.Document
    print(dom.toprettyxml())  # This prints the actual XML content
except Exception as e:
    print(f"Failed to parse XML: {e}")
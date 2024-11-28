import openai
import os
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Set the API key, base URL, and version for Azure OpenAI
openai.api_key = os.environ["AZURE_OPENAI_KEY"]
openai.api_base = os.environ["AZURE_OPENAI_ENDPOINT"]  # Example: "https://your-openai-resource-name.openai.azure.com/"
openai.api_type = "azure"
openai.api_version = os.environ["AZURE_OPENAI_VERSION"]  # Example: "2023-03-15-preview"

# Set your deployment (model) ID
deployment = os.environ['AZURE_OPENAI_DEPLOYMENT']  # Example: "gpt-35-turbo"

template = (
    "You are tasked with extracting specific information from the following text content: {dom_content}. "
    "Please follow these instructions carefully: \n\n"
    "1. **Extract Information:** Only extract the information that directly matches the provided description: {parse_description}. "
    "2. **No Extra Content:** Do not include any additional text, comments, or explanations in your response. "
    "3. **Empty Response:** If no information matches the description, return an empty string ('')."
    "4. **Direct Data Only:** Your output should contain only the data that is explicitly requested, with no other text."
)

def parse_with_azureai(dom_chunks, parse_description):
    prompt = ChatPromptTemplate.from_template(template)
    parsed_results = []
    for i, chunk in enumerate(dom_chunks, start=1):
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt.format(dom_content = chunk, parse_description = parse_description)}
        ]
        completion = openai.chat.completions.create(model=deployment, messages=messages)
        response = completion.choices[0].message.content
        print(f"Parsed batch {i}: {response}")
        parsed_results.append(response)

    return "\n".join(parsed_results)
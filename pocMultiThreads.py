import openai
from dotenv import load_dotenv
import os
load_dotenv()

OPENAI_KEY      = os.getenv('OPENAI_KEY')
OPENAI_ORGANIZATION = os.getenv('OPENAI_ORGANIZATION')


openai.api_key = OPENAI_KEY
openai.organization = OPENAI_ORGANIZATION
response = openai.Completion.create(
    engine="text-davinci-002",
    prompt="cuanto es 2 + 2?",
    temperature=0.5,
    max_tokens=256,
    top_p=1.0,
    frequency_penalty=0,
    presence_penalty=0
)

print(response['choices'][0]['text'])
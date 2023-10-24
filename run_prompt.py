import time
import configparser
import os
import openai
import json

__OUTPUT_DIR = 'output_pdf'
__CONTENT_PROMPT_LENGTH = 4000

prompt_template = """
Based on the following content from the document "{pdf_name}", identify all sections related to taxes. 
For each section, provide a citation with the relevant text and page number. 
Additionally, evaluate if the content suggests the party is in favor or against raising taxes on driving cars.

The content to be evaluated is:
"""

config_parser = configparser.ConfigParser()
config_parser.read('openaiconfig.ini')
openai_secret = config_parser['keys']['openaikey']
openai.api_key = openai_secret

with open('docs/extracted_texts.json', 'r', encoding='utf-8') as json_file:
    pdf_texts = json.load(json_file)

if not os.path.exists(__OUTPUT_DIR):
    os.makedirs(__OUTPUT_DIR)

for pdf_name, data in pdf_texts.items():
    print(pdf_name)
    base_file_name = os.path.splitext(pdf_name)[0]
    text = ""
    for page_data in data:
        text += f"Page {page_data['page_number']}:\n{page_data['text']}\n\n"

    text_parts = [text[i * __CONTENT_PROMPT_LENGTH:(i + 1) * __CONTENT_PROMPT_LENGTH] for i in range((len(text) + __CONTENT_PROMPT_LENGTH - 1) // __CONTENT_PROMPT_LENGTH)]

    for idx, part in enumerate(text_parts):
        outfile = os.path.join(__OUTPUT_DIR, f"{base_file_name}-{idx:04d}.txt")
        if not os.path.exists(outfile):
            retry_count = 3
            for _ in range(retry_count):
                try:
                    print('calling OpenAI')
                    response = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo-16k",
                        messages=[
                            {
                                "role": "user",
                                "content": prompt_template.format(pdf_name=pdf_name) + part
                            }
                        ],
                        temperature=0.5,
                        max_tokens=12000,
                        top_p=1,
                        frequency_penalty=0,
                        presence_penalty=0
                    )

                    print('writing files')
                    with open(outfile, 'w') as f:
                        result = response['choices'][0]['message']['content']
                        f.write(result)
                    break  # If the API call is successful, break out of the retry loop
                except openai.error.RateLimitError as e:
                    print(f"Rate limit error: {e}. Waiting for a few seconds before retrying...")
                    time.sleep(5)
                except openai.error.Timeout:
                    print("Request timed out. Waiting for a few seconds before retrying...")
                    time.sleep(5)
        else:
            print("output file exists, skipping")

    print('\n')

import json
import os
from PyPDF2 import PdfReader

def clean_non_ascii(text):
    return ''.join(i if ord(i) < 128 else ' ' for i in text)  # Replacing non-ASCII characters with a space

def extract_text_from_pdfs(folder_path):
    pdf_texts = {}

    # List all files in the folder
    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f)) and f.endswith('.pdf')]

    for pdffile in sorted(files):
        pdf_path = os.path.join(folder_path, pdffile)
        with open(pdf_path, 'rb') as f:
            pdf = PdfReader(f)
            pdf_data = []

            for page_num, page in enumerate(pdf.pages):
                pdf_data.append({
                    'page_number': page_num + 1,
                    'text': page.extract_text()
                })

            pdf_texts[pdffile] = pdf_data

    return pdf_texts

# Test the function
folder_path = 'docs'  # Replace with the path to your folder containing the PDFs
pdf_texts = extract_text_from_pdfs(folder_path)
for pdf_name, data in pdf_texts.items():
    print(f"Extracted from {pdf_name}:")
    for page_data in data:
        clean_text = clean_non_ascii(page_data['text'])
        print(f"Page {page_data['page_number']}: {clean_text[:100]}...")
    print("\n")

# Save the extracted text to a JSON file
with open('docs\extracted_texts.json', 'w', encoding='utf-8') as json_file:
    json.dump(pdf_texts, json_file, ensure_ascii=False, indent=4)

import os
import docx

docs_dir = '_docs'
output_file = 'extracted_texts.txt'

with open(output_file, 'w', encoding='utf-8') as out:
    for filename in os.listdir(docs_dir):
        if filename.endswith('.docx') and not filename.startswith('~'):
            filepath = os.path.join(docs_dir, filename)
            if os.path.getsize(filepath) == 0:
                print(f"Skipping empty file: {filename}")
                continue
            try:
                doc = docx.Document(filepath)
                out.write(f"--- {filename} ---\n")
                for para in doc.paragraphs:
                    if para.text.strip():
                        out.write(para.text + "\n")
                out.write("\n\n")
            except Exception as e:
                print(f"Error reading {filename}: {e}")

print(f"Extraction complete. Results saved to {output_file}")

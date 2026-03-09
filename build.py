import os
import json
import re
import shutil

# Configuration
TEXT_FILE = 'extracted_texts.txt'
SRC_DIR = 'src'
PUBLIC_DIR = 'public'
TEMPLATE_INDEX = os.path.join(SRC_DIR, 'index_template.html')
TEMPLATE_STYLE = os.path.join(SRC_DIR, 'style_template.html')
TEMPLATE_MENU = os.path.join(SRC_DIR, 'includes', 'menu.html')

def parse_texts():
    """Parses the extracted text file into a list of dictionaries."""
    with open(TEXT_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    # Split documents by the '--- filename ---' delimiter
    docsRaw = re.split(r'---\s*(.*?)\s*---', content)
    docs = []
    
    # docsRaw[0] is empty or whitespace. The rest are in pairs: [filename, text, filename, text...]
    for i in range(1, len(docsRaw), 2):
        filename = docsRaw[i].strip()
        textRaw = docsRaw[i+1].strip()
        
        # We need to parse the document into title, description, and examples
        lines = [line.strip() for line in textRaw.split('\n') if line.strip()]
        
        if not lines:
            continue
            
        title = lines[0]
        
        # Find the line that says "Example tones for different IT experiences:"
        example_start_idx = -1
        reflection_end_idx = len(lines)
        
        for j, line in enumerate(lines):
            if "Example tones" in line:
                example_start_idx = j
                break
            if "Your submission should be" in line:
                reflection_end_idx = j
                break
                
        if example_start_idx != -1:
            desc_lines = lines[1:example_start_idx]
        else:
            desc_lines = lines[1:reflection_end_idx]
            
        description = "<br><br>".join(desc_lines)
        
        examples = {}
        if example_start_idx != -1:
            # We have examples. Let's parse them.
            current_category = None
            current_example_lines = []
            
            for line in lines[example_start_idx+1:]:
                if "Your submission should be" in line:
                    if current_category:
                        examples[current_category] = "<br>".join(current_example_lines)
                    break
                    
                # A category usually doesn't end with a period, while example sentences do
                if not line.endswith('.') and not line.endswith('!') and len(line.split()) < 6:
                    if current_category:
                        examples[current_category] = "<br>".join(current_example_lines)
                    current_category = line
                    current_example_lines = []
                else:
                    if current_category:
                        current_example_lines.append(line)
                        
        # Basic ID creation from title
        doc_id = title.replace("Weekly Lab Reflection \u2013 ", "").replace("Weekly Lab Reflection - ", "").replace(" ", "-").lower()
        if not doc_id:
             doc_id = "unknown"
             
        docs.append({
            'id': doc_id,
            'title': title,
            'description': description,
            'examples': examples,
            'filename': filename
        })
        
    return docs

def build_menu(docs):
    """Generates the HTML for the sidebar menu"""
    menu_html = '<div class="list-group list-group-flush rounded shadow-sm">\n'
    menu_html += '  <a href="index.html" class="list-group-item list-group-item-action bg-dark text-light border-secondary"><i class="bi bi-house-door me-2"></i>Home</a>\n'
    for doc in docs:
        menu_html += f'  <a href="{doc["id"]}.html" class="list-group-item list-group-item-action bg-dark text-light border-secondary"><i class="bi bi-file-earmark-text me-2"></i>{doc["title"].replace("Weekly Lab Reflection \u2013 ", "")}</a>\n'
    menu_html += '</div>\n'
    return menu_html

def generate_site():
    print("Starting build process...")
    
    # 1. Ensure public dir exists
    if not os.path.exists(PUBLIC_DIR):
        os.makedirs(PUBLIC_DIR)
        
    # 2. Copy CSS
    shutil.copy(os.path.join(SRC_DIR, 'style.css'), os.path.join(PUBLIC_DIR, 'style.css'))
    
    # 3. Parse Data
    docs = parse_texts()
    
    # 4. Generate Menu
    menu_html = build_menu(docs)
    
    # 5. Build Index Page
    with open(TEMPLATE_INDEX, 'r', encoding='utf-8') as f:
        idx_template = f.read()
        
    # Generate cards for index
    cards_html = ""
    for doc in docs:
        short_title = doc["title"].replace("Weekly Lab Reflection \u2013 ", "").replace("Weekly Lab Reflection - ", "")
        short_desc = doc["description"].split("<br>")[0][:120] + "..." if len(doc["description"]) > 120 else doc["description"]
        cards_html += f"""
        <div class="col-md-6 col-lg-4 mb-4">
            <div class="card h-100 style-card shadow-sm border-0">
                <div class="card-body">
                    <h5 class="card-title text-primary-accent fw-bold">{short_title}</h5>
                    <p class="card-text text-muted small">{short_desc}</p>
                </div>
                <div class="card-footer bg-transparent border-0 pt-0">
                    <a href="{doc['id']}.html" class="btn btn-outline-primary btn-sm w-100 rounded-pill">View Prompt</a>
                </div>
            </div>
        </div>
        """
    
    idx_out = idx_template.replace("{{MENU}}", menu_html).replace("{{CARDS}}", cards_html)
    with open(os.path.join(PUBLIC_DIR, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(idx_out)
        
    # 6. Build Individual Pages
    with open(TEMPLATE_STYLE, 'r', encoding='utf-8') as f:
        style_template = f.read()
        
    for doc in docs:
        examples_html = ""
        for category, text in doc['examples'].items():
            examples_html += f"""
            <div class="mb-4">
                <h5 class="text-secondary-accent border-bottom border-secondary pb-2"><i class="bi bi-code-square me-2"></i>{category}</h5>
                <div class="p-3 bg-darker rounded border border-secondary shadow-sm">
                    <p class="mb-0 text-light fst-italic">"{text}"</p>
                </div>
            </div>
            """
            
        page_out = style_template.replace("{{MENU}}", menu_html)
        page_out = page_out.replace("{{TITLE}}", doc['title'])
        page_out = page_out.replace("{{DESCRIPTION}}", doc['description'])
        page_out = page_out.replace("{{EXAMPLES}}", examples_html)
        
        with open(os.path.join(PUBLIC_DIR, f"{doc['id']}.html"), 'w', encoding='utf-8') as f:
            f.write(page_out)
            
    print(f"Build complete. {len(docs) + 1} pages generated in '{PUBLIC_DIR}' directory.")
    
if __name__ == "__main__":
    generate_site()

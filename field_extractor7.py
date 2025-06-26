import fitz
from langchain_ollama import OllamaLLM
from langchain.prompts import ChatPromptTemplate

llm = OllamaLLM(model="llama3.1:8b")

# def generate_label(text, value):
#     prompt = ChatPromptTemplate.from_template(
#         "Given the following value from a PDF form: '{value}', "
#         "and nearby text: '{text}', return a short label like 'email', 'full name', or 'move-in date'. "
#         "Avoid using company info or template values."
#     )
#     return llm.invoke(prompt.format(value=value, text=text)).strip().lower()

# def generate_label(text, value):
#     prompt = ChatPromptTemplate.from_template(
#         "You are labeling a field in a PDF form.\n\n"
#         "Given the field value: '{value}'\n"
#         "And the nearby text: '{text}'\n\n"
#         "Return ONLY the most appropriate short label for this field, such as 'email', 'full name', 'move-in date', etc.\n"
#         "Avoid explaining your reasoning. Do not return multiple labels. Just reply with the label only, nothing else."
#     )
#     return llm.invoke(prompt.format(value=value, text=text)).strip().lower()

def generate_label(text, value):
    prompt = ChatPromptTemplate.from_template(
        "You are labeling a field from a filled-out PDF form. Your job is to identify **only the information entered by the client/user filling the form**, and return a short semantic label for it.\n\n"
        "The value is: '{value}'\n"
        "Nearby text on the form is: '{text}'\n\n"
        "- Only return values that the client would reasonably fill in (e.g., their name, email, phone, suite number).\n"
        "- Do NOT label company information, template values, or landlord/lawyer data unless it's clearly entered by the client.\n"
        "- Examples of valid labels: 'full name', 'email', 'move-in date', 'suite number', 'phone number'.\n"
        "- Return just the most relevant label (no reasoning, no quotes).\n\n"
        "Return only one most relevant short label. No lists. No newlines. No reasoning.\n"
        "Return the label now:"
    )
    return llm.invoke(prompt.format(value=value, text=text)).strip().lower()

def extract_fields_from_filled_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    output = []
    for page_num, page in enumerate(doc):
        widgets = page.widgets()
        for w in widgets:
            val = w.field_value
            if not val or val.strip() == "":
                continue
            rect = w.rect
            center_x = (rect.x0 + rect.x1) / 2
            center_y = (rect.y0 + rect.y1) / 2
            text_near = page.get_textbox(rect + (-70, -70, 70, 70)).strip()
            label = generate_label(text_near, val)
            if "provident" in val.lower() or "customerservice" in val.lower():
                continue  # Filter out known company fields
            output.append({
                "field_name": w.field_name,
                "label": label,
                "value": val.strip(),
                "page": page_num,
                "pos": [center_x, center_y]
            })
    return output
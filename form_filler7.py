import fitz

def fill_pdf_fields(blank_pdf_path, output_pdf_path, matched_data):
    doc = fitz.open(blank_pdf_path)
    for page in doc:
        for w in page.widgets():
            if w.field_name in matched_data:
                w.field_value = matched_data[w.field_name]
                w.update()
    doc.save(output_pdf_path)
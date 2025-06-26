import streamlit as st
from field_extractor7 import extract_fields_from_filled_pdf
from form_matcher7 import match_filled_to_blank_fields
from form_filler7 import fill_pdf_fields
import tempfile
import os

st.title("Form Filler")

filled_file = st.file_uploader("Step 1: Upload filled PDF", type="pdf")
blank_file = st.file_uploader("Step 2: Upload blank PDF", type="pdf")

if filled_file and blank_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as f1:
        f1.write(filled_file.read())
        filled_path = f1.name
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as f2:
        f2.write(blank_file.read())
        blank_path = f2.name

    st.write("Getting fields from filled form...")
    extracted = extract_fields_from_filled_pdf(filled_path)
    st.json(extracted)

    st.write("Matching to blank form...")
    matched = match_filled_to_blank_fields(extracted, blank_path)
    st.json(matched)

    if st.button("Fill and Download PDF"):
        output_path = os.path.join(tempfile.gettempdir(), "ai_filled_form.pdf")
        fill_pdf_fields(blank_path, output_path, matched)
        with open(output_path, "rb") as f:
            st.download_button("Download Filled PDF", f, file_name="filled_form.pdf")
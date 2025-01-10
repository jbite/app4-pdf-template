import streamlit as st
import os
from pypdf import PdfReader
from io import BytesIO 
import SplitPDF

with st.sidebar:
    st.title("File Upload and Save")

    uploaded_file = st.file_uploader("Choose a file")

    if uploaded_file is not None:
        file_name = uploaded_file.name
        pdf_bytes = uploaded_file.read()
        pdfreader = PdfReader(BytesIO(pdf_bytes))

col_split,col_merge = st.columns(2)
 
with col_split:     
    st.title("Split PDF")
    if not uploaded_file:
        st.info("No PDF files found. Please upload a PDF file.")
    else:
        output_prefix = st.text_input(label="New file prefix",value="Newfile")
        ranges_string = st.text_input(label="Page range",value="1-10,11-20")
        if st.button("Split PDF"):
            if pdfreader:
                output_pdf_path = SplitPDF.split_pdf_by_ranges(pdfreader, output_prefix+'_'+file_name.strip('.pdf'), ranges_string)
                if output_pdf_path:
                    st.success(f"PDF split successfully! Please dowload")
                    with open(output_pdf_path, "rb") as file:
                        st.download_button(
                            label="Download Split PDF",
                            data=file,
                            file_name=os.path.basename(output_pdf_path),
                            mime="application/pdf"
                        )
            else:
                st.warning("Please select a PDF file.")

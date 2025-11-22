import streamlit as st
from langchain_community.document_loaders import PDFPlumberLoader
from langchain_core.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser
from langchain_groq import ChatGroq
from pydantic import BaseModel, Field
import pandas as pd
import os
import tempfile
from dotenv import load_dotenv

load_dotenv()

st.title("PDF → Excel Data Extractor")

uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])

if uploaded_file:
    st.success("PDF uploaded successfully.")

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
        temp_file.write(uploaded_file.read())
        pdf_path = temp_file.name

    if st.button("Extract Data"):

        loader = PDFPlumberLoader(pdf_path)
        docs = loader.load()
        full_text = "\n\n".join([d.page_content for d in docs])

        class Row(BaseModel):
            key: str
            value: str
            comments: str

        class Output(BaseModel):
            data: list[Row]

        parser = PydanticOutputParser(pydantic_object=Output)

        prompt = PromptTemplate(
            template="""
Extract key:value pairs from this document.

Rules:
- Preserve exact wording (NO paraphrasing)
- No summarization
- Capture 100% content
- Add contextual notes in "comments"
- Output ONLY JSON in the provided format

Document:
{document}

JSON Format:
{format}
""",
            input_variables=["document"],
            partial_variables={"format": parser.get_format_instructions()},
        )

        prompt_text = prompt.format(document=full_text)

        llm = ChatGroq(
            api_key=os.getenv("GROQ_API_KEY"),
            model_name="openai/gpt-oss-20b",
            temperature=0,
        )

        response = llm.invoke(prompt_text)
        raw_output = response.content

        parsed = parser.parse(raw_output)

        rows = [[r.key, r.value, r.comments] for r in parsed.data]
        df = pd.DataFrame(rows, columns=["Key", "Value", "Comments"])
        output_file = "Output_chatgroq.xlsx"
        df.to_excel(output_file, index=False)

        st.success("Extraction completed!")

        with open(output_file, "rb") as f:
            st.download_button(
                "Download Excel File",
                f,
                file_name="Output_chatgroq.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

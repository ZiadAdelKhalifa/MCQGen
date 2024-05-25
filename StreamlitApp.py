import os
import json
import traceback
import pandas as pd
from dotenv import load_dotenv
from src.mcqgenerator.utils import read_file,get_table_data
import streamlit as st
from langchain.callbacks import get_openai_callback
from src.mcqgenerator.MCQGenerator import generate_evaluate_chain
from src.mcqgenerator.logger import logging

#loading json file

with open('Response.json', 'r') as file:
    RESPONSE_JSON = json.load(file)

#creating a title for the app
st.title("MCQs Creator Application with LangChain 🦜⛓️")

with st.form("user_inputs"):
    upload_file = st.file_uploader("Upload a PDF or txt file")
    mcq_count = st.number_input("No. of MCQs", min_value=3, max_value=50)
    subject = st.text_input("Insert Subject", max_chars=20)
    st.caption("Please enter the complexity level of questions (e.g., Simple, Advanced):")
    tone = st.text_input("Complexity Level of Questions", max_chars=20)
    button = st.form_submit_button("Create MCQs")

if button and upload_file is not None and mcq_count and subject and tone:
    with st.spinner("loading..."):
        try:
            text = read_file(upload_file)
            with get_openai_callback() as cb:
                response = generate_evaluate_chain(
                    {
                        "text": text,
                        "number": mcq_count,
                        "subject": subject,
                        "tone": tone,
                        "response_json": json.dumps(RESPONSE_JSON)
                    }
                )

        except Exception as e:
            traceback.print_exception(type(e), e, e.__traceback__)
            st.error("Error")

        else:
            st.write(f"Total Tokens: {cb.total_tokens}")
            st.write(f"Prompt Tokens: {cb.prompt_tokens}")
            st.write(f"Completion Tokens: {cb.completion_tokens}")
            st.write(f"Total Cost: {cb.total_cost}")
            if isinstance(response, dict):
                quiz = response.get("quiz", None)
                if quiz is not None:
                    table_data = get_table_data(quiz)
                    if table_data is not None:
                        df = pd.DataFrame(table_data)
                        df.index = df.index + 1
                        st.table(df)

                        csv = df.to_csv(index=False)
                        st.download_button(
                            label="Download Quiz as CSV",
                            data=csv,
                            file_name='quiz.csv',
                            mime='text/csv'
                        )

                        st.text_area(label="Review", value=response.get("review", ""))

                    else:
                        st.error("Error in the table data")
                else:
                    st.write(response)
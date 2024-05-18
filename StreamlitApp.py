import os
import json
import pandas as pd
import traceback
from dotenv import load_dotenv
from src.mcqgenerator.utils import read_file, get_table_data
import streamlit as st
from langchain.callbacks import get_openai_callback
from src.mcqgenerator.MCQGenerator import generate_evaluate_chain
from src.mcqgenerator.logger import logging



# Loading JSON file
with open(r'C:\Users\Ziad\MCQGen\Response.json', 'r') as file:
    RESPONSE_JSON = json.load(file)



# Creating title for the app
st.title("MCQs Creator Application using LangChain")

# Create a form using st.form
with st.form('user_inputs'):
    # File upload
    upload_file = st.file_uploader("Upload a PDF or text file")

    # Input fields
    mcq_count = st.number_input("Number of MCQs", min_value=5, max_value=100)
    subject = st.text_input("Insert subject", max_chars=30)
    tone = st.text_input("Complexity of the quiz", max_chars=30, placeholder='Simple')

    # Add button
    button = st.form_submit_button('Create MCQs')

    # Check if the button is clicked and the input fields are inserted or not
    if button and upload_file is not None and mcq_count and subject and tone:
        with st.spinner("Loading ....."):
            try:
                text = read_file(upload_file)

                # Count tokens and the cost of the API call
                with get_openai_callback() as cb:
                    response = generate_evaluate_chain({
                        "text": text,
                        "number": mcq_count,
                        "subject": subject,
                        "tone": tone,
                        "response_json": json.dumps(RESPONSE_JSON)
                    })
            except Exception as e:
                traceback.print_exception(type(e), e, e.__traceback__)
                st.error("Error during MCQ generation.")
            else:
                st.write(f"Total Tokens: {cb.total_tokens}")
                st.write(f"Prompt Tokens: {cb.prompt_tokens}")
                st.write(f"Completion Tokens: {cb.completion_tokens}")
                st.write(f"Total Cost: {cb.total_cost}")
                
                if isinstance(response, dict):
                    quiz = response.get("quiz",None)
                    if quiz is not None:
                        table_data = get_table_data(quiz)
                        if table_data is not None:
                            df = pd.DataFrame(table_data)
                            df.index = df.index + 1
                            st.table(df)
                            # Display the review in a text box as well
                            st.text_area(label="Review", value=response['review'])
                        else:
                            st.error('Error in the table data')
                
                       
                else:
                    st.write(response)

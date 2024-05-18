import os
import traceback
import json
import PyPDF2


def read_file(file):
    if file.name.endswith('.pdf'):
        try:
            pdf_reader=PyPDF2.PdfFileReader(file)
            text=""
            for pages in pdf_reader.pages:
                text+=pages.extract_text
            return text
        except Exception as e:
            raise Exception('Error reading the pdf file')
    elif file.name.endswith('.txt'):
        return file.read().decode('utf-8')
    else :
        raise Exception('Unsupported file format onlt pdf and text file supported')
    

def get_table_data(quiz_str):
    try:
        #convert the str to dict 
        quiz_dict=json.loads(quiz_str)
        quiz_data_table=[]

        #iterate over the quiz dictionary and extract the required information
        for key,value in quiz_dict.items():
            mcq=value['mcq']
            options="  ||  ".join(
                [
                    f"{option}->{option_value} " for option ,option_value in value['options'].items()
                ]

            )
            correct=value['correct']
            quiz_data_table.append({'MCQ':mcq ,"Choices":options,"correct":correct})

        return quiz_data_table
    except Exception as e:
        traceback.print_exception(type(e),e,e.__traceback__)
        return False
    

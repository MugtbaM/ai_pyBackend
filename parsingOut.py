import pandas as pd
import re

def clean_text(text):
    # Remove non-alphanumeric characters using regex
    cleaned_text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    cleaned_text = cleaned_text.replace('\n', '')
    return cleaned_text

# Example usage
text = "Hello, World! @2023 #Python #CleanText"
cleaned_text = clean_text(text)

def create_parsing_out(parsed_data):
    # Safely get the data with default empty lists in case keys are missing
    pre_education = parsed_data.get('degree', [])
    pre_skills = parsed_data.get('skills', [])
    pre_experience = parsed_data.get('experience', [])
    
    # Handling missing education data
    if not pre_education or not pre_education[0] or pd.isnull(pre_education[0][0]):
        education = 'no Education Information'
    else:
        education = pre_education[0][0]
    
    # Handling missing experience data
    if not pre_experience:
        experience = 'No previous Experience Record'
    else:
        experience = " ".join(pre_experience)
    
    # Joining skills list into a comma-separated string
    skills = ", ".join(pre_skills)
    
    parsed_text = (f"the user has {education} and has {experience} and has the skills set of {skills}")
    cleand_text = clean_text(parsed_text)
    return cleand_text
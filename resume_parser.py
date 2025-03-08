from pyresparser import ResumeParser
import logging

def parse_resume(file_path):
    try:
        # Parse resume using pyresparser
        data = ResumeParser(file_path).get_extracted_data()
        
        # Standardize output format
        return {
            "degree": [data.get("degree", "")],
            "skills": data.get("skills", []),
            "experience": data.get("experience", [])
        }
    
    except Exception as e:
        logging.error(f"Resume parsing failed: {str(e)}")
        raise
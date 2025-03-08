from flask import Flask, request, jsonify
from flask_cors import CORS
from resume_parser import parse_resume
from parsingOut import create_parsing_out
from job_predictor import predict_job_title
from job_api import fetch_jobs
from dataOut import create_text
import tempfile
import os
import logging


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # Enable CORS

# Route 1: Parse Resume
@app.route('/api/parse_resume', methods=['POST'])
def handle_resume_parsing():
    try:
        # Get uploaded file
        resume_file = request.files['resume']
        
        # Save to temp file
        temp_dir = tempfile.mkdtemp()
        temp_path = os.path.join(temp_dir, resume_file.filename)
        resume_file.save(temp_path)
        # Parse resume
        parsed_data = parse_resume(temp_path)
        # logger.info(parsed_data)
        text = create_parsing_out(parsed_data)
        # logger.info(text)

        # Predict Job Title
        job_title = predict_job_title(text)
        logger.info(job_title)

        # Cleanup temp file
        os.remove(temp_path)
        os.rmdir(temp_dir)
        
        # Extract required fields
        result = {
            # "education": parsed_data.get("degree", []),
            # "skills": parsed_data.get("skills", []),
            # "experience": parsed_data.get("experience", [])
            "preicted_job": job_title
        }
        # logger.info(result)
        return jsonify(result)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
# Route 2: Handle Manual Input
@app.route('/api/entered_data', methods=['POST'])
def handle_entered_data():
    try:
        data = request.json
        education = data.get('education')
        skills = data.get('skills')
        experience = data.get('experience')

        # Predict job title using BERT
        #job_title = predict_job_title(education, skills, experience)
        job_prediction = education, skills, experience#this would be edited

        return jsonify(job_prediction)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route 3: Job Search
@app.route('/api/search-from-data', methods=['POST'])
def handle_job_search():
    try:
        data = request.json
        # logger.info(data)
        text = create_text(data)
        # Get user inputs
        education = data.get('education')
        skills = data.get('skills')
        experience = data.get('experience')
        #preferences = data.get('preferences')
        
        
        job_title = predict_job_title(text)
        logger.info(job_title)
        # Fetch jobs from API
        #jobs = fetch_jobs(job_title, preferences)
        
        return jsonify({
            # 'education': education,
            # 'skills': skills,
            # 'experience': experience
            "predicted_job": job_title
            #"jobs": jobs[:10]  # Return top 10 results
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
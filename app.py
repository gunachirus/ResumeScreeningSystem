from flask import Flask, request
import pdfplumber
import os
import re

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

skills_list = [
    'python',
    'sql',
    'machine learning',
    'flask',
    'django',
    'data science',
    'numpy',
    'pandas',
    'html',
    'css',
    'javascript',
    'react'
]

job_skills = [
    'python',
    'sql',
    'machine learning',
    'flask'
]


def extract_text(pdf_path):

    text = ""

    with pdfplumber.open(pdf_path) as pdf:

        for page in pdf.pages:

            extracted = page.extract_text()

            if extracted:
                text += extracted

    return text


def clean_text(text):

    text = text.lower()

    text = re.sub(r'[^a-zA-Z ]', ' ', text)

    return text


def extract_skills(text):

    found_skills = []

    for skill in skills_list:

        if skill.lower() in text:
            found_skills.append(skill)

    return found_skills


@app.route('/')
def home():

    return '''
    <!DOCTYPE html>
    <html>
    <head>

        <title>Resume Screening System</title>

        <style>

            body{
                font-family: Arial;
                background:#f4f4f4;
                padding:40px;
            }

            .container{
                background:white;
                padding:30px;
                width:500px;
                margin:auto;
                border-radius:10px;
                box-shadow:0px 0px 10px gray;
            }

            h1{
                text-align:center;
                color:blue;
            }

            button{
                background:blue;
                color:white;
                border:none;
                padding:10px;
                width:100%;
                cursor:pointer;
                border-radius:5px;
            }

        </style>

    </head>

    <body>

        <div class="container">

            <h1>Resume Screening System</h1>

            <form action="/upload" method="POST" enctype="multipart/form-data">

                <input type="file" name="resume" required><br><br>

                <button type="submit">Upload Resume</button>

            </form>

        </div>

    </body>

    </html>
    '''


@app.route('/upload', methods=['POST'])
def upload_resume():

    file = request.files['resume']

    if file:

        filepath = os.path.join(UPLOAD_FOLDER, file.filename)

        file.save(filepath)

        resume_text = extract_text(filepath)

        cleaned_text = clean_text(resume_text)

        found_skills = extract_skills(cleaned_text)

        matched_skills = []

        for skill in found_skills:

            if skill in job_skills:
                matched_skills.append(skill)

        score = (len(matched_skills) / len(job_skills)) * 100

        if score >= 75:
            recommendation = "Excellent Match"

        elif score >= 50:
            recommendation = "Good Match"

        else:
            recommendation = "Needs Improvement"

        return f'''

        <html>

        <head>

        <style>

        body{{
            font-family:Arial;
            background:#f4f4f4;
            padding:40px;
        }}

        .container{{
            background:white;
            padding:30px;
            width:600px;
            margin:auto;
            border-radius:10px;
            box-shadow:0px 0px 10px gray;
        }}

        h1{{
            color:green;
        }}

        </style>

        </head>

        <body>

        <div class="container">

        <h1>Resume Analysis Result</h1>

        <h3>Detected Skills</h3>

        <p>{", ".join(found_skills)}</p>

        <h3>Matched Skills</h3>

        <p>{", ".join(matched_skills)}</p>

        <h3>Resume Score</h3>

        <p>{score}%</p>

        <h3>Recommendation</h3>

        <p>{recommendation}</p>

        <br>

        <a href="/">Go Back</a>

        </div>

        </body>

        </html>

        '''

    return "No File Uploaded"


if __name__ == '__main__':

   app.run(host='0.0.0.0', port=5000)

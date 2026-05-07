from flask import Flask, render_template, request
from PyPDF2 import PdfReader
import os
import re

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Skills List
skills_list = [
    'python',
    'sql',
    'machine learning',
    'data science',
    'html',
    'css',
    'javascript',
    'flask',
    'django',
    'react',
    'pandas',
    'numpy',
    'opencv',
    'mysql',
    'java',
    'c++'
]


# Home Page
@app.route('/')
def home():
    return render_template('index.html')


# Prediction Route
@app.route('/predict', methods=['POST'])
def predict():

    if 'resume' not in request.files:
        return 'No File Uploaded'

    file = request.files['resume']

    if file.filename == '':
        return 'No Selected File'

    filepath = os.path.join(
        app.config['UPLOAD_FOLDER'],
        file.filename
    )

    file.save(filepath)

    # Read PDF
    pdf = PdfReader(filepath)

    text = ""

    for page in pdf.pages:
        extracted = page.extract_text()

        if extracted:
            text += extracted

    # Clean Text
    clean_text = re.sub(r'[^A-Za-z ]', ' ', text)
    clean_text = clean_text.lower()

    # Skill Detection
    found_skills = []

    for skill in skills_list:
        if skill in clean_text:
            found_skills.append(skill)

    # Resume Score
    score = min(len(found_skills) * 10, 100)

    # Category Prediction
    category = "General"

    if 'machine learning' in clean_text or 'data science' in clean_text:
        category = 'Data Scientist'

    elif 'python' in clean_text or 'django' in clean_text:
        category = 'Python Developer'

    elif 'html' in clean_text or 'css' in clean_text or 'javascript' in clean_text:
        category = 'Web Developer'

    elif 'mysql' in clean_text or 'sql' in clean_text:
        category = 'Database Developer'

    elif 'java' in clean_text:
        category = 'Java Developer'

    # Suggestions
    suggestions = []

    if score < 30:
        suggestions.append("Add more technical skills")
        suggestions.append("Improve project section")
        suggestions.append("Add certifications")

    elif score < 60:
        suggestions.append("Add more real-time projects")
        suggestions.append("Improve resume formatting")

    else:
        suggestions.append("Excellent Resume")
        suggestions.append("Ready for job applications")

    return render_template(
        'result.html',
        category=category,
        skills=found_skills,
        score=score,
        suggestions=suggestions
    )


if __name__ == '__main__':

    if not os.path.exists('uploads'):
        os.makedirs('uploads')

    app.run(debug=True)
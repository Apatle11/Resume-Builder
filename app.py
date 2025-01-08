from flask import Flask, render_template, request, jsonify, send_file, make_response
import os
import json
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import tempfile
import base64
import time
import pdfkit

app = Flask(__name__)

# Resume templates configuration
RESUME_TEMPLATES = [
    {
        'id': 1,
        'name': 'Modern Professional',
        'description': 'A clean and modern template with a professional layout',
        'template': 'template1.html',
        'image': 'template1.png'
    },
    {
        'id': 2,
        'name': 'Creative Design',
        'description': 'A creative template with a unique design and layout',
        'template': 'template2.html',
        'image': 'template2.png'
    },
    {
        'id': 3,
        'name': 'Executive Style',
        'description': 'An executive template perfect for senior professionals',
        'template': 'template3.html',
        'image': 'template3.png'
    }
]

# Your resume data
MY_RESUME_DATA = {
    "fullName": "Abhijeet Shinde",
    "email": "abhijeetshinde2025@gmail.com",
    "phone": "+91 7066713577",
    "location": "Pune, Maharashtra",
    "summary": "Dedicated and detail-oriented Full Stack Developer with expertise in Python, JavaScript, and modern web technologies. Passionate about creating efficient, scalable web applications and implementing innovative solutions.",
    "experience": [
        {
            "position": "Full Stack Developer",
            "company": "Freelancer",
            "duration": "2023 - Present",
            "responsibilities": "Developed and maintained web applications using Python, Flask, and JavaScript. Implemented responsive designs and optimized application performance."
        },
        {
            "position": "Web Developer Intern",
            "company": "Tech Solutions Ltd",
            "duration": "2022 - 2023",
            "responsibilities": "Assisted in developing web applications, created responsive UI designs, and collaborated with senior developers on various projects."
        }
    ],
    "education": [
        {
            "degree": "Bachelor of Engineering in Information Technology",
            "institution": "Savitribai Phule Pune University",
            "year": "2020 - 2024",
            "gpa": "8.5"
        }
    ],
    "skills": "Python, JavaScript, HTML5, CSS3, Flask, React.js, Node.js, MongoDB, SQL, Git, RESTful APIs, Responsive Design"
}

# Sample data for template previews
PREVIEW_DATA = {
    "fullName": "John Smith",
    "email": "john.smith@example.com",
    "phone": "+1 234 567 8900",
    "location": "New York, NY",
    "summary": "Experienced software engineer with expertise in web development and cloud technologies.",
    "experience": [
        {
            "position": "Senior Software Engineer",
            "company": "Tech Corp",
            "duration": "2020 - Present",
            "responsibilities": "Led development of cloud-based applications and mentored junior developers."
        }
    ],
    "education": [
        {
            "degree": "Bachelor of Science in Computer Science",
            "institution": "University of Technology",
            "year": "2016 - 2020",
            "gpa": "3.8"
        }
    ],
    "skills": "Python, JavaScript, React, Node.js, AWS, Docker"
}

@app.route('/')
def index():
    return render_template('index.html', templates=RESUME_TEMPLATES)

@app.route('/template/<int:template_id>')
def template_form(template_id):
    template = next((t for t in RESUME_TEMPLATES if t['id'] == template_id), None)
    if template:
        return render_template('form.html', template=template)
    return "Template not found", 404

@app.route('/form/<int:template_id>')
def template_form_route(template_id):
    template = next((t for t in RESUME_TEMPLATES if t['id'] == template_id), RESUME_TEMPLATES[0])
    return render_template('form.html', template=template)

@app.route('/generate_resume', methods=['POST'])
def generate_resume():
    data = request.form.to_dict(flat=False)
    template_id = request.form.get('template_id', '1')
    
    # Process the form data
    resume_data = {
        'fullName': data.get('fullName', [''])[0],
        'fatherName': data.get('fatherName', [''])[0],
        'dateOfBirth': data.get('dateOfBirth', [''])[0],
        'email': data.get('email', [''])[0],
        'phone': data.get('phone', [''])[0],
        'location': data.get('location', [''])[0],
        'summary': data.get('summary', [''])[0],
        'skills': [skill.strip() for skill in data.get('skills', [''])[0].split(',') if skill.strip()],
        'experiences': [],
        'education': []
    }

    # Process multiple work experiences
    positions = data.get('position[]', [])
    companies = data.get('company[]', [])
    durations = data.get('duration[]', [])
    responsibilities = data.get('responsibilities[]', [])

    for i in range(len(positions)):
        if i < len(companies) and i < len(durations) and i < len(responsibilities):
            resume_data['experiences'].append({
                'position': positions[i],
                'company': companies[i],
                'duration': durations[i],
                'description': responsibilities[i]
            })

    # Process multiple education entries
    degrees = data.get('degree[]', [])
    institutions = data.get('institution[]', [])
    years = data.get('year[]', [])
    gpas = data.get('gpa[]', [])

    for i in range(len(degrees)):
        if i < len(institutions) and i < len(years):
            resume_data['education'].append({
                'degree': degrees[i],
                'institution': institutions[i],
                'year': years[i],
                'gpa': gpas[i] if i < len(gpas) else ''
            })

    template = next((t for t in RESUME_TEMPLATES if str(t['id']) == template_id), RESUME_TEMPLATES[0])
    return render_template('preview.html', template=template, resume=resume_data)

@app.route('/preview/<int:template_id>')
def preview_template(template_id):
    template = next((t for t in RESUME_TEMPLATES if t['id'] == template_id), RESUME_TEMPLATES[0])
    sample_data = {
        'fullName': 'John Doe',
        'fatherName': 'Robert Doe',
        'dateOfBirth': '1990-01-01',
        'email': 'john@example.com',
        'phone': '(123) 456-7890',
        'location': 'New York, NY',
        'summary': 'Experienced professional with expertise in...',
        'experiences': [
            {
                'position': 'Senior Developer',
                'company': 'Tech Corp',
                'duration': '2020 - Present',
                'description': 'Led development of multiple projects...'
            }
        ],
        'education': [
            {
                'degree': 'Bachelor of Science in Computer Science',
                'institution': 'University of Technology',
                'year': '2019',
                'gpa': '3.8'
            }
        ],
        'skills': ['Python', 'JavaScript', 'React', 'Node.js', 'SQL']
    }
    return render_template('preview.html', template=template, resume=sample_data)

@app.route('/download-pdf/<int:template_id>')
def download_pdf(template_id):
    template = next((t for t in RESUME_TEMPLATES if t['id'] == template_id), RESUME_TEMPLATES[0])
    resume_data = {
        'fullName': 'John Doe',
        'fatherName': 'Robert Doe',
        'dateOfBirth': '1990-01-01',
        'email': 'john@example.com',
        'phone': '(123) 456-7890',
        'location': 'New York, NY',
        'summary': 'Experienced professional with expertise in...',
        'experiences': [
            {
                'position': 'Senior Developer',
                'company': 'Tech Corp',
                'duration': '2020 - Present',
                'description': 'Led development of multiple projects...'
            }
        ],
        'education': [
            {
                'degree': 'Bachelor of Science in Computer Science',
                'institution': 'University of Technology',
                'year': '2019',
                'gpa': '3.8'
            }
        ],
        'skills': ['Python', 'JavaScript', 'React', 'Node.js', 'SQL']
    }

    # Generate HTML
    html = render_template(template['template'], resume=resume_data)

    # PDF options
    options = {
        'page-size': 'A4',
        'margin-top': '0mm',
        'margin-right': '0mm',
        'margin-bottom': '0mm',
        'margin-left': '0mm',
        'encoding': 'UTF-8',
        'no-outline': None,
        'enable-local-file-access': None
    }

    # Create a temporary file for the HTML
    with tempfile.NamedTemporaryFile(suffix='.html', delete=False, mode='w', encoding='utf-8') as f:
        f.write(html)
        temp_html_path = f.name

    try:
        # Create PDF
        pdf = pdfkit.from_file(temp_html_path, False, options=options)
        
        # Clean up
        os.unlink(temp_html_path)
        
        # Create response
        response = make_response(pdf)
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = f'attachment; filename=resume_{template_id}.pdf'
        
        return response
        
    except Exception as e:
        print(f"Error generating PDF: {str(e)}")
        if os.path.exists(temp_html_path):
            os.unlink(temp_html_path)
        return str(e), 500

@app.route('/my-resume')
def my_resume():
    template_id = request.args.get('template', '1')
    selected_template = next((t for t in RESUME_TEMPLATES if str(t['id']) == template_id), RESUME_TEMPLATES[0])
    return render_template(selected_template['template'], data=MY_RESUME_DATA)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

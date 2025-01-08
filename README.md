# Resume Builder

A modern web application that allows users to create professional resumes using beautiful templates. Users can input their information through a user-friendly form and generate a downloadable resume in their chosen template style.

## Features

- Multiple modern resume templates
- User-friendly form interface
- Dynamic form fields for education and work experience
- Print and PDF download options
- Responsive design
- Modern and professional UI

## Setup Instructions

1. Install Python (3.7 or higher)

2. Install the required packages:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python app.py
```

4. Open your browser and navigate to `http://localhost:5000`

## Project Structure

```
Resume Builder/
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
├── static/
│   ├── css/
│   │   └── style.css  # Custom styles
│   ├── js/
│   │   └── main.js    # Custom JavaScript
│   └── images/        # Template thumbnails
└── templates/
    ├── base.html      # Base template
    ├── index.html     # Template selection page
    ├── form.html      # Resume form
    └── resume_templates/ # Resume template designs
```

## Technologies Used

- Python Flask
- HTML5
- CSS3
- JavaScript
- Bootstrap 5
- html2pdf.js

## Contributing

Feel free to submit issues and enhancement requests!

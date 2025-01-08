from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import os

# Setup Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode
chrome_options.add_argument("--window-size=1024,1500")  # Set window size

# Initialize the driver with ChromeDriverManager
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# Create directory for template images if it doesn't exist
os.makedirs("static/images", exist_ok=True)

# Sample data for preview
preview_data = {
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

# Start Flask server
import subprocess
server = subprocess.Popen(["python", "-m", "flask", "run"])
time.sleep(2)  # Wait for server to start

try:
    # Generate preview for each template
    for i in range(1, 11):
        url = f"http://localhost:5000/preview?template={i}"
        driver.get(url)
        time.sleep(1)  # Wait for page to load
        
        # Take screenshot
        driver.save_screenshot(f"static/images/template{i}.png")
        print(f"Generated preview for template {i}")

finally:
    # Clean up
    driver.quit()
    server.terminate()
    print("Preview generation complete!")

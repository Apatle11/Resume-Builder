// Form validation
(() => {
    'use strict'
    const forms = document.querySelectorAll('.needs-validation')
    Array.from(forms).forEach(form => {
        form.addEventListener('submit', event => {
            if (!form.checkValidity()) {
                event.preventDefault()
                event.stopPropagation()
            }
            form.classList.add('was-validated')
        }, false)
    })
})()

// Print functionality
function printResume() {
    window.print();
}

// Download as PDF functionality
function downloadPDF() {
    // Show loading animation
    const loadingDiv = document.createElement('div');
    loadingDiv.className = 'loading';
    loadingDiv.innerHTML = '<div class="loading-spinner"></div>';
    document.body.appendChild(loadingDiv);

    const element = document.getElementById('resume');
    const opt = {
        margin: [10, 10],
        filename: 'resume.pdf',
        image: { type: 'jpeg', quality: 0.98 },
        html2canvas: { 
            scale: 2,
            useCORS: true,
            logging: false
        },
        jsPDF: { 
            unit: 'mm', 
            format: 'a4', 
            orientation: 'portrait' 
        }
    };

    // Generate PDF
    html2pdf().set(opt).from(element).save().then(() => {
        // Remove loading animation
        document.body.removeChild(loadingDiv);
    });
}

// Dynamic form fields with animation
function addEducation() {
    const container = document.getElementById('educationContainer');
    const newEntry = document.createElement('div');
    newEntry.className = 'education-entry mb-4 animate-fade-in';
    
    const educationCount = container.getElementsByClassName('education-entry').length;
    
    newEntry.innerHTML = `
        <div class="form-section">
            <div class="d-flex justify-content-between align-items-center mb-3">
                <h5 class="mb-0">Education ${educationCount + 1}</h5>
                <button type="button" class="btn btn-outline-danger btn-sm" onclick="this.parentElement.parentElement.remove()">
                    <i class="fas fa-trash me-1"></i>Remove
                </button>
            </div>
            <div class="row g-3">
                <div class="col-md-6">
                    <div class="form-floating">
                        <input type="text" class="form-control" name="education[${educationCount}][degree]" required>
                        <label><i class="fas fa-graduation-cap me-2"></i>Degree</label>
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="form-floating">
                        <input type="text" class="form-control" name="education[${educationCount}][institution]" required>
                        <label><i class="fas fa-university me-2"></i>Institution</label>
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="form-floating">
                        <input type="text" class="form-control" name="education[${educationCount}][year]" required>
                        <label><i class="fas fa-calendar me-2"></i>Year</label>
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="form-floating">
                        <input type="text" class="form-control" name="education[${educationCount}][gpa]">
                        <label><i class="fas fa-star me-2"></i>GPA/Score</label>
                    </div>
                </div>
            </div>
        </div>
    `;
    container.appendChild(newEntry);
}

function addExperience() {
    const container = document.getElementById('experienceContainer');
    const newEntry = document.createElement('div');
    newEntry.className = 'experience-entry mb-4 animate-fade-in';
    
    const experienceCount = container.getElementsByClassName('experience-entry').length;
    
    newEntry.innerHTML = `
        <div class="form-section">
            <div class="d-flex justify-content-between align-items-center mb-3">
                <h5 class="mb-0">Experience ${experienceCount + 1}</h5>
                <button type="button" class="btn btn-outline-danger btn-sm" onclick="this.parentElement.parentElement.remove()">
                    <i class="fas fa-trash me-1"></i>Remove
                </button>
            </div>
            <div class="row g-3">
                <div class="col-md-6">
                    <div class="form-floating">
                        <input type="text" class="form-control" name="experience[${experienceCount}][company]" required>
                        <label><i class="fas fa-building me-2"></i>Company</label>
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="form-floating">
                        <input type="text" class="form-control" name="experience[${experienceCount}][position]" required>
                        <label><i class="fas fa-briefcase me-2"></i>Position</label>
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="form-floating">
                        <input type="text" class="form-control" name="experience[${experienceCount}][duration]" required>
                        <label><i class="fas fa-clock me-2"></i>Duration</label>
                    </div>
                </div>
                <div class="col-12">
                    <div class="form-floating">
                        <textarea class="form-control" name="experience[${experienceCount}][description]" style="height: 100px" required></textarea>
                        <label><i class="fas fa-tasks me-2"></i>Job Description</label>
                    </div>
                </div>
            </div>
        </div>
    `;
    container.appendChild(newEntry);
}

// Initialize tooltips
document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    tooltipTriggerList.forEach(function (tooltipTriggerEl) {
        new bootstrap.Tooltip(tooltipTriggerEl)
    });

    // Add smooth scrolling
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            document.querySelector(this.getAttribute('href')).scrollIntoView({
                behavior: 'smooth'
            });
        });
    });
});

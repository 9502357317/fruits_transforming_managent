// Main JavaScript file for Fruit Classifier

document.addEventListener('DOMContentLoaded', function() {
    const uploadForm = document.getElementById('uploadForm');
    const resultDiv = document.getElementById('result');
    const resultContent = document.getElementById('resultContent');
    const fileInput = document.getElementById('file');

    // Handle form submission
    if (uploadForm) {
        uploadForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData(uploadForm);
            const file = fileInput.files[0];
            
            if (!file) {
                alert('Please select a file first!');
                return;
            }
            
            // Show loading state
            showLoading();
            
            // Submit form via AJAX
            fetch('/predict', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                displayResult(data, file);
            })
            .catch(error => {
                console.error('Error:', error);
                hideLoading();
                alert('An error occurred while processing the image.');
            });
        });
    }

    // Preview uploaded image
    if (fileInput) {
        fileInput.addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file) {
                previewImage(file);
            }
        });
    }

    function showLoading() {
        resultContent.innerHTML = `
            <div class="text-center">
                <div class="spinner-border text-primary" role="status">
                    <span class="visually-hidden">Loading...</span>
                </div>
                <p class="mt-2">Analyzing image...</p>
            </div>
        `;
        resultDiv.style.display = 'block';
    }

    function hideLoading() {
        resultDiv.style.display = 'none';
    }

    function displayResult(data, file) {
        if (data.error) {
            resultContent.innerHTML = `
                <div class="alert alert-danger" role="alert">
                    <strong>Error:</strong> ${data.error}
                </div>
            `;
            return;
        }

        const isHealthy = data.prediction === 'Fresh/Healthy';
        const resultClass = isHealthy ? 'prediction-fresh' : 'prediction-rotten';
        const icon = isHealthy ? '🍎' : '🍎';
        const bgColor = isHealthy ? 'success' : 'danger';

        // Create image preview
        const imagePreview = URL.createObjectURL(file);

        resultContent.innerHTML = `
            <div class="row">
                <div class="col-md-6">
                    <img src="${imagePreview}" class="img-fluid rounded shadow" alt="Uploaded image">
                </div>
                <div class="col-md-6">
                    <div class="prediction-result ${resultClass}">
                        <div class="display-4 mb-3">${icon}</div>
                        <h3>Prediction: ${data.prediction}</h3>
                        <h4>Confidence: ${data.confidence}%</h4>
                        <div class="confidence-bar">
                            <div class="confidence-fill" style="width: ${data.confidence}%"></div>
                        </div>
                        <p class="mt-3">
                            ${isHealthy ? 
                                'This fruit appears to be fresh and healthy!' : 
                                'This fruit appears to be rotten or spoiled.'}
                        </p>
                    </div>
                </div>
            </div>
        `;

        // Add animation
        resultDiv.style.display = 'block';
        resultDiv.scrollIntoView({ behavior: 'smooth' });
    }

    function previewImage(file) {
        // You can add image preview functionality here if needed
        console.log('File selected:', file.name);
    }
});

// Utility functions
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

function validateImageFile(file) {
    const allowedTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif'];
    const maxSize = 16 * 1024 * 1024; // 16MB

    if (!allowedTypes.includes(file.type)) {
        return 'Please select a valid image file (JPEG, PNG, or GIF).';
    }

    if (file.size > maxSize) {
        return 'File size must be less than 16MB.';
    }

    return null; // No errors
}

// Add smooth scrolling for navigation links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth'
            });
        }
    });
});
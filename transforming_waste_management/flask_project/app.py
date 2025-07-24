from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
import tensorflow as tf
import numpy as np
from PIL import Image
import io
import os
from werkzeug.utils import secure_filename
import logging

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Change this to a random secret key

# Configuration
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

# Ensure upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Global variable to store the model
model = None

def load_model():
    """Load the trained model"""
    global model
    try:
        if os.path.exists('healthy_vs_rotten.h5'):
            model = tf.keras.models.load_model('healthy_vs_rotten.h5')
            print("Model loaded successfully!")
        else:
            print("Model file not found. Please run model_creator.py first.")
    except Exception as e:
        print(f"Error loading model: {e}")

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def preprocess_image(image):
    """Preprocess image for model prediction"""
    try:
        # Convert to RGB if necessary
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Resize image
        image = image.resize((224, 224))
        
        # Convert to array
        img_array = np.array(image)
        
        # Add batch dimension
        img_array = np.expand_dims(img_array, axis=0)
        
        # Normalize
        img_array = img_array / 255.0
        
        return img_array
    except Exception as e:
        print(f"Error preprocessing image: {e}")
        return None

@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')

@app.route('/blog')
def blog():
    """Blog listing page"""
    # Sample blog posts data
    posts = [
        {
            'id': 1,
            'title': 'Understanding Fruit Quality Detection',
            'content': 'Learn about AI-powered fruit quality assessment...',
            'author': 'Admin',
            'date': '2024-01-15'
        },
        {
            'id': 2,
            'title': 'Machine Learning in Agriculture',
            'content': 'Exploring the applications of ML in farming...',
            'author': 'Admin',
            'date': '2024-01-10'
        }
    ]
    return render_template('blog.html', posts=posts)

@app.route('/blog/<int:post_id>')
def blog_single(post_id):
    """Single blog post page"""
    # Sample blog post data
    post = {
        'id': post_id,
        'title': f'Blog Post {post_id}',
        'content': 'This is the detailed content of the blog post...',
        'author': 'Admin',
        'date': '2024-01-15'
    }
    return render_template('blog-single.html', post=post)

@app.route('/portfolio-details')
def portfolio_details():
    """Portfolio details page"""
    return render_template('portfolio-details.html')

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    """Handle image upload and prediction"""
    if request.method == 'POST':
        # Check if file was uploaded
        if 'file' not in request.files:
            flash('No file uploaded')
            return redirect(request.url)
        
        file = request.files['file']
        if file.filename == '':
            flash('No file selected')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            try:
                # Read and process image
                image = Image.open(file.stream)
                processed_image = preprocess_image(image)
                
                if processed_image is None:
                    flash('Error processing image')
                    return redirect(request.url)
                
                # Make prediction if model is loaded
                if model is not None:
                    prediction = model.predict(processed_image)
                    
                    # Interpret result
                    if prediction[0][0] > 0.5:
                        result = 'Rotten'
                        confidence = float(prediction[0][0]) * 100
                    else:
                        result = 'Fresh/Healthy'
                        confidence = float(1 - prediction[0][0]) * 100
                    
                    # Save uploaded file
                    filename = secure_filename(file.filename)
                    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    file.seek(0)  # Reset file pointer
                    file.save(filepath)
                    
                    return jsonify({
                        'prediction': result,
                        'confidence': round(confidence, 2),
                        'filename': filename
                    })
                else:
                    flash('Model not loaded. Please check server logs.')
                    return redirect(request.url)
                    
            except Exception as e:
                flash(f'Error processing image: {str(e)}')
                return redirect(request.url)
        else:
            flash('Invalid file type. Please upload an image.')
            return redirect(request.url)
    
    return render_template('index.html')

@app.errorhandler(404)
def not_found(error):
    return render_template('index.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('index.html'), 500

if __name__ == '__main__':
    # Load the model on startup
    load_model()
    
    # Run the app
    app.run(debug=True, host='0.0.0.0', port=5000)
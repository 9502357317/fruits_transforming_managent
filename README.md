# Fruit Quality Classifier - Flask Web Application

## Project Overview
This is a Flask-based web application that uses machine learning to classify fruit quality as fresh/healthy or rotten. The application uses a trained TensorFlow model to analyze uploaded fruit images and provide instant predictions.

## Features
- AI-powered fruit quality detection
- User-friendly web interface
- Real-time image analysis
- Confidence score for predictions
- Responsive design
- Blog and portfolio sections
- File upload with validation

## Project Structure
flask_project/
├── static/
│   ├── assets/          # CSS, JS, and image assets
│   ├── forms/           # Standalone HTML forms
│   └── uploads/         # Uploaded images storage
├── templates/           # HTML templates
├── app.py              # Main Flask application
├── model_creator.py    # Script to create ML model
├── healthy_vs_rotten.h5 # Trained model file
└── requirements.txt    # Python dependencies

## Installation & Setup

1. Clone or download the project files
2. Create a virtual environment:
   python -m venv venv
   
3. Activate virtual environment:
   # Windows:
   venv\Scripts\activate
   # macOS/Linux:
   source venv/bin/activate

4. Install dependencies:
   pip install -r requirements.txt

5. Create the ML model:
   python model_creator.py

6. Run the application:
   python app.py

7. Open your browser and go to:
   http://localhost:5000

## Usage
1. Navigate to the home page
2. Upload an image of a fruit
3. Click "Analyze Image"
4. View the prediction results with confidence score

## Model Information
- Input: 224x224 RGB images
- Output: Binary classification (Fresh/Healthy vs Rotten)
- Architecture: CNN with data augmentation
- Alternative: VGG16 transfer learning

## API Endpoints
- GET /              - Home page
- GET /blog          - Blog listing
- GET /blog/<id>     - Single blog post
- GET /portfolio-details - Portfolio page
- POST /predict      - Image upload and prediction

## Configuration
- Maximum file size: 16MB
- Supported formats: JPEG, PNG, GIF
- Upload directory: static/uploads/
- Model file: healthy_vs_rotten.h5

## Development
- Framework: Flask 2.3.3
- ML Library: TensorFlow 2.13.0
- Frontend: Bootstrap 5, HTML5, CSS3, JavaScript
- Image Processing: Pillow (PIL)

## Deployment
For production deployment:
1. Set Flask environment to production
2. Use a WSGI server like Gunicorn
3. Configure proper file permissions
4. Set up reverse proxy (nginx)
5. Use environment variables for sensitive data

## Troubleshooting
- If model fails to load, run model_creator.py first
- Check file permissions for uploads directory
- Ensure all dependencies are installed
- Check Python version compatibility (3.8+)

## License
This project is for educational purposes.

## Contact
For questions or support, please contact the development team.

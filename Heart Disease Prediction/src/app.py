from flask import Flask, request, jsonify, render_template, send_from_directory
import joblib
import numpy as np
import os
import pandas as pd

# Load models & scaler
scaler = joblib.load("models/scaler.pkl")
xgb_model = joblib.load("models/best_xgb_model.pkl")

# Create Flask app
app = Flask(__name__, 
            static_folder='../static',
            template_folder='../templates')

# Load feature names from the dataset
feature_names = pd.read_csv("data/heart.csv").drop(columns=["target"]).columns.tolist()

# Define the 5 essential features we'll collect from users
essential_features = ['age', 'sex', 'cp', 'trestbps', 'thalach']

# Feature descriptions for the form
feature_descriptions = {
    'age': 'Age (years)',
    'sex': 'Sex (1 = Male, 0 = Female)',
    'cp': 'Chest Pain Type (0-3)',
    'trestbps': 'Resting Blood Pressure (mm Hg)',
    'thalach': 'Maximum Heart Rate Achieved (bpm)'
}

# Recommendations based on prediction
recommendations = {
    'lifestyle': [
        'Engage in regular moderate exercise (at least 150 minutes per week)',
        'Maintain a healthy weight',
        'Quit smoking and avoid secondhand smoke',
        'Limit alcohol consumption',
        'Manage stress through meditation, yoga, or other relaxation techniques'
    ],
    'diet': [
        'Follow a heart-healthy diet rich in fruits, vegetables, and whole grains',
        'Limit saturated fats, trans fats, and cholesterol',
        'Reduce sodium intake to less than 2,300 mg per day',
        'Limit added sugars and processed foods',
        'Consider the DASH or Mediterranean diet plans'
    ],
    'medical': [
        'Schedule an appointment with your doctor as soon as possible',
        'Discuss your risk factors and symptoms with your healthcare provider',
        'Consider getting a complete lipid profile and other heart-related tests',
        'Follow your doctor\'s recommendations for medications or treatments',
        'Monitor your blood pressure and cholesterol regularly'
    ]
}

@app.route('/')
def index():
    return render_template('index.html', 
                          features=essential_features,
                          descriptions=feature_descriptions)

@app.route('/predict', methods=['POST'])
def predict():
    if request.content_type == 'application/json':
        # API request
        data = request.json
        features_dict = data['features']
    else:
        # Form submission
        features_dict = {}
        for feature in essential_features:
            features_dict[feature] = float(request.form.get(feature))
    
    # Create a complete feature vector with default values for non-essential features
    full_features = {}
    for feature in feature_names:
        if feature in features_dict:
            full_features[feature] = features_dict[feature]
        else:
            # Use default values for non-essential features
            # These are median values from the dataset
            default_values = {
                'chol': 240,
                'fbs': 0,
                'restecg': 1,
                'exang': 0,
                'oldpeak': 0.8,
                'slope': 1,
                'ca': 0,
                'thal': 2
            }
            full_features[feature] = default_values.get(feature, 0)
    
    # Convert to numpy array in the correct order
    features_array = np.array([full_features[f] for f in feature_names]).reshape(1, -1)
    
    # Scale features
    features_scaled = scaler.transform(features_array)
    
    # Make prediction
    prediction = int(xgb_model.predict(features_scaled)[0])
    probability = float(xgb_model.predict_proba(features_scaled)[0][1])
    
    if request.content_type == 'application/json':
        return jsonify({
            "prediction": prediction,
            "probability": probability,
            "recommendations": recommendations if prediction == 1 else {}
        })
    else:
        return render_template('result.html', 
                              prediction=prediction,
                              probability=probability,
                              recommendations=recommendations)

@app.route('/faq')
def faq():
    return render_template('faq.html')

@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory(app.static_folder, path)

if __name__ == '__main__':
    # Create directories if they don't exist
    os.makedirs('../templates', exist_ok=True)
    os.makedirs('../static/css', exist_ok=True)
    os.makedirs('../static/js', exist_ok=True)
    
    app.run(debug=True)

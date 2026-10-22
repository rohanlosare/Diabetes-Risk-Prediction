import os
import pickle
from flask import Flask, render_template_string, request

app = Flask(__name__)

# Load the SVM model
model_path = 'svm.pkl'
with open(model_path, 'rb') as f:
  model = pickle.load(f)

# HTML Template with Embedded Modern Styling & Responsive Layout
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Health Risk Assessment Portal</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --primary: #4f46e5;
            --primary-hover: #4338ca;
            --bg-color: #f1f5f9;
            --card-bg: #ffffff;
            --text-main: #1e293b;
            --text-muted: #64748b;
            --border-color: #cbd5e1;
        }
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: 'Inter', sans-serif;
        }
        body {
            background-color: var(--bg-color);
            color: var(--text-main);
            line-height: 1.5;
            padding: 40px 20px;
        }
        .container {
            max-width: 850px;
            margin: 0 auto;
            background: var(--card-bg);
            border-radius: 16px;
            box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.05), 0 8px 10px -6px rgba(0, 0, 0, 0.05);
            overflow: hidden;
            border: 1px solid #e2e8f0;
        }
        .header {
            background: linear-gradient(135deg, #4f46e5 0%, #3b82f6 100%);
            color: white;
            padding: 35px 30px;
            text-align: center;
        }
        .header h1 {
            font-size: 26px;
            font-weight: 700;
            margin-bottom: 8px;
        }
        .header p {
            font-size: 14px;
            opacity: 0.9;
        }
        .form-container {
            padding: 35px 30px;
        }
        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
            gap: 20px;
        }
        .form-group {
            display: flex;
            flex-direction: column;
        }
        label {
            font-size: 13px;
            font-weight: 600;
            color: var(--text-main);
            margin-bottom: 6px;
        }
        input, select {
            padding: 10px 14px;
            border: 1px solid var(--border-color);
            border-radius: 8px;
            font-size: 14px;
            color: var(--text-main);
            background-color: #fff;
            transition: all 0.2s ease;
        }
        input:focus, select:focus {
            outline: none;
            border-color: var(--primary);
            box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.15);
        }
        .btn-submit {
            grid-column: 1 / -1;
            background-color: var(--primary);
            color: white;
            border: none;
            border-radius: 8px;
            padding: 14px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: background-color 0.2s;
            margin-top: 15px;
        }
        .btn-submit:hover {
            background-color: var(--primary-hover);
        }
        .result-card {
            margin-top: 30px;
            padding: 20px;
            background-color: #e0e7ff;
            border-radius: 10px;
            text-align: center;
            border: 1px solid #c7d2fe;
        }
        .result-card h3 {
            color: #312e81;
            font-size: 16px;
            margin-bottom: 6px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        .result-card p {
            color: #3730a3;
            font-size: 22px;
            font-weight: 700;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>SVM Model Prediction Portal</h1>
            <p>Provide your features below to run the classification model.</p>
        </div>
        <div class="form-container">
            <form method="POST">
                <div class="grid">
                    <div class="form-group">
                        <label for="age">Age</label>
                        <input type="number" step="any" id="age" name="age" required placeholder="e.g., 40">
                    </div>
                    <div class="form-group">
                        <label for="gender">Gender (Code)</label>
                        <input type="number" step="any" id="gender" name="gender" required placeholder="e.g., 1">
                    </div>
                    <div class="form-group">
                        <label for="city">City Code</label>
                        <input type="number" step="any" id="city" name="city" required placeholder="e.g., 3">
                    </div>
                    <div class="form-group">
                        <label for="bmi">BMI</label>
                        <input type="number" step="any" id="bmi" name="bmi" required placeholder="e.g., 25.4">
                    </div>
                    <div class="form-group">
                        <label for="family_history_diabetes">Family History Diabetes</label>
                        <input type="number" step="any" id="family_history_diabetes" name="family_history_diabetes" required placeholder="0 or 1">
                    </div>
                    <div class="form-group">
                        <label for="physical_activity_level">Physical Activity Level</label>
                        <input type="number" step="any" id="physical_activity_level" name="physical_activity_level" required placeholder="e.g., 2">
                    </div>
                    <div class="form-group">
                        <label for="diet_type">Diet Type</label>
                        <input type="number" step="any" id="diet_type" name="diet_type" required placeholder="e.g., 1">
                    </div>
                    <div class="form-group">
                        <label for="smoking_status">Smoking Status</label>
                        <input type="number" step="any" id="smoking_status" name="smoking_status" required placeholder="0 or 1">
                    </div>
                    <div class="form-group">
                        <label for="alcohol_consumption">Alcohol Consumption</label>
                        <input type="number" step="any" id="alcohol_consumption" name="alcohol_consumption" required placeholder="0 or 1">
                    </div>
                    <div class="form-group">
                        <label for="hours_sleep_per_night">Hours Sleep Per Night</label>
                        <input type="number" step="any" id="hours_sleep_per_night" name="hours_sleep_per_night" required placeholder="e.g., 7">
                    </div>
                    <div class="form-group">
                        <label for="stress_level">Stress Level</label>
                        <input type="number" step="any" id="stress_level" name="stress_level" required placeholder="e.g., 3">
                    </div>
                    <div class="form-group">
                        <label for="fasting_blood_sugar">Fasting Blood Sugar</label>
                        <input type="number" step="any" id="fasting_blood_sugar" name="fasting_blood_sugar" required placeholder="e.g., 100">
                    </div>
                    <div class="form-group">
                        <label for="hba1c_level">HbA1c Level</label>
                        <input type="number" step="any" id="hba1c_level" name="hba1c_level" required placeholder="e.g., 5.5">
                    </div>
                    <div class="form-group">
                        <label for="blood_pressure_systolic">BP Systolic</label>
                        <input type="number" step="any" id="blood_pressure_systolic" name="blood_pressure_systolic" required placeholder="e.g., 120">
                    </div>
                    <div class="form-group">
                        <label for="blood_pressure_diastolic">BP Diastolic</label>
                        <input type="number" step="any" id="blood_pressure_diastolic" name="blood_pressure_diastolic" required placeholder="e.g., 80">
                    </div>
                    <div class="form-group">
                        <label for="waist_circumference_cm">Waist Circumference (cm)</label>
                        <input type="number" step="any" id="waist_circumference_cm" name="waist_circumference_cm" required placeholder="e.g., 85">
                    </div>
                    <div class="form-group">
                        <label for="income_bracket">Income Bracket</label>
                        <input type="number" step="any" id="income_bracket" name="income_bracket" required placeholder="e.g., 2">
                    </div>
                    <button type="submit" class="btn-submit">Calculate Prediction</button>
                </div>
            </form>

            {% if prediction is not none %}
            <div class="result-card">
                <h3>Model Output</h3>
                <p>{{ prediction }}</p>
            </div>
            {% endif %}
        </div>
    </div>
</body>
</html>
"""


@app.route('/', methods=['GET', 'POST'])
def home():
  prediction = None
  if request.method == 'POST':
    try:
      # Map form fields to the exact 17 feature sequence expected by your model
      features = [
          float(request.form['age']),
          float(request.form['gender']),
          float(request.form['city']),
          float(request.form['bmi']),
          float(request.form['family_history_diabetes']),
          float(request.form['physical_activity_level']),
          float(request.form['diet_type']),
          float(request.form['smoking_status']),
          float(request.form['alcohol_consumption']),
          float(request.form['hours_sleep_per_night']),
          float(request.form['stress_level']),
          float(request.form['fasting_blood_sugar']),
          float(request.form['hba1c_level']),
          float(request.form['blood_pressure_systolic']),
          float(request.form['blood_pressure_diastolic']),
          float(request.form['waist_circumference_cm']),
          float(request.form['income_bracket']),
      ]

      # Run prediction
      pred = model.predict([features])[0]
      prediction = f'Predicted Class: {pred}'
    except Exception as e:
      prediction = f'Error: {str(e)}'

  return render_template_string(HTML_TEMPLATE, prediction=prediction)


if __name__ == '__main__':
  port = int(os.environ.get('PORT', 5000))
  app.run(host='0.0.0.0', port=port)

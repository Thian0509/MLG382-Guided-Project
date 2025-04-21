from flask import Flask, render_template, Response, request
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64
import numpy as np
import joblib

app = Flask(__name__)

# Load the dataset
df = pd.read_csv('Student_performance_data.csv')

# Load the trained Random Forest model
model = joblib.load('model.pkl')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/grade-class-distribution')
def grade_class_distribution():
    # Generate the plot
    plt.figure(figsize=(8, 4))
    sns.countplot(data=df, x='GradeClass', palette='viridis')
    plt.title('Distribution of Grade Classes')
    plt.xlabel('Grade Class (0:A, 1:B, 2:C, 3:D, 4:F)')
    plt.ylabel('Number of Students')

    # Save the plot to a BytesIO object
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    plt.close()
    return render_template('plot.html', plot_url=plot_url)

@app.route('/absences-distribution')
def absences_distribution():
    # Generate the plot
    plt.figure(figsize=(8, 4))
    sns.histplot(data=df, x='Absences', bins=20, kde=True, color='blue')
    plt.title('Absences Distribution')
    plt.xlabel('Number of Absences')
    plt.ylabel('Frequency')

    # Save the plot to a BytesIO object
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    plt.close()
    return render_template('plot.html', plot_url=plot_url)

@app.route('/parental-support-distribution')
def parental_support_distribution():
    # Generate the plot
    plt.figure(figsize=(8, 4))
    sns.countplot(data=df, x='ParentalSupport', palette='Set2')
    plt.title('Parental Support Distribution')
    plt.xlabel('Parental Support')
    plt.ylabel('Number of Students')

    # Save the plot to a BytesIO object
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    plt.close()
    return render_template('plot.html', plot_url=plot_url)

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        # Get form data
        parental_education = int(request.form['ParentalEducation'])
        study_time_weekly = float(request.form['StudyTimeWeekly'])
        absences = int(request.form['Absences'])
        tutoring = int(request.form['Tutoring'])
        parental_support = int(request.form['ParentalSupport'])
        gpa = float(request.form['GPA'])

        # Create a DataFrame for the input
        input_data = pd.DataFrame({
            'ParentalEducation': [parental_education],
            'StudyTimeWeekly': [study_time_weekly],
            'Absences': [absences],
            'Tutoring': [tutoring],
            'ParentalSupport': [parental_support],
            'GPA': [gpa]
        })

        # Make a prediction
        prediction = model.predict(input_data)[0]

        # Map the prediction to grade class
        grade_class_mapping = {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'F'}
        predicted_grade = grade_class_mapping[prediction]

        return render_template('result.html', grade=predicted_grade)

    return render_template('predict.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
from flask import Flask, render_template, Response
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64

app = Flask(__name__)

# Load the dataset
df = pd.read_csv('Student_performance_data.csv')

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
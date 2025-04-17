from flask import Flask, render_template, request
import numpy as np
from tensorflow.keras.models import load_model
from sklearn.preprocessing import LabelEncoder
import pandas as pd
import numpy as np

app = Flask(__name__)

model = load_model('fil.h5')
label_encoder = LabelEncoder()



df = pd.read_csv('nn.csv')
X = df.drop('highest_priority_subject', axis=1)
y = df['highest_priority_subject']


label_encoder.fit(y)

@app.route('/')
def home():
    return render_template('hlo.html')

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/student')
def student():
    return render_template('student.html')

@app.route('/teacher')
def teacher():
    return render_template('teacher.html')

@app.route('/studentinfo', methods=['POST'])
def student_info():
    if request.method == 'POST':
        # Process the form data here
        username = request.form.get('username')
        password = request.form.get('password')


        return render_template('studentinfo.html') 

    return render_template('error.html')

@app.route('/contests')
def contests():
    return render_template('contest.html')

@app.route('/quiz')
def quiz():
    return render_template('quiz.html')

@app.route('/assignments')
def assignments():
    return render_template('Assignments.html')

@app.route('/benefits')
def benefits():
    return render_template('benefits.html')

@app.route('/points')
def points():
    return render_template('points.html')


@app.route('/academic_assignments')
def academic_assignments():
    return render_template('AcademicAssignments.html')

@app.route('/sports_achievements')
def sports_achievements():
    return render_template('SportsAchievements.html')

@app.route('/co_curricular_assignments')
def co_curricular_assignments():
    return render_template('CoCurricularAssignments.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/help')
def help():
    return render_template('help.html')


@app.route('/predict', methods=['POST'])
def predict():
    try:
       
        user_input = [float(request.form[f'score{i}']) for i in range(1,24)]
        
        user_input = np.array([user_input])

        if user_input.shape != (1, 23):
            raise ValueError("Invalid input shape. Expected shape (1, 23).")

        probabilities = model.predict(user_input)
        predicted_classes = np.argmax(probabilities, axis=1)

        if not label_encoder.classes_.any():
            raise ValueError("LabelEncoder is not fitted yet. Call 'fit' with appropriate arguments before using this estimator.")

        decoded_prediction = label_encoder.inverse_transform(predicted_classes)[0]

        recommendations = {
            'Maths': {'degree': 'STEM', 'career': 'Engineer'},
            'Physics': {'degree': 'NDA', 'career': 'IAF'},
            'Biology': {'degree': 'BIPC', 'career': 'Doctor'},
            'Chemistry': {'degree': 'Pharmacy', 'career': 'Pharmaceutical'},
            'Economics': {'degree': 'Commerce', 'career': 'CA'},
            'Civics': {'degree': 'Political Science', 'career': 'Politics'},
            'C': {'degree': 'CSE', 'career': 'Software'},
            'C++': {'degree': 'CSE', 'career': 'Software'},
            'Python': {'degree': 'CSE', 'career': 'Physicist'},
            'History': {'degree': 'Humanities', 'career': 'Government Job'},
            'Geography': {'degree': 'Arts', 'career': 'Analyst'},
            'Running': {'degree': 'Athletic Academy', 'career': 'Athletes/Government Job'},
            'Shoutput': {'degree': 'Sports Academy', 'career': 'Athletes/Government Job'},
            'Longjump': {'degree': 'Sports Academy', 'career': 'Athletes/Government Job'},
            'Highjump': {'degree': 'Sports Academy', 'career': 'Athletes/Government Job'},
            'Javelinthrow': {'degree': 'Sports Academy', 'career': 'Athletes/Government Job'},
            'Cricket': {'degree': 'Cricket Coaching', 'career': 'Cricketer'},
            'Football': {'degree': 'PIFA', 'career': 'Footballer'},
            'Volleyball': {'degree': 'SVA', 'career': 'Athletes/Government Job'},
            'Hockey': {'degree': 'Academy', 'career': 'Athletes/Government Job'},
            'Kabaddi': {'degree': 'Academy', 'career': 'Athletes/Government Job'},
            'Dance': {'degree': 'Dance Club', 'career': 'Dance Club'},
            'Music': {'degree': 'Music Club', 'career': 'Music Club'}
        }

        if decoded_prediction in recommendations:
            recommended_degree = recommendations[decoded_prediction]['degree']
            recommended_career = recommendations[decoded_prediction]['career']
        else:
            recommended_degree = 'Unknown'
            recommended_career = 'Unknown'

        return render_template('result.html', prediction=decoded_prediction,
                               recommended_degree=recommended_degree, recommended_career=recommended_career)

    except Exception as e:
        return render_template('error.html', error=str(e))


if __name__ == '__main__':
    app.run(debug=True)

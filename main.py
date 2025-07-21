from flask import Flask, request, render_template

app = Flask(__name__)

student_list = [{
    "Student": "Dalia",
    "Shifts": {
        "AM": ["Monday", "Tuesday"],
        "PM": ["Friday"],
        "Current Shifts": ""
    },
    "Number of Shifts": 0
    },
    {
    "Student": "Aanshi",
    "Shifts": {
        "AM": ["Friday", "Saturday", "Monday"],
        "PM": ["Tuesday"],
        "Current Shifts": ""
    },
    "Number of Shifts": 0
    },
    {
    "Student": "Daniel",
    "Shifts": {
        "AM": ["Tuesday"],
        "PM": ["Tuesday"],
        "Current Shifts": ""
    },
    "Number of Shifts": 0
    }]

# clinic shifts are structured [day, time, capacity]
clinic_list = [{
    "Clinic": "Health Center A",
    "Shifts": {
        "AM": [["Monday", "10", "5"], ["Tuesday", "11", "4"]],
        "PM": [['Wednesday', '2', '1'], ['Friday', "3", "2"]]
    }},
    {
    "Clinic": "Health Center B",
    "Shifts": {
        "AM": [["Tuesday", "12", "3"], ["Wednesday", "11", "4"]],
        "PM": [['Wednesday', '2', '3'], ['Friday', "3", "2"]]
    }
    }]
assignments = []
shift_days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']

@app.route('/', methods=['POST', 'GET'])
def home():
    if request.method == "POST":
        student_list.append({
            "Student": request.form['student'],
            "Shifts": {
                "AM": request.form['AMavailability'].split(),
                "PM": request.form['PMavailability'].split(),
                "Current Shifts": ""
            },
            "Number of Shifts": 0
        })
    return render_template('index.html', student_list = student_list)

@app.route('/clinic', methods=['POST', 'GET']) 
def clinic():
    # ideally there will be more students than clinics 
    if (len(clinic_list) >= 1 and len(student_list) >= 1):
        for clinic in clinic_list:
            for student in student_list:
                for student_day in student["Shifts"]["AM"]:
                    for i, shift in enumerate(clinic['Shifts']['AM']):
                        shift_day, time, capacity = shift
                        if shift_day == student_day and int(capacity) >= 1 and shift_day not in student["Shifts"]["Current Shifts"]:
                            assignments.append({
                                "Student": student['Student'],
                                "Assigned Clinic": clinic['Clinic'],
                                "Time": shift_day, 
                                "Session": "AM"
                                })
                            clinic['Shifts']['AM'][i][2] = str(int(capacity) - 1)
                            student["Shifts"]["Current Shifts"] = student["Shifts"]["Current Shifts"] + " " + shift_day 
                            student["Number of Shifts"] += 1
                for student_day in student["Shifts"]["PM"]:
                    for i, shift in enumerate(clinic['Shifts']['PM']):
                        shift_day, time, capacity = shift
                        if shift_day == student_day and int(capacity) >= 1 and shift_day not in student["Shifts"]["Current Shifts"]:
                            assignments.append({
                                "Student": student['Student'],
                                "Assigned Clinic": clinic['Clinic'],
                                "Time": shift_day, 
                                "Session": "PM"
                                })
                            clinic['Shifts']['PM'][i][2] = str(int(capacity) - 1)
                            student["Shifts"]["Current Shifts"] = student["Shifts"]["Current Shifts"] + " " + shift_day 
                            student["Number of Shifts"] += 1
        print(student_list)
    return render_template('clinic_matching.html', assignments=assignments, clinic_list=clinic_list, student_list=student_list)

@app.route('/matching')
def matching():
    return render_template('matching.html', assignments=assignments, shift_days=shift_days)


if __name__ == "__main__":
    app.run(debug=True)
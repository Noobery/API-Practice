from flask import Flask, jsonify, request
import sys
import psycopg2 # postgres


# Database Connection

db_connection = psycopg2.connect(
    dbname = "postgres",
    user = "postgres",
    password = "123",
    host = "localhost"
)

app = Flask(__name__)

def spcall(qry, param, commit=False):
    try:
        cursor = db_connection.cursor()
        cursor.callproc(qry, param)
        res = cursor.fetchall()
        if commit:
            db_connection.commit()
        return res
    except:
        res = [("Error: " + str(sys.exc_info()[0]) +
                " " + str(sys.exc_info()[1]),)]
    return res

@app.route('/courses', methods=['GET'])
def get_courses():
    try:
        courses=spcall('get_courses', param=None)[0][0]
        return jsonify({"status": "ok",
                        'Message': courses})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route('/course', methods=['POST'])
def create_course():
    data = request.get_json()
    course = data.get('course')
    try:
        if course:
            print(f'Received course: {course}')
            res = spcall('insert_course', (course,), commit=True)
            return jsonify({"status": "ok", 'message': 'course created successfully'})
        else:
            return jsonify({"status": "error", "message": "Course name is missing"})
    except Exception as e:
        print(f'Error: {e}')
        return jsonify({"status": "error", "message": str(e)})


# Get a specific course by ID
@app.route('/course/<int:course_id>', methods=['GET'])
def get_course(course_id):
    try:
        res = spcall('get_course_by_id', (course_id, ), commit=False)[0][0]
        return jsonify({"status": "ok",
                            'message': res})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route('/course/<int:course_id>', methods=['PUT'])
def update_course(course_id):
    try:
        data = request.get_json()
        course = data.get('course')

        if course:
            # Assuming spcall executes the update operation in the database
            res = spcall('update_course_by_id', (course_id, course), commit=True)
            return jsonify({"status": "ok", "message": "Course updated successfully"})
        else:
            return jsonify({"status": "error", "message": "No course data provided"})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

# Delete a course by ID
@app.route('/course/<int:course_id>', methods=['DELETE'])
def delete_course(course_id):
    try:
        res = spcall('delete_course_by_id', (course_id, ), commit=True)
        return jsonify({"status": "ok",
                        'message': 'course deleted successfully'})
    except:
        return {"status":"error", "message":str(sys.exc_info()[0]) +
                " " + str(sys.exc_info()[1])}


#STUDENTS API

@app.route('/students', methods=['GET'])
def get_students():
    try:
        students =spcall('get_students', param=None)[0][0]
        return jsonify({"status": "ok",
                        'Message': students})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route('/student', methods=['POST'])
def create_student():
    data = request.get_json()
    student = data.get('student')
    course_id = data.get('course_id')
    try:
        if student:
            res=spcall('insert_student', (student, course_id), commit=True)
            return jsonify({"status": "ok",
                        'message': 'student created successfully'})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})


# Get a specific student by ID
@app.route('/student/<int:student_id>', methods=['GET'])
def get_student(student_id):
    try:
        res = spcall('get_student_by_id', (student_id, ), commit=False)[0][0]
        return jsonify({"status": "ok",
                            'message': res})
                            
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

# Update a student by ID
@app.route('/student/<int:student_id>', methods=['PUT'])
def update_student(student_id):
    try:
        data = request.get_json()
        student = data.get('student')
        course_id = data.get('course_id')

        if student:
            res = spcall('update_student_by_id', (student_id, student, course_id), commit=True)
            return jsonify({"status": "ok", 'message': 'student updated successfully'})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

# Delete a student by ID
@app.route('/student/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    try:
        res = spcall('delete_student_by_id', (student_id, ), commit=True)
        return jsonify({"status": "ok",
                        'message': 'student deleted successfully'})
    except:
        return {"status":"error", "message":str(sys.exc_info()[0]) +
                " " + str(sys.exc_info()[1])}


if __name__ == '__main__':
    app.run(debug=True, port = 5001)
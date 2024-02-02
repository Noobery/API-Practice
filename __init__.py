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
        res = [("Error: " + str(sys.exc_info()[0]) + " " + str(sys.exc_info()[1]),)]

    return res

# Get course function
@app.route("/courses", methods=['GET'])
def get_courses():
    try:
        courses = spcall('get_courses', param=None)
        return jsonify({
            "status": "success",
            "data": courses})
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)})
    
# Create course function
@app.route('/course', methods=['POST'])
def create_course():
    data = request.get_json()
    course = data.get('course')
    try:
        if course:
            res = spcall('insert_course', (course,), commit=True)
            return jsonify({
                "status": "success",
                "message": res
            })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        })

    
if __name__ == '__main__':
    app.run(debug=True)
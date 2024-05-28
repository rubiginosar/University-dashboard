from flask import Flask, render_template, request, redirect, jsonify, make_response
import json
from flask_mysqldb import MySQL
from flask import jsonify

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'pass_root'
app.config['MYSQL_DB'] = 'db_university'
app.config['MYSQL_PORT'] = 3307

mysql = MySQL(app)



@app.route('/details', methods=['GET', 'POST'])
def details():
    return render_template('analytics.html')  


@app.route('/edit', methods=['GET', 'POST'])
def edit():
    return render_template('edit.html');

@app.route('/api/dashboard_data')
def getDashboardData():
    try:
        conn = mysql.connect
        cursor = conn.cursor()

        # Fetch data for students by year
        cursor.execute("SELECT ANNEE, COUNT(*) AS num_students FROM resultats GROUP BY ANNEE;")
        year_data = cursor.fetchall()
        year_labels = [x[0] for x in cursor.description]
        year_json_data = []
        for result in year_data:
            year_json_data.append(dict(zip(year_labels, result)))

        # Fetch data for students by gender
        gender_data = {"labels": [], "data": []}
        cursor.execute("SELECT DISTINCT sexe FROM resultats")
        genders_tuple = cursor.fetchall()
        genders_list = [item[0] for item in genders_tuple]
        for gender in genders_list:
            cursor.execute("SELECT COUNT(*) FROM resultats WHERE sexe = %s", (gender,))
            count = cursor.fetchone()[0]
            gender_data["labels"].append(gender)
            gender_data["data"].append(count)

        # Fetch data for students by specialty
        specialty_data = {"labels": [], "data": []}
        cursor.execute("SELECT DISTINCT SPECIALITE FROM resultats")
        specialties_tuple = cursor.fetchall()
        specialties_list = [item[0] for item in specialties_tuple]
        for specialty in specialties_list:
            cursor.execute("SELECT COUNT(*) FROM resultats WHERE SPECIALITE = %s", (specialty,))
            count = cursor.fetchone()[0]
            specialty_data["labels"].append(specialty)
            specialty_data["data"].append(count)

        cursor.close()

        return jsonify({
            "year_data": year_json_data,
            "gender_data": gender_data,
            "specialty_data": specialty_data
        })

    except Exception as e:
        return jsonify({'error': str(e)})


@app.route('/total_counts')
def total_counts():
    try:
        conn = mysql.connect
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) AS total_students FROM resultats")
        total_students = cursor.fetchone()[0]

        # Count the total number of specialties
        cursor.execute("SELECT COUNT(DISTINCT SPECIALITE) FROM resultats")
        total_specialties = cursor.fetchone()[0]

        # Count the total number of years
        cursor.execute("SELECT COUNT(DISTINCT ANNEE) FROM resultats")
        total_years = cursor.fetchone()[0]

        cursor.execute("SELECT AVG(moyenne) AS average_moyenne FROM resultats")
        average_moyenne = cursor.fetchone()[0]
        average_moyenne = round(average_moyenne, 2)  # Round to two decimal places

        cursor.execute("SELECT COUNT(*) AS successful_students FROM resultats WHERE moyenne >= 10")
        successful_students = cursor.fetchone()[0]
        percentage_success = round((successful_students / total_students) * 100, 2) if total_students > 0 else 0  # Round the percentage to two decimal places

        cursor.close()

        # Return the total counts of specialties, years, and students in JSON format
        return jsonify({
            "total_students": total_students,
            "total_specialties": total_specialties,
            "total_years": total_years,
            "average_moyenne": average_moyenne,
            "percentage_success": percentage_success
        })

    except Exception as e:
        return jsonify({'error': str(e)})


def execute_query(query, values=None):
    try:
        conn = mysql.connection
        cursor = conn.cursor()
        if values:
            cursor.execute(query, values)
        else:
            cursor.execute(query)
        conn.commit()
        cursor.close()
        return True
    except Exception as e:
        print(f"Error: {str(e)}")
        return False

@app.route('/api/persons', methods=["GET"])
def selectPersons():
    try:
        conn = mysql.connection
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM resultats")  # Fetch data from the 'resultats' table
        data = cursor.fetchall()
        row_headers = [x[0] for x in cursor.description]
        cursor.close()
        
        json_data = []
        for result in data:
            json_data.append(dict(zip(row_headers, result)))

        return make_response(jsonify(json_data), 200)

    except Exception as e:
        return make_response(jsonify({"error": "Erreur lors de la requête SQL"}), 500)

@app.route('/api/persons', methods=["POST"])
def insertPerson():
    try:
        nom = request.form.get("valNom")
        prenom = request.form.get("valPrenom")
        points = request.form.get("valPoints")
        sexe = request.form.get("valSexe")
        specialite = request.form.get("valSpecialite")
        matricule = request.form.get("valMatricule")
        annee = request.form.get("valAnnee")

        cursor = mysql.connection.cursor()

        query = "INSERT INTO resultats (annee, matricule, nom, prenom, sexe, specialite, moyenne) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        values = (annee, matricule, nom, prenom, sexe, specialite, points)
       
        success = execute_query(query, values)

        if success:
            return make_response("", 201)  # Empty response with success status code (201)
        else:
            return make_response(jsonify({"error": "Erreur lors de l'insertion"}), 500)


    except Exception as e:
        return make_response(jsonify({"error": "Erreur lors de l'insertion"}), 500)
@app.route('/api/persons/<int:annee>/<int:matricule>', methods=["PUT"])
def updatePerson(annee, matricule):
    try:
        nom = request.form.get("valNom")
        prenom = request.form.get("valPrenom")
        points = request.form.get("valPoints")
        sexe = request.form.get("valSexe")
        specialite = request.form.get("valSpecialite")
        new_annee = request.form.get("valAnnee")
        new_matricule = request.form.get("valMatricule")

        query = "UPDATE resultats SET annee=%s, matricule=%s, nom=%s, prenom=%s, sexe=%s, specialite=%s, moyenne=%s WHERE annee=%s AND matricule=%s"
        values = (new_annee, new_matricule, nom, prenom, sexe, specialite, points, annee, matricule)
        success = execute_query(query, values)

        if success:
            return make_response("Record updated", 200)
        else:
            return make_response(jsonify({"error": "Erreur lors de la mise à jour"}), 500)

    except Exception as e:
        return make_response(jsonify({"error": "Erreur lors de la mise à jour"}), 500)


@app.route('/api/persons/<int:annee>/<int:matricule>', methods=["DELETE"])
def deletePerson(annee, matricule):
    try:
        # Adjust your SQL DELETE query to match your database schema and use these parameters
        query = "DELETE FROM resultats WHERE annee=%s AND matricule=%s "
        success = execute_query(query, (annee, matricule))

        if success:
            return make_response("Record deleted", 204)
        else:
            return make_response(jsonify({"error": "Erreur lors de la suppression"}), 500)

    except Exception as e:
        return make_response(jsonify({"error": "Erreur lors de la suppression"}), 500)
@app.route('/api/persons/search', methods=['GET'])
def search_persons():
    term = request.args.get('term')
    term_as_int = None

    # Check if the term can be converted into an integer
    try:
        term_as_int = int(term)
    except ValueError:
        pass  # Do nothing if it's not a valid integer

    cur = mysql.connection.cursor()

    if term_as_int is not None:
        # Perform a database query to find persons by matricule if term is an integer
        cur.execute(f"SELECT * FROM resultats WHERE matricule = {term_as_int} OR annee= {term_as_int}")
    else:
        # Perform a database query to find persons matching the search term in other columns
        cur.execute(f"SELECT * FROM resultats WHERE nom LIKE '%{term}%' OR prenom LIKE '%{term}%' OR specialite LIKE '%{term}%'")

    rows = cur.fetchall()

    # Transform the query results into a list of dictionaries
    search_results = []
    for row in rows:
        result = {
            'annee': row[0],
            'matricule': row[1],
            'nom': row[2],
            'prenom': row[3],
            'sexe': row[4],
            'specialite': row[5],
            'moyenne': row[6]
        }
        search_results.append(result)

    return jsonify(search_results)

@app.route('/api/dashboard_data2')
def getDashboardData2():
    try:
        conn = mysql.connect
        cursor = conn.cursor()

        # Calculate success percentage per year and sex
        # cursor.execute("SELECT sexe, COUNT(*) AS num_success FROM resultats WHERE moyenne >= 10 GROUP BY sexe")
        # success_by_sex = cursor.fetchall()
        # sex_labels = [x[0] for x in cursor.description]

        # success_data = []
        # for success in success_by_sex:
        #     success_dict = dict(zip(sex_labels, success))
        #     success_data.append(success_dict)
        # Calculate success percentage per sex
        cursor.execute("SELECT sexe, COUNT(*) AS num_success FROM resultats WHERE moyenne >= 10 GROUP BY sexe")
        success_by_sex = cursor.fetchall()
        sex_labels = [x[0] for x in cursor.description]

        success_data = []
        for success in success_by_sex:
            success_dict = dict(zip(sex_labels, success))

            # Calculate the total count of students by sex
            sex_value = success_dict['sexe']
            cursor.execute("SELECT COUNT(*) AS total_students FROM resultats WHERE sexe = %s", (sex_value,))
            total_students = cursor.fetchone()[0]

            # Calculate success percentage per sex
            total_count = success_dict['num_success']
            success_percentage = (total_count / total_students) * 100 if total_students > 0 else 0
            success_dict['success_percentage'] = success_percentage

            success_data.append(success_dict)

        # Calculate average per sex
        cursor.execute("SELECT sexe, AVG(moyenne) AS avg_moyenne FROM resultats GROUP BY sexe")
        avg_by_sex = cursor.fetchall()
        avg_labels = [x[0] for x in cursor.description]

        avg_data = []
        for avg in avg_by_sex:
            avg_dict = dict(zip(avg_labels, avg))
            avg_data.append(avg_dict)
            
        cursor.execute("SELECT ANNEE, COUNT(*) AS num_success FROM resultats WHERE moyenne >= 10 GROUP BY ANNEE")
        success_by_year = cursor.fetchall()
        year_labels = [x[0] for x in cursor.description]

        year_data1 = []
        for year in success_by_year:
            year_dict = dict(zip(year_labels, year))

            # Calculate the total count of students in this year
            year_value = year_dict['ANNEE']
            cursor.execute("SELECT COUNT(*) AS total_students FROM resultats WHERE ANNEE = %s", (year_value,))
            total_students = cursor.fetchone()[0]  # Fetch the count directly

            # Calculate success percentage per year
            total_count = year_dict['num_success']
            success_percentage = (total_count / total_students) * 100 if total_students > 0 else 0
            year_dict['success_percentage'] = success_percentage

            year_data1.append(year_dict)

        cursor.execute("SELECT SPECIALITE, COUNT(*) AS num_success FROM resultats WHERE moyenne >= 10 GROUP BY SPECIALITE")
        success_by_specialty = cursor.fetchall()
        specialty_labels = [x[0] for x in cursor.description]

        specialty_data = []
        for specialty in success_by_specialty:
            specialty_dict = dict(zip(specialty_labels, specialty))

            # Calculate the total count of students in this specialty
            specialty_name = specialty_dict['SPECIALITE']
            cursor.execute("SELECT COUNT(*) AS total_students FROM resultats WHERE SPECIALITE = %s", (specialty_name,))
            total_students = cursor.fetchone()[0]  # Fetch the count directly

            # Calculate success percentage per specialty
            total_count = specialty_dict['num_success']
            success_percentage = (total_count / total_students) * 100 if total_students > 0 else 0
            specialty_dict['success_percentage'] = success_percentage

            specialty_data.append(specialty_dict)
        cursor.execute("SELECT SPECIALITE, AVG(moyenne) AS avg_moyenne FROM resultats GROUP BY SPECIALITE")
        average_by_speciality = cursor.fetchall()
        specialty_labels = [x[0] for x in cursor.description]

        average_data = []
        for specialty in average_by_speciality:
            specialty_dict = dict(zip(specialty_labels, specialty))
            average_data.append(specialty_dict)

        # cursor.execute("SELECT ANNEE, AVG(moyenne) AS avg_moyenne FROM resultats GROUP BY ANNEE")
        # average_by_year = cursor.fetchall()
        # year_labels = [x[0] for x in cursor.description]

        # average_data_by_year = []
        # for year_data in average_by_year:
        #     year_dict = dict(zip(year_labels, year_data))
        #     average_data_by_year.append(year_dict)
        cursor.execute("SELECT ANNEE, AVG(moyenne) AS avg_moyenne FROM resultats GROUP BY ANNEE")
        average_by_year = cursor.fetchall()

        average_data_by_year = {}
        for year_data in average_by_year:
            year_dict = {
                str(year_data[0]): {
                    "avg_moyenne": year_data[1]
                }
            }
            average_data_by_year.update(year_dict)


        cursor.execute("SELECT moyenne FROM resultats")
        all_moyenne_values = cursor.fetchall()
        moyenne_values = [moyenne[0] for moyenne in all_moyenne_values]
        cursor.close()

        return jsonify({
            "success_by_sex": success_data,
            "success_by_speciality": specialty_data,
            "success_by_year": year_data1,
            "average_moyenne_by_speciality": average_data,
            "average_moyenne_by_year_speciality": average_data_by_year,
            "all_moyenne_values": moyenne_values,
            "average_by_sexe":avg_data
        })

    except Exception as e:
        return jsonify({'error': str(e)})



@app.route('/', methods=["GET"])
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)

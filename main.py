from flask import Flask, jsonify, request, render_template
from flask_mysqldb import MySQL
import pymysql

app = Flask(__name__)

mysql = MySQL(app)

# Connect to the MySQL database
def connect_to_database():
    try:
        db_connection = mysql.connect(
            host="localhost",
            user="root",
            password="1234",
            database="dcc_a4"
        )
        return db_connection
    except pymysql.Error as err:
        print("Error connecting to the database:", err)
        return None

# Execute SQL query based on user input
def execute_query(db_connection, query):
    try:
        cursor = db_connection.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except pymysql.Error as err:
        print("Error executing query:", err)
        return None

@app.route('/', methods=["POST", "GET"])
def main_page():
    return render_template("index.html")

@app.route('/search', methods=['GET'])
def search():
    # Retrieve query parameters from the request
    query = request.args.get('query')
    column = request.args.get('column')
    
    # Connect to the database
    db_connection = connect_to_database()
    if not db_connection:
        return jsonify({"error": "Error connecting to the database"})

    # Execute database search based on the query and column
    search_results_1 = execute_query(db_connection, f"SELECT * FROM csv1 WHERE {column.replace('_',' ')} LIKE '%{query}%'")
    search_results_2 = execute_query(db_connection, f"SELECT * FROM csv2 WHERE {column.replace('_',' ')} LIKE '%{query}%'")
    
    # Close database connection
    db_connection.close()

    # Return search results as JSON
    return jsonify({"search_results_1": search_results_1, "search_results_2": search_results_2})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port="80", debug=True)

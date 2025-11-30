from flask import Flask, jsonify
from flask_cors import CORS
import mysql.connector, os

app = Flask(__name__)
CORS(app)  # <-- Das erlaubt standardmäßig alle Origins

@app.route("/")
def hello():
    return jsonify({"message": "Backend läuft"})

@app.route("/users")
def get_users():
    db = mysql.connector.connect(
        host=os.getenv("DB_HOST", "db"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", "pass"),
        database=os.getenv("DB_NAME", "demo")
    )
    cursor = db.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS users (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(50));")
    cursor.execute("INSERT INTO users (name) VALUES ('Alice'), ('Bob'), ('Charlie');")
    db.commit()
    cursor.execute("SELECT * FROM users;")
    result = cursor.fetchall()
    return jsonify(result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
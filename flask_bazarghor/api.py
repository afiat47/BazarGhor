from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

# MySQL (TiDB) config
config = {
    'host': 'gateway01.us-west-2.prod.aws.tidbcloud.com',
    'port': 4000,
    'user': 'axp3UvF4RX4GsfZ.root',
    'password': 'JTz0F0pimBqHFUoh',
    'database': 'bazarghor',
    'ssl_ca': 'isrgrootx1.pem'
}

def get_db():
    return mysql.connector.connect(**config)

# ------------------- CREATE USER -------------------
@app.route('/users', methods=['POST'])
def create_user():
    data = request.json
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    if not name or not email or not password:
        return jsonify({'error': 'Missing fields'}), 400

    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s)",
                       (name, email, password))
        db.commit()
        user_id = cursor.lastrowid
        return jsonify({'message': 'User created', 'user_id': user_id}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        db.close()

# ------------------- GET ALL USERS -------------------
@app.route('/users', methods=['GET'])
def get_users():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        return jsonify(users)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        db.close()

if __name__ == '__main__':
    app.run(debug=True)

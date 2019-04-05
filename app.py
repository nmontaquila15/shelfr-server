import pymysql
from flask import Flask, jsonify, request
from werkzeug.security import generate_password_hash
from flaskext.mysql import MySQL

mysql = MySQL()

app = Flask(__name__)
app.config["DEBUG"] = True

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'shelfr'
app.config['MYSQL_DATABASE_PASSWORD'] = 'shelfr'
app.config['MYSQL_DATABASE_DB'] = 'inventory'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)


@app.route('/add', methods=['POST'])
def add_item():
    try:
        json = request.json
        upc = json['upc']
        count = json['count']
        name = json['name']
        weight = json['weight']
        shelfid = json['shelfid']
        zone = json['zone']
        total_weight = json['totalweight']
        # validate the received values
        if upc and count and name and weight and shelfid and zone and total_weight and request.method == 'POST':
            # save edits
            sql = "INSERT INTO stock(upc, count, name, weight, shelfid, zone, totalweight) VALUES(%s, %s, %s, %s, %s, %s, %s)"
            data = (upc, count, name, weight, shelfid, zone, total_weight)
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sql, data)
            conn.commit()
            resp = jsonify('Item added successfully!')
            resp.status_code = 200
            return resp
        else:
            return not_found()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/items')
def items():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM stock")
        rows = cursor.fetchall()
        resp = jsonify(rows)
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/item/<name>', methods=['GET'])
def item(name):
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM stock WHERE name=%s", name)
        row = cursor.fetchone()
        resp = jsonify(row)
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/update/<name>', methods=['PUT'])
def update_item(name):
    try:
        json = request.json
        _name = name
        upc = json['upc']
        count = json['count']
        weight = json['weight']
        shelfid = json['shelfid']
        zone = json['zone']
        total_weight = json['totalweight']
        # validate the received values
        if _name and upc and count and weight and shelfid and zone and total_weight and request.method == 'PUT':
            # save edits
            conn = mysql.connect()
            cursor = conn.cursor()
            sql = "UPDATE stock SET upc=%s, count=%s, weight=%s, shelfid=%s, zone=%s, totalweight=%s WHERE name=%s"
            data = (upc, count, weight, shelfid, zone, total_weight, _name)
            cursor.execute(sql, data)
            conn.commit()
            resp = jsonify('User updated successfully!')
            resp.status_code = 200
            return resp
        else:
            return not_found()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/delete/<name>', methods=['DELETE'])
def delete_item(name):
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM stock WHERE name=%s", (name))
        conn.commit()
        resp = jsonify('User deleted successfully!')
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404

    return resp


if __name__ == "__main__":
    app.run('0.0.0.0', 5000)

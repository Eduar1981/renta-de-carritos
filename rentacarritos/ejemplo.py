from flask import Flask, render_template, request
from flaskext.mysql import MySQL
import hashlib

programa = Flask(__name__)
mysql = MySQL()
programa.config['MYSQL_DATABASE_HOST']='localhost'
programa.config['MYSQL_DATABASE_PORT']=3306
programa.config['MYSQL_DATABASE_USER']='root'
programa.config['MYSQL_DATABASE_PASSWORD']=''
programa.config['MYSQL_DATABASE_DB']='renta_carritos'
mysql.init_app(programa)

@programa.route('/')

def index():
    return render_template('/index22.html')

@programa.route('/index22', methods=['POST'])
def index22():
    nombre = request.form['nombre']
    clave = request.form['Contrasena']
    cifrada = hashlib.sha512(clave.encode("utf-8")).hexdigest()
    sql = f"INSERT INTO usuario (nombre, contrasena) VALUES ('{nombre}','{cifrada}')"
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    return 'Tu usuario esta creado'

if __name__=='__main__':
    programa.run(host='0.0.0.0', debug=True, port="5080")

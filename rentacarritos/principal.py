from flask import Flask, render_template, request, redirect
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
    return render_template('/index.html')

@programa.route("/login", methods=['POST'])
def login():
    nom = request.form['txtNom']
    contra = request.form['txtContra']
    cifrada = hashlib.sha512(contra.encode("utf-8")).hexdigest()
    sql=f"SELECT * FROM usuario WHERE nombre='{nom}' AND contrasena='{cifrada}'"
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql)
    resultado = cursor.fetchall()
    if(len(resultado)>0):
        if resultado is not None:
            return render_template("/principal.html")
    return render_template('/index.html')

@programa.route("/carritos")
def carritos():
    sentencia = "SELECT * FROM carritos"
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sentencia)
    resultado = cursor.fetchall()
    conn.commit()
    return render_template('/carritos.html', car=resultado)

@programa.route("/agregacarrito")
def agregacarrito():
    return render_template('agregacar.html')

@programa.route("/guardacar", methods=['POST'])
def guardacar():
    pla = request.form['txtPlaca']
    tip = request.form['txtTipo']
    vHo = request.form['txtValHora']
    vSe = request.form['txtValSem']
    col = request.form['txtColor']
    mod = request.form['txtModelo']
    sql = f"INSERT INTO carritos (placa,tipo,valhora,valsemana,color,modelo,kilometraje,disponibilidad) VALUES ('{pla}',{tip},{vHo},{vSe},'Negro',{col},{mod},0,1)"
    print(sql)
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    return redirect('/carritos')

@programa.route("/editarcar/<pla>")
def editarcar(pla):
    sql=f"SELECT * FROM carritos WHERE placa='{pla}'"
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql)
    car = cursor.fetchall()
    conn.commit()
    return render_template('actualizacar.html',car=car[0])

@programa.route("/modificacar", methods=['POST'])
def modificacar():
    pla = request.form['txtPlaca']
    tip = request.form['txtTipo']
    vHo = request.form['txtValHora']
    vSe = request.form['txtValSem']
    col = request.form['txtColor']
    mod = request.form['txtModelo']
    sql=f"UPDATE carritos SET tipo={tip},valHora={vHo},valSemana={vSe},colo={col}modelo={mod} WHERE placa='{pla}'"
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    return redirect('/carritos')


@programa.route('/borracar/<pla>')
def borracar(pla):
    sql=f"UPDATE carritos SET BORRADO=1 WHERE placa='{pla}'"
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    return redirect('/carritos')

if __name__ == '__main__':
    programa.run(host='0.0.0.0', debug=True, port="5080")


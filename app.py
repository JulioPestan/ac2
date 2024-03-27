

import os
from flask import Flask, render_template, json, request,jsonify, redirect, url_for
from flaskext.mysql import MySQL

mysql = MySQL()
app = Flask(__name__)

app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'impacta2024'
app.config['MYSQL_DATABASE_DB'] = 'teste'
app.config['MYSQL_DATABASE_HOST'] = 'db'

mysql.init_app(app)

@app.route('/')
def main():
     return render_template('home.html')

@app.route('/registre')
def registre():
    return render_template('registrar.html')


@app.route('/registrar', methods =['GET','POST'])
def registrar():

    print(request.form['inputusername'])
    try:
        if request.method == 'POST':
            nome = request.form['inputusername']
            telefone = request.form['inputtelefone']
            endereco = request.form['inputendereco']

            print(endereco)

            cur = mysql.connect().cursor()
            cur.execute('insert into tbl_registro (name, telefone,endereco ) values (%s, %s, %s)', (nome, telefone, endereco))
            mysql.connect().commit()
            print("oi")
            cur.close()

            

            msg = 'Registro feito com sucesso !!'
            return render_template('registrar.html', mensagem = msg)
    except Exception as e:
        return json.dumps({'error':str(e)})
    

@app.route('/list',methods=['POST','GET'])
def listar():
    try:
            
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute ('select * from tbl_registro') 
            data = cursor.fetchall()
            print(data[0])
            for x in range(len(data)):
                print(data[x])

            conn.commit()
            return render_template('signup2.html', datas=data)

    except Exception as e:
        return json.dumps({'error':str(e)})
    



if __name__=='__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
from flask import Flask,render_template, request
from datetime import datetime
import mysql.connector
app = Flask(__name__)

@app.route("/")
def home():
    
    return render_template("home.html")
    
    



@app.route("/mensagem", methods=["POST"])
def mensagem():
    numero =  str(request.form.get('telefone'))
    nome = request.form.get('nome')
    data = str(request.form.get('data'))
    horario =  request.form.get('horario')
    horarioreal = datetime.strptime(horario,'%H:%M').strftime('%H:%M:%S')
    connector = mysql.connector.connect(database='cadastro', host='localhost', user='root', password='')
    cursor =  connector.cursor()

    if connector.is_connected:
        cursor.execute('SELECT * FROM cadastrados')
        analiseTabela = cursor.fetchall()
        pessoascadastradas=[]
        horarioscadastrados=[]
        diasagendados = []

        for dado in analiseTabela:
            nomepessoa = dado[2]
            dataagendada= dado[3]
            horariopessoa =  dado[4]
            pessoascadastradas.append(nomepessoa)
            horarioscadastrados.append(str(horariopessoa))
            diasagendados.append(str(dataagendada))
        if nome in pessoascadastradas:
            return render_template("error.html")
        

        elif data in diasagendados:
            if horarioreal in horarioscadastrados:
                return render_template("error.html")
        else:
            print(data, diasagendados,horarioreal, horarioscadastrados)
            cursor.execute(f"INSERT INTO cadastrados (id, numero, nome, dia, horario) VALUES (id ,'{numero}' , '{nome}' , '{data}'  , '{horarioreal}' );")
            return render_template("mensagem.html",nome=nome,data=data,horario=horario)
    
    if connector.is_connected:
        cursor.close()
        connector.close()
    

app.run(debug=True)
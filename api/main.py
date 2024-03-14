from flask import Flask,render_template, request, redirect,flash
from datetime import datetime
import mysql.connector
app = Flask(__name__)
app.config['SECRET_KEY'] = "deus-é-maior"
@app.route("/")
def home():
    
    return render_template("home.html")
    
    



@app.route("/mensagem", methods=["POST"])
def mensagem():
    # RECEBENDO INFORMAÇÕES DO FORMULÁRIO
    numero =  str(request.form.get('telefone'))
    nome = request.form.get('nome')
    data = request.form.get('data')
    dataformatada = datetime.strptime(f'{data}', "%Y-%m-%d").strftime("%d-%m-%y")
    horario =  request.form.get('horario')
    horarioreal = datetime.strptime(horario,'%H:%M').strftime('%H:%M:%S')
    datahorario = str(f'{data} '+horarioreal)
    # CONEXÃO COM BANCO DE DADOS MYSQL:
    connector = mysql.connector.connect(database='railway',
                                        host='viaduct.proxy.rlwy.net', 
                                        user='root', 
                                        password='cXFrDAMVhHtcoZNynUiVsFDmNtWNfghC',
                                        port = '51229')
    cursor =  connector.cursor()


    if connector.is_connected:
        cursor.execute('SELECT * FROM cadastrados')
        analiseTabela = cursor.fetchall()
        pessoascadastradas=[]
        horarioscadastrados=[]

        for dado in analiseTabela:
            nomepessoa = dado[2]
            dataagendada= dado[3]
            pessoascadastradas.append(nomepessoa)
            horarioscadastrados.append(str(dataagendada))
        if nome in pessoascadastradas:
            flash('PESSOA JÁ AGENDADA')
            return redirect('/')
        
        elif datahorario in horarioscadastrados:
            flash("HORÁRIO OCUPADO")
            return redirect("/")
        
        else:
            cursor.execute(f"INSERT INTO cadastrados (id, numero, nome, dia ) VALUES (id ,'{numero}' , '{nome}' , '{datahorario}' );")
            flash("AGENDADO COM SUCESSO!")
            return redirect('/')
    
    if connector.is_connected:
        cursor.close()
        connector.close()
    

if __name__ == "__main__":
    app.run()
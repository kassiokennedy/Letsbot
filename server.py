import requests
import json
import pymongo
import time
from flask import Flask, request

app = Flask("letsbot-api-py")
# app = Flask(__name__)


@app.route("/", methods=["GET"])
def Hello():
    data = {"msg": "To vivo"}
    print("To vivo!")
    return data 




@app.route("/school_guardian", methods=["POST"])
def school_guardian():
    request_data = request.get_json()
    print(request_data)

    action = request_data['queryResult']['action']
    parameters = request_data['queryResult']['parameters']

    print(action)

    if action == "consultar_alunos_escola":
        alunos = consultarAlunosNaEscola()
        msg = []
        for x in alunos:
           msg.append({
                    "type": "info",
                    "title": x['nome'],
                    })

        resposta = {
            "fulfillmentMessages": [
                {
                    "payload": {
                        "richContent": [
                                msg
                        ]
                    }
                }
            ]
        }



    elif action == "consultar_carros":
        carros = consultarCarros()
        msg = []
        for x in carros:
            msg.append({
                    "type": "info",
                    "title": x['modelo'] + " - " + x['marca'],
                    "subtitle": "Placa: "+ x['placa'] + ", Cor: " + x['cor']
                }),  
    
        resposta = {
            "fulfillmentMessages": [
                {
                    "payload": {
                        "richContent": [
                                msg
                        ]
                    }
                }
            ]
        }

    
    elif action == "consultar_responsaveis":
        responsaveis = consultarResponsaveis()
        msg = []
        for x in responsaveis:
             msg.append({
                    "type": "info",
                    "title": x['nome'],
                    "subtitle": x['parentesco']
                }), 
        
        resposta = {
            "fulfillmentMessages": [
                {
                    "payload": {
                        "richContent": [
                       
                                msg
                        ]
                    }
                }
            ]
        }

    
    elif action == "consultar_tipo_busca_aluno":
        msg = consultarTipoBuscaAluno(parameters)

        resposta = { 
            "fulfillmentText": msg,
            "displayText" : msg,
            "speech" :  msg
        }

    elif action == "consultar_horario_retirada":
        msg = consultarHorarioRetirada(parameters)

        resposta = { 
            "fulfillmentText": msg,
            "displayText" : msg,
            "speech" :  msg
        }

    elif action == "consultar_ultima_pessoa_buscar_aluno":
        msg = consultarUltimaPessoaBuscarAluno(parameters)
        resposta = { 
            "fulfillmentText": msg,
            "displayText" : msg,
            "speech" :  msg
        }
    elif action == "consultar_portao_saida_aluno":
        msg = consultarPortaoSaidaAluno(parameters)
        resposta = { 
            "fulfillmentText": msg,
            "displayText" : msg,
            "speech" :  msg
        }
        
    return resposta
    



   


# ---------------- functions ----------------
#1 - Qual filho está na escola hoje
def consultarAlunosNaEscola():
    try:
        alunos = DBconsultarAlunosNaEscola()
    except Exception as e:  
        print(e)
    
   # msg = ''
   # for x in alunos:
   #     msg = msg + x['nome'] + ", "
    print('Vai imprimir alunos')
    print(alunos)

    return alunos


def consultarCarros():
    try:
        carros = DBconsultarCarros()
    except Exception as e:  
        print(e)
    
    return carros


def consultarResponsaveis():
    try:
        responsaveis = DBconsultarResponsaveis()
    except Exception as e:  
        print(e)
    
   
    return responsaveis


def consultarTipoBuscaAluno(parameters):
    tipo_busca = parameters["tipo_chamada"].lower()

    print(tipo_busca)

    msg = ''
    if "direta" in tipo_busca:
        msg = "Uma busca direta é quando você esta próximo a escola, e faz uma busca imediada do seu filho."
    elif "agendada" in tipo_busca:
        msg = "Uma busca agendada é quando você tem um horário planejado para buscar seu filho estando em casa ou no trabalho."
    elif "emergencia" in tipo_busca:
        msg = "Este caso é quando algum imprevisto possa ter acontecido e você precisa buscar seu filho imediatamente e sem planejamento." 

    print(msg)
    
    return msg


def consultarHorarioRetirada(parameters):
    periodo = parameters["periodo"].lower()

    msg = ''
    if "meio" in periodo:
        msg = "O horário de retirada do meio período é até as 14h00"
    elif "integral" in periodo:
        msg = "O horário de retirada do período integral é até as 19h00"
     

    print(msg)
    
    return msg




def consultarUltimaPessoaBuscarAluno(parameters):
    aluno = parameters["aluno"]['name'].lower() 

    try:
        alunoDB = DBconsultarUltimaPessoaBuscarAluno(aluno)
    except Exception as e:  
        print(e)
    

    msg = ''
    if alunoDB:
       msg = "A ultima pessoa a pegar " + alunoDB['nome'] + " foi " + alunoDB['ultima_busca']  
    else:
       msg = "Você não tem este filho cadastrado" 

    print(msg)
    
    return msg

def consultarPortaoSaidaAluno(parameters):
    aluno = parameters["aluno"]['name'].lower() 

    try:
        alunoDB = DBconsultarUltimaPessoaBuscarAluno(aluno)
    except Exception as e:  
        print(e)

    msg = ''
    if alunoDB:
       msg = "A saída de " + alunoDB['nome'] + " sempre acontece pelo portão " + alunoDB['portao'] + ". Dirija-se para lá ao chegar na escola."  
    else:
       msg = "Você não tem este filho cadastrado" 

    print(msg)
    
    return msg 


# ---------------- DB ----------------
def DBconsultarAlunosNaEscola():
    myclient = pymongo.MongoClient("mongodb+srv://botcamp:botcamp@cluster0-hgsso.mongodb.net/test?retryWrites=true&w=majority")
    mydb = myclient["schoolguardian"]
    mycol = mydb["alunos"] 

    data = mycol.find({'na_escola': True})

    return data


def DBconsultarCarros():
    myclient = pymongo.MongoClient("mongodb+srv://botcamp:botcamp@cluster0-hgsso.mongodb.net/test?retryWrites=true&w=majority")
    mydb = myclient["schoolguardian"]
    mycol = mydb["carros"] 

    data = mycol.find()

    return data  


def DBconsultarResponsaveis():
    myclient = pymongo.MongoClient("mongodb+srv://botcamp:botcamp@cluster0-hgsso.mongodb.net/test?retryWrites=true&w=majority")
    mydb = myclient["schoolguardian"]
    mycol = mydb["responsaveis"] 

    data = mycol.find()

    return data  

def DBconsultarUltimaPessoaBuscarAluno(aluno):
    myclient = pymongo.MongoClient("mongodb+srv://botcamp:botcamp@cluster0-hgsso.mongodb.net/test?retryWrites=true&w=majority")
    mydb = myclient["schoolguardian"]
    mycol = mydb["alunos"] 

    data = mycol.find_one({'nome': { "$regex": aluno,"$options" : "i"}})

    return data

if __name__ == "__main__":
    app.run()

#app.run(debug=True, host="0.0.0.0", port=80)--------------- functions ----------------
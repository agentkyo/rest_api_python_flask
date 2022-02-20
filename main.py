import json
from flask import Flask, request, render_template
import requests

app = Flask('cpf')

def responses(cpf,path):

  responses = {
    "bad_request":{"cpf": cpf,"message": "Bad Request - Invalid Characters","status_code": 400},
    "missing_information":{"cpf": cpf,"message": "Bad Request - CPF minimum numbers is 11","status_code": 400},
    "success_valid":{"cpf": cpf,"message": "This CPF is VALID!","status_code":200},
    "success_invalid":{"cpf": cpf,"message": "This CPF is NOT VALID!","status_code":200}
    }

  return responses[path], responses[path]["status_code"]

@app.route('/', methods=["GET"])
def home():
  return render_template('index.html')




@app.route('/validade/<cpf>', methods=["GET"])
def duedatedelete(cpf):
  target = str(cpf).replace('.', '').replace('-', '').replace(' ', '').strip()
  if target.isdigit() == False:
    print("[Error] - Digite apenas numeros! [Fail]")
    return responses(cpf,"bad_request")
  else:
    if len(target) != 11:
      print(f'[Result] - O cpf {target} não possui 11 digitos, logo é um CPF invalido. [Fail]')
      return responses(cpf,"missing_information")
    else:
      y = [10, 9, 8, 7, 6, 5, 4, 3, 2]
      validacao_digito1 = []
      i = 0
      for digito in range(0, 9):
          validacao_digito1.append(int(target[digito]) * y[i])
          i += 1
      d1 = sum(validacao_digito1)
      validador_do_digito1 = 11 - (d1 % 11)
      if validador_do_digito1 > 9:
          validador_do_digito1 = 0
      if validador_do_digito1 != int(target[9]):
        print(f'[Result] - O CPF {target} informado não é valido. [Fail]')
        return responses(cpf,"success_invalid")
      else:
        w = [11, 10, 9, 8, 7, 6, 5, 4, 3]
        validacao_digito2 = []
        i = 0
        for digito in range(0, 9):
            validacao_digito2.append(int(target[digito]) * w[i])
            i += 1
        validacao_digito2.append(validador_do_digito1*2)
        d2 = sum(validacao_digito2)
        validador_do_digito2 = 11 - (d2 % 11)
        if validador_do_digito2 > 9:
            validador_do_digito2 = 0
        if validador_do_digito2 != int(target[10]):
            print(f'[Result] - O CPF {target} informado não é valido. [Fail]')
            return responses(cpf,"success_invalid")
        else:
            print(
                f'[Result] - O CPF {target} informado é um CPF válido! - [Success]')
            return responses(cpf,"success_valid")

app.run(host='0.0.0.0', port=8080)

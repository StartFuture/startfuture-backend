from flask_restful import Resource, reqparse


class Certificate(Resource):
    
    def get(self):
        global cod 
        from random import randint
        cod = randint(111111, 9999999)
        
        function.send_email(session['email_user'], cod)
        
        print(session['email_user'])
        
        return{
            'verification_code': cod
        }     
    
    def post(self):  
        
        argumentos = reqparse.RequestParser()
        
        argumentos.add_argument('nome')
        argumentos.add_argument('sobrenome')
        argumentos.add_argument('data_aniversario')
        argumentos.add_argument('sexo')
        argumentos.add_argument('telefone')
        argumentos.add_argument('email')
        argumentos.add_argument('senha')
        
        dados = argumentos.parse_args()
        
        if dao.DataBaseUser.verify_user_exist(dados['email'], dados['telefone']):
        
            return {
                'msg': 'User alredy exist'
            }, 400
        
        else:
            user = User(dados['nome'], dados['sobrenome'], 
                        dados['data_aniversario'],dados['sexo'] ,dados['telefone'], 
                        dados['email'], generate_password_hash(dados['senha']),
                        dados['cpf_cnpj'])
            
            create = dao.DataBaseUser.save_user(
                name=user.name,
                last_name=user.lastname,
                email=user.email,
                cellphone=user.phone,
                birthdate=user.birthday,
                password=user.password,
                identity=user.identity,
                sex=user.sex,
            )
            
            
            if create:
                return {'msg': 'User create'}, 200
            else:
                return {'msg': 'Db Problem'}, 400
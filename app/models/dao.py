import psycopg2
import app.utils as Function
import logging
import os
import re
from app.parameters import DB_PG_NAME, DB_PG_PASSWORD, DB_PG_NAME_DB, DB_PG_HOST 

class DataBase:
    
    def __init__(self, user, password, host, database):
        self.user = user
        self.password = password
        self.host = host
        self.database = database
        
    def __enter__(self):
        try:
            self.db = psycopg2.connect(user=self.user,
                                        password=self.password,
                                        host=self.host,
                                        port=self.port,
                                        database=self.database)
            self.cursor = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
        except Exception as erro:
            print(erro)
        else:
            return self.cursor

    def __exit__(self, *args):
        try:
            self.db.commit()
            self.db.close()
        except Exception as erro:
            print(erro)
            
class DataBaseUser:               
            
    def verify_user_exist(email, telefone):
        with DataBase(DB_PG_NAME, DB_PG_PASSWORD, DB_PG_HOST, DB_PG_NAME_DB) as cursor:
            if cursor:
                query_search = f"""
                SELECT email, telefone
                FROM user
                LEFT JOIN info_user_cpf
                ON user.id = info_user_cpf.id
                where cpf = '{cpf}' or email = '{email}' or telefone = '{telefone}';  
                """
                cursor.execute(query_search)
                if cursor.fetchone():
                    return True
                return False
    
    
    def get_user_id_by_email(email):
        with DataBase(DB_PG_NAME, DB_PG_PASSWORD, DB_PG_HOST, DB_PG_NAME_DB) as cursor:
            if cursor:
                query = f"""
                               select id from user where email = '{email}';
                               """
                
                cursor.execute(query)
                
                value = cursor.fetchone()

                if value:
                    
                    value = value['id']
                else:
                    value = None
                    
                return value

    def save_user_infos(name, last_name, email, cellphone, birthdate, sex, password):
        with DataBase(DB_PG_NAME, DB_PG_PASSWORD, DB_PG_HOST, DB_PG_NAME_DB) as cursor:
            if cursor:
                query_user = f"""
                insert into user
                values 
                (default,'{name}', '{last_name}', '{sex}','{birthdate}', '{cellphone}','{email}', '{password}');
                """
                try:
                    cursor.execute(query_user)
                except Exception as erro:
                    logging.error(erro)
    
    def save_user_identification(id, identity):
        with DataBase(DB_PG_NAME, DB_PG_PASSWORD, DB_PG_HOST, DB_PG_NAME_DB) as cursor:
            if len(identity) == 11 or re.match(r"^\d{3}\.\d{3}\.\d{3}-\d{2}$", identity):
                query_identity = f"""
                insert into info_user_cpf(cpf, id)
                values
                ('{identity}', '{id}')
                """
            elif len(identity) == 14 or re.match(r"^\d{2}\.\d{3}\.\d{3}\/\d{4}\-\d{2}$", identity):
                query_identity = f"""
                insert into info_user_cnpj(cnpj, id)
                values
                ('{identity}', '{id}')
                """
                print('cnpj')
                
            else:
                raise Exception('error in identity')
            
            cursor.execute(query_identity)
                


    def save_user(name, last_name, email, cellphone, birthdate, password, identity, sex):
        # Save Basic infos
        try:
            DataBaseUser.save_user_infos(name, last_name, email, cellphone, birthdate, sex, password)
        except Exception as erro:
            return False
        else:
            # Get id
            id = DataBaseUser.get_user_id_by_email(email)
            print(id)
            # Save identification
            DataBaseUser.save_user_identification(id, identity)
            return True

    def search_pj(cnpj, email):
        with DataBase(DB_PG_NAME, DB_PG_PASSWORD, DB_PG_HOST, DB_PG_NAME_DB) as cursor:
            if cursor:
                query = f"""
                select * from user 
                where cpf = '{cnpj}' or email = '{email}';
                """
                cursor.execute(query)
                if cursor.fetchall():
                    return True
                return False


    def save_user_pj(name, sobrenome, telefone, email, cnpj, data_nasc, senha):
        with DataBase(DB_PG_NAME, DB_PG_PASSWORD, DB_PG_HOST, DB_PG_NAME_DB) as cursor:
            if cursor:
                query =f"""
                insert into user 
                values (default, '{name}','{sobrenome}',
                '{cnpj}', '{data_nasc}', '{telefone}',
                '{email}', '{senha}');
                """
                cursor.execute(query)
                


    def query_exist_email(email):
        with DataBase(DB_PG_NAME, DB_PG_PASSWORD, DB_PG_HOST, DB_PG_NAME_DB) as cursor:
            if cursor:
                query = f"""
                select * from user 
                where email = '{email}'
                """
                cursor.execute(query)
                if not (list_user := cursor.fetchall()):
                    return None, None
                for info in list_user:
                    password = info['senha']
                    name = info['email']
                    return password, name


    def query_exist_cpf(cpf):
        with DataBase(DB_PG_NAME, DB_PG_PASSWORD, DB_PG_HOST, DB_PG_NAME_DB) as cursor:
            if cursor:
                query_ = f"""
                select * from info_user_cpf
                where cpf = '{cpf}'
                """
                cursor.execute(query)
                cpf = cursor.fetchall()
                if cpf:
                    for value in cpf:
                        id = value['id']

                    cursor.execute(f"""select * from user where id = '{id}' """)
                    values = cursor.fetchall()
                    for value in values:
                        senha = value['senha']
                        nome = value['nome']
                        email = value['email']
                    return senha, nome, email 

    def query_exist_cnpj(cnpj):
        with DataBase(DB_PG_NAME, DB_PG_PASSWORD, DB_PG_HOST, DB_PG_NAME_DB) as cursor:
            if cursor:
                cursor.execute(f"""select * from info_user_cnpj where cnpj = '{cnpj}'""")
                cnpj = cursor.fetchall()
                if cnpj:
                    for value in cnpj:
                        id = value['id']

                    cursor.execute(f"""select * from user where id = '{id}' """)
                    values = cursor.fetchall()
                    for value in values:
                        senha = value['senha']
                        nome = value['nome']
                        email = value['email']
                    return senha, nome, email

    def delete_user(id):
        with DataBase(DB_PG_NAME, DB_PG_PASSWORD, DB_PG_HOST, DB_PG_NAME_DB) as cursor:
            if cursor:
                cursor.execute(f"""
                delete from user where id = '{id}';               
                """)


    def update_user(id, new_name, new_lastname, new_cpf, new_birth_date, new_cell, new_email):
        with DataBase(DB_PG_NAME, DB_PG_PASSWORD, DB_PG_HOST, DB_PG_NAME_DB) as cursor:
            if cursor:
                cursor.execute(f"""
                update user set nome = '{new_name}', sobrenome = '{new_lastname}', cpf = '{new_cpf}',
                data_nascimento = '{new_birth_date}', telefone = '{new_cell}', email = '{new_email}'
                where id = '{id}';        
                """)
            

    def new_password(id, newpassword):
        with DataBase(DB_PG_NAME, DB_PG_PASSWORD, DB_PG_HOST, DB_PG_NAME_DB) as cursor:
            if cursor:
                query = f"""
                update user 
                set senha = '{newpassword}' 
                where id = '{id}';
                """
                cursor.execute(query)

DataBaseUser.get_user_id_by_email('mateustoni04@gmail.com')

# select id from user where email = 'mateustoni04@gmail.com';
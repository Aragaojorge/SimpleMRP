import psycopg2

class AppBD:
    def __init__(self):
        print('Constructor method')
        print('Connecting...')
        
    def abrirConexao(self):
        try:
            self.connection = psycopg2.connect(database="postgres", user="postgres", password="123psql", host="127.0.0.1", port="5432")
        except(Exception, psycopg2.Error) as error:
            if(self.connection):
                print('Failed to connect to the Database!')
                
    def selecionarDados(self):
        try:
            self.abrirConexao()
            cursor = self.connection.cursor()
            
            print('Selecting all products')
            sql_select_query = """select * from public."PRODUTO" """
            
            cursor.execute(sql_select_query)
            registros = cursor.fetchall()
            print(registros)
            
        except(Exception, psycopg2.Error) as error:
            print('Error when selecting: ', error)
            
        finally:
            if(self.connection):
                cursor.close()
                self.connection.close()
                print('Connection to PostgreSQL has been closed.')
                
        return registros
    
    def inserirDados(self, codigo, nome, preco):
        try:
            self.abrirConexao()
            cursor = self.connection.cursor()            
            sql_insert_query = """INSERT INTO public."PRODUTO" ("CODIGO", "NOME", "PRECO") VALUES (%s, %s, %s)"""
            record_to_insert = (codigo, nome, preco)
            cursor.execute(sql_insert_query, record_to_insert)
            self.connection.commit()
            count = cursor.rowcount
            print(count, ' - Registration entered successfully!')
            
        except(Exception, psycopg2.Error) as error:
            print('Failed to insert data into the PRODUCT table', error)
            
        finally:
            if(self.connection):
                cursor.close()
                self.connection.close()
                print('Connection to PostgreSQL has been closed.')     
                
    def atualizarDados(self, codigo, nome, preco):
        try:
            self.abrirConexao()
            cursor = self.connection.cursor()  
                      
            # registro antes da atualização
            sql_select_query = """select * from public."PRODUTO" where "CODIGO" = %s """
            cursor.execute(sql_select_query, (codigo,))
            record= cursor.fetchone()
            print(record)
            
            # atualizar registro
            sql_update_query = """Update public."PRODUTO" set "NOME" = %s,
            "PRECO" = %s where "CODIGO" = %s """
            cursor.execute(sql_update_query, (nome, preco, codigo))
            self.connection.commit()
            count = cursor.rowcount
            print(count, ' - Record(s) updated successfully!')
            print('Registration after update: ')
            sql_select_query = """select * from public."PRODUTO" where "CODIGO" = %s """
            cursor.execute(sql_select_query, (codigo,))
            record= cursor.fetchone()
            print(record)
            
            
        except(Exception, psycopg2.Error) as error:
            print('Error when updating!', error)
            
        finally:
            if(self.connection):
                cursor.close()
                self.connection.close()
                print('Connection to PostgreSQL has been closed.')   
                
    def excluirDados(self, codigo):
        try:
            self.abrirConexao()
            cursor = self.connection.cursor()
            
            # atualizar registro
            sql_delete_query = """Delete from public."PRODUTO"
            where "CODIGO" = %s"""
            cursor.execute(sql_delete_query, (codigo, ))
            self.connection.commit()
            count = cursor.rowcount
            print(count, '- Record deleted successfully!')
            
        except(Exception, psycopg2.Error) as error:
            print('Error deleting: ', error)
            
        finally:
            if(self.connection):
                cursor.close()
                self.connection.close()
                print('Connection to PostgreSQL has been closed.')
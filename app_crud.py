import tkinter as tk
from tkinter import ttk
import crud as crud

class PrincipalBD:
    def __init__(self, win):
        self.objBD = crud.AppBD()
            
        # componentes
        self.lbCodigo = tk.Label(win, text='Code: ')
        self.lblName = tk.Label(win, text='Product: ')
        self.lblPreco = tk.Label(win, text='Price:')
        
        self.txtCodigo=tk.Entry(bd=3)
        self.txtName=tk.Entry()
        self.txtPreco=tk.Entry()
        
        self.btnCadastrar = tk.Button(win, text='Register', command=self.fCadastrarProduto)
        self.btnAtualizar = tk.Button(win, text='Update', command=self.fAtualizarProduto)
        self.btnExcluir = tk.Button(win, text='Delete', command=self.fExcluirProduto)
        self.btnLimpar = tk.Button(win, text='Clear', command=self.fLimparTela)
        
        self.dadosColunas = ("Code", "Name", "Price")
        
        self.treeProdutos = ttk.Treeview(win, columns=self.dadosColunas, selectmode='browse')
        
        self.verscrlbar = ttk.Scrollbar(win, orient='vertical', command=self.treeProdutos.yview)
        
        self.verscrlbar.pack(side='right', fill='x')
        
        self.treeProdutos.configure(yscrollcommand=self.verscrlbar.set)
        
        self.treeProdutos.heading("Code", text='Code')
        self.treeProdutos.heading("Name", text='Name')
        self.treeProdutos.heading("Price", text='Price')

        self.treeProdutos.column("Code", minwidth=0, width=100)
        self.treeProdutos.column("Name", minwidth=0, width=100)
        self.treeProdutos.column("Price", minwidth=0, width=100)
        
        self.treeProdutos.pack(padx=10, pady=10)
        self.treeProdutos.bind("<<TreeviewSelect>>", self.apresentarRegistrosSelecionados)
        
        self.lbCodigo.place(x=100, y=50)
        self.txtCodigo.place(x=250, y=50)
        
        self.lblName.place(x=100, y=100)
        self.txtName.place(x=250, y=100)
        
        self.lblPreco.place(x=100, y=150)
        self.txtPreco.place(x=250, y=150)
        
        self.btnCadastrar.place(x=100, y=200)
        self.btnAtualizar.place(x=200, y=200)
        self.btnExcluir.place(x=300, y=200)
        self.btnLimpar.place(x=400, y=200)
        
        self.treeProdutos.place(x=100, y=300)
        self.verscrlbar.place(x=850, y=300, height=225)
        self.carregarDadosIniciais()
        
    def apresentarRegistrosSelecionados(self, event):
        self.fLimparTela()
        for selection in self.treeProdutos.selection():
            item = self.treeProdutos.item(selection)
            codigo, nome, preco = item['values'][0:3]
            self.txtCodigo.insert(0, codigo)
            self.txtName.insert(0, nome)
            self.txtPreco.insert(0, preco)
            
    def carregarDadosIniciais(self):
        try:
            self.id = 0
            self.iid = 0
            
            registros = self.objBD.selecionarDados()
            print('------------------ Data available in the BD ------------------')
            
            for item in registros:
                codigo =item[0]
                nome = item[1]
                preco = item[2]
                print('Code = ', codigo)
                print('Name = ', nome)
                print('Price = ', preco, '\n')
                
                self.treeProdutos.insert('', 'end', iid=self.iid, values=(codigo, nome, preco))
                self.iid = self.iid + 1
                self.id = self.id + 1
                
            print('Base Data')
        
        except:
            print('There is no data to load yet!') 
            
    def fLerCampos(self):
        try:
            print('******************** Data available ********************')
            codigo = int(self.txtCodigo.get())
            print('codigo', codigo)
            nome = self.txtName.get()
            print('Name', nome)
            preco = float(self.txtPreco.get())
            print('preco', preco)
            print('Data reading done successfully!')
        except:
            print('Unable to read data!')
        return codigo, nome, preco
    
    def fCadastrarProduto(self):
        try:
            print('******************** Data available ********************')
            codigo, nome, preco = self.fLerCampos()
            self.objBD.inserirDados(codigo, nome, preco)
            self.treeProdutos.insert('', 'end', iid=self.iid, values=(codigo, nome, preco))
            
            self.iid = self.iid + 1
            self.id = self.id + 1
            self.fLimparTela()
            print('Product registered successfully!')
        except:
            print('Unable to register!')
            
    def fAtualizarProduto(self):
        try:
            print('******************** Data available ********************')
            codigo, nome, preco = self.fLerCampos()
            self.objBD.atualizarDados(codigo, nome, preco)
            
            # recarregar dados na tela
            self.treeProdutos.delete(*self.treeProdutos.get_children())
            self.carregarDadosIniciais()
            self.fLimparTela()
            print('Product updated successfully!')
        except:
            print('Unable to update!')
            
            
    def fExcluirProduto(self):
        try:
            print('******************** Data available ********************')
            codigo, nome, preco = self.fLerCampos()
            self.objBD.excluirDados(codigo)
            
            # recarregar dados na tela
            self.treeProdutos.delete(*self.treeProdutos.get_children())
            self.carregarDadosIniciais()
            self.fLimparTela()
            print('Product deleted successfully!')
        except:
            print('Unable to delete product!')
            
    def fLimparTela(self):
        try:
            print('******************** Data available ********************')
            self.txtCodigo.delete(0, tk.END)
            self.txtName.delete(0, tk.END)
            self.txtPreco.delete(0, tk.END)
            print('Fields cleaned!')
        except:
            print('Unable to clear the fields!')

# main porgram 
janela = tk.Tk()
principal = PrincipalBD(janela)
janela.title('Welcome to the Database application')
janela.geometry('820x600+10+10')
janela.mainloop()
import csv
import random
import os

def porcento(num):
    num = f'{num:.2f}'
    return num + '%'

def pular():
    os.system('pause')
    os.system('cls')

class ExtratorDeProbabilidades:
    def __init__(self, arquivo):
        self.banco = arquivo
        self.lista = []
    
    def validar(self):
        try:
            file = open(self.banco)
            file.close()
            return True
        except FileNotFoundError:
            print(f'Arquivo "{self.banco}" não encontrado. Tente novamente.')
            return False
            
    def registros(self, n=0):
        if not self.lista:
            print('Banco de Dados não carregado!')
        
        if not n:
            for row in self.lista:
                for key, value in row.items():
                    print(f"{key}: {value}")
                print()
        elif n > len(self.lista) or n < 0:
            print("Número inválido.")
        else:
            for i in range(n):
                for key, value in self.lista[i].items():
                    print(f"{key}: {value}")
                print()
    
    def carregar_colunas(self, lista_colunas, quantidade):
        counter1 = 0
        counter2 = 0
        lista_base = []
        
        with open(self.banco, encoding = 'cp850') as file:
            dit = csv.DictReader(file)
            for row in dit: counter1 += 1
        
        indexes = [random.randint(0, counter1) for i in range(quantidade)]
            
        with open(self.banco, encoding = 'cp850') as file:
            dit = csv.DictReader(file)
            
            for row in dit:
                counter2 += 1
                if counter2 in indexes: lista_base.append(row)
            
            tmp_dict = {}
            lista_def = []
            erros = [coluna for coluna in lista_colunas if coluna not in dit.fieldnames]
            
            for row in lista_base:
                for key, value in row.items():
                    if key in lista_colunas:
                        tmp_dict[key] = value
                lista_def.append(tmp_dict.copy())
            
            self.lista = lista_def
                
            if erros:
                print("Colunas indisponíveis no banco de dados: ", end="")
                for erro in erros:
                    print(f"'{erro}' ", end="")
                print("")
                print("O banco de dados foi carregado sem elas.\n")
            elif len(erros) == len(lista_colunas):
                print("Nenhuma coluna válida na entrada. Tente novamente.")
            else:
                print("Colunas carregadas com sucesso a partir do banco de dados.\n")
    
    def descarregar(self):
        self.lista.clear()
        print('Banco de Dados descarregado com Sucesso!') 
    
    def probabilidade_apriori(self, caracteristica, valor):  
        count = 0
        
        for linha in self.lista:
            if linha[caracteristica] == valor: count += 1
        
        if len(self.lista) == 0: return porcento(0)
        
        count *= 100 
        count /= len(self.lista)
        
        return porcento(count)
    
    def probabilidade_apriori_intervalo(self, caracteristica, inicio, fim):
        count = 0
        
        for linha in self.lista:
            valor = int(linha[caracteristica])
            if valor > inicio and valor < fim: count += 1
        
        if len(self.lista) == 0: return porcento(0)
        
        count *= 100 
        count /= len(self.lista)
        
        return porcento(count)
    
    def probabilidade_condicional(self, car1, valor1, car2, valor2):
        count1 = 0
        count2 = 0
        
        for linha in self.lista:
            if linha[car2] == valor2:
                count2 += 1
                if linha[car1] == valor1: count1 += 1
        if count2 == 0: return porcento(0)
        
        count1 *= 100 
        count1 /= count2
        
        return porcento(count1)
    
    def probabilidade_condicional_intervalo(self, car1, valor1, car2, inicio, fim):
        count1 = 0
        count2 = 0
        
        for linha in self.lista:
            if linha[car1] == valor1:
                count1 += 1
                valor2 = int(linha[car2])
                if valor2 > inicio and valor2 < fim: count2 += 1
        if count1 == 0: return porcento(0)
        
        count2 *= 100 
        count2 /= count1
        
        return porcento(count2)

    def substituir(self, novo_banco):
        self.descarregar()
        self.banco = novo_banco
        print("Nova base de dados inserida com sucesso!")     

while True:
    arquivo = input('Digite o nome do arquivo: ')
    classe = ExtratorDeProbabilidades(arquivo)
    if classe.validar(): break

while True:
    print('-=- ' * 6, 'MENU', ' -=-' * 6)
    print(' ')
    print(':    1. Carregar Colunas                              :')
    print(':    2. Descarregar Colunas                           :')
    print(':    3. Visualizar Registros                          :')
    print(':    4. Probabilidade a Priori                        :')
    print(':    5. Probabilidade a Priori com Intervalo          :')
    print(':    6. Probabilidade Condicional                     :')
    print(':    7. Probabilidade Condicional com Intervalo       :')
    print(':    8. Alterar base de dados                         :')
    print(':    9. Sair                                          :')
    print(" ")
    print('=', ' -=-' * 13)
    
    try:
        op = int(input('Digite uma Opção: ').strip())
        os.system("cls")
    except ValueError:
        print('A entrada deve ser um número. Tente Novamente!')
        pular()

    if op == 9: break
    
    if op == 1:
        
            qtd_colunas = int(input('Digite quantos registros você quer carregar: ').strip())
            n_colunas = input('Quais colunas você quer carregar? Divida por espaços!\n').strip().split(" ")
            classe.carregar_colunas(n_colunas, qtd_colunas)
            pular()
        
        
    elif op == 2:
        classe.descarregar()
        pular()
        
    elif op == 3:
        print('1. Visualizar todos os itens da lista')
        print('2. Visualizar uma quantidade específica')
        
        try:
            op_visu = int(input('Digite uma opção: '))
        except ValueError:
            print('A entrada deve ser um número. Tente Novamente!')
            pular()
            
        if op_visu == 1:
            classe.registros()
            pular()
        elif op_visu == 2:
            try:
                segun_op = int(input('Digite a quantidade desejada: ').strip())
            except ValueError:
                print('A entrada deve ser um número. Tente Novamente!')
                pular()
            classe.registros(segun_op)
            pular()
            
        else:
            print('Opção não encontrada!')
     
    elif op == 4:
        var_1 = input('Digite a característica de verificação: ').strip()
        var_2 = input('Digite o valor: ').strip()
        prob = classe.probabilidade_apriori(var_1, var_2)
        print('A Probabilidade a Priori é', prob)
        pular()
        
    elif op == 5:
        caractes = input('Digite a Característica desejada: ').strip()
        try:
            inicio = float(input('Digite o valor inicial: ').strip())
            final = float(input('Digite o valor final: ').strip())
            probI = classe.probabilidade_apriori_intervalo(caractes, inicio, final)
            print('A Probabilidade a Priori com Intervalo é', probI)
            pular()
        except ValueError:
            print('O início e final devem ser um número. Tente Novamente!')
            pular()
        
    elif op == 6:
        caracter1 = input('Digite a primeira característica: ').strip()
        valor1 = input('Digite o valor: ').strip()
        caracter2 = input('Digite a segunda característica: ').strip()
        valor2 = input('Digite o valor: ').strip()
        prob_C = classe.probabilidade_condicional(caracter1, valor1, caracter2, valor2)
        print('A Probabilidade Condicional é', prob_C)
        pular()
        
    elif op == 7:
        caracter_C = input('Digite a característica de Condição: ').strip()
        valor_C = input('Digite o valor da Condição: ').strip()
        caracter_C2 = input('Digite a característica do intervalo: ').strip()
        try:
            inicio_C = float(input('Digite o início do Intervalo: ').strip())
            final_C = float(input('Digite o final do Intervalo: ').strip())
            prob_I = classe.probabilidade_condicional_intervalo(caracter_C, valor_C, caracter_C2, inicio_C, final_C)
            print('A Probabilidade Condicional com Intervalo é', prob_I)
            pular()
        except ValueError:
            print('O início e final devem ser um número. Tente Novamente!')
            pular()
    elif op == 8:
        base = input("Digite o nome da nova base de dados: ")
        classe.substituir(base)
        classe.validar()
        pular()
    else:
        print("Opção não existente.")

print("Desenvolvido por Iury Mikael Sobral dos Santos e Nicoly Lana Lourenço Carvalho")
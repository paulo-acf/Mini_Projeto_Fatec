# Orientação para executar o programa: no terminal, digite --> python mini_projeto_2.py


# Os caracteres gráficos "Black Square" (■ ■ ■) foram   P R O P O S I T A L M E N T E   acrescentados como RECURSOS VISUAIS:
#    •Para salientar pontos/diferenças importantes;
#    •Para facilitar ♦a revisão e ♦os possíveis estudos futuros do código (por mim mesmo ou por outros).


from sqlalchemy import (
    # sqlalchemy:
    #    •Biblioteca do Python que permite trabalhar com banco de dados
    #    •Permite •conectar, •consultar, •inserir, •alterar e •apagar dados
    MetaData, # Objeto do sqlalchemy que guarda informações sobre as tabelas do banco de dados
    Table,
    Column,
    Integer, # Número inteiro
    String, # Texto
    Date, # Data --> YYYY-MM-DD
    DateTime, # Data e hora --> YYYY-MM-DD HH:MM:SS (■ ■ ■ USADO PARA   D E F I N I R   UMA COLUNA COMO DATA E HORA)
    # # # # # # #   insert, # Insere dados na tabela
    text # Permite usar linguagem SQL (DISU --> •Delete, •Insert, •Select, •Update)
)
from datetime import datetime # ■ ■ ■ USADO PARA   P R E E N C H E R   UMA COLUNA COM DATA E HORA
import time # Biblioteca que mede o tempo de execução do código
from functools import wraps # Wrap --> Envolver; embrulhar
# functools --> Módulo do Python que permite trabalhar com •decorators, •wraps •etc.
# Wraps --> Função do módulo functools que copia Metadados (W é M ao contrário):
#    •Ao usar um decorator, a função original é substituída por um wrapper...
#    •O problema --> Sem wraps, o wrapper perde os metadados da função original (nome etc.)...
#    •A solução --> O wraps resolve isso copiando esses metadados para o wrapper
import csv
from collections import defaultdict


def medir_tempo(func): # Decorator --> Função que modifica outra função
    @wraps(func) # Wrap --> Envolver; embrulhar (preserva os metadados da função original - no caso, LGPD)
    def wrapper_embrulhador(*args, **kwargs): # •args (vira uma tupla) <> •kwargs (vira um dicionário)
        inicio = time.perf_counter() # perf_counter --> Contador de alta performance (marca o início da execução)
        resultado = func(*args, **kwargs)
        # •Executa "func" (LGPD), •passando todos os argumentos recebidos pelo wrapper e •guarda o retorno em "resultado"
        fim = time.perf_counter() # perf_counter --> Contador de alta performance (marca o final da execução)
        duracao = fim - inicio # Calcula o tempo de execução


        with open("log.txt", "a", encoding="utf-8") as log:
        # with open --> Abre o arquivo "log.txt"
        # "a" --> Append
        # encoding="utf-8" --> Permite uso de caracteres especiais
        # log = Variável
            log.write(f"{func.__name__} | {duracao:.6f} segundos\n")


        print(f"A função '{func.__name__}' foi executada em {duracao:.6f} segundos.") # Printa o tempo de execução
        return resultado
    return wrapper_embrulhador


from banco_de_dados import engine # Cria conexão com o PostgreSQL


metadata = MetaData() # Objeto usado para organizar tabelas


usuarios = Table(
    'usuarios', # Nome da tabela no banco
    metadata, # Permite controlar tabelas
    # ABAIXO (estrutura da tabela):
    # Column(•Nome da coluna,     •Tipo de dado,  •Atributo(s) da coluna)
    Column(  'id',                Integer,        primary_key=True),
    Column(  'nome',              String(50),     nullable=False, index=True), # Index --> Similar a um índice de livro
    Column(  'cpf',               String(14),     nullable=False),
    Column(  'email',             String(100),    nullable=False, unique=True), # Unique --> Não aceita valores repetidos
    Column(  'telefone',          String(20),     nullable=False),
    Column(  'data_nascimento',   Date,           nullable=False),
    Column(  'created_on',        DateTime(),     default=datetime.now),
    Column(  'updated_on',        DateTime(),     default=datetime.now, onupdate=datetime.now) #onupdate --> Atualiza data e hora
)


metadata.create_all(engine) # Cria a tabela caso esta não exista


@medir_tempo # --> Aplica decorator para medir o tempo de execução da função LGPD
def LGPD(row):
    # row --> Linha vinda do banco
    # Atualmente, apenas retorna os dados originais
    # Futuramente, será alterado para anonimização
    return row


usersss = [] # Lista para guardar os resultados da consulta SQL depois de passar pela função


with engine.connect() as conexao:
# with ... as conn --> Garante que, depois, a conexão será fechada automaticamente
# engine.connect() --> Cria uma conexão com o banco de dados


    result = conexao.execute(text('''                                           -- ■ ■ ■ Comando do Professor (PDF) --> "SELECT * FROM usuarios LIMIT 10;"
        SELECT
            LEFT(SPLIT_PART(nome, ' ', 1), 1)                                   -- Pega a primeira letra do primeiro nome
            || REPEAT('*', LENGTH(SPLIT_PART(nome, ' ', 1)) - 1)                -- || --> Concatenador  
            || CASE                                                             -- Similar ao IF
                WHEN POSITION(' ' IN nome) > 0
                THEN ' ' || SPLIT_PART(nome, ' ', 2)
                ELSE ''
            END AS nome,

            SUBSTRING(cpf FROM 1 FOR 3) || '.***.***-**' AS cpf,

            LEFT(SPLIT_PART(email, '@', 1), 1)
            || REPEAT('*', LENGTH(SPLIT_PART(email, '@', 1)) - 1)
            || '@'
            || SPLIT_PART(email, '@', 2) AS email,

            RIGHT(REGEXP_REPLACE(telefone, '[^0-9]', '', 'g'), 4) AS telefone
                                                                                -- telefone --> Coluna original
                                                                                -- '[^0-9]' --> Tudo que não for número (em regex - expressões regulares - o ^ significa "não")
                                                                                -- '' --> Substitui por vazio
                                                                                -- 'g' → Global (substitui todas as ocorrências)                               
        FROM usuarios
        LIMIT 10;                                                               -- QUANTIDADE DE REGISTROS RETORNADOS
    '''))


    for row in result: # Percorre os n registros encontrados na linha acima
        row = LGPD(row) 
        # LGPD(row) --> Chama a função LGPD, passando row como argumento
        # row = ... --> O valor retornado pela função substitui o row original
        # adiciona resultado na lista
        usersss.append(row) # Adiciona o resultado na lista "users"


for user in usersss:
    print(user)


@medir_tempo
def tempo_da_atividade_2_csv_por_ano():


    dados_por_ano = defaultdict(list) # Dicionário de listas (se a chave não existir, cria uma lista automaticamente)


    with engine.connect() as conexao_2:
    # with ... as conn --> Garante que, depois, a conexão será fechada automaticamente
    # engine.connect() --> Cria uma conexão com o banco de dados


        resultado_2 = conexao_2.execute(text("""
            SELECT
                id,
                created_on,
                updated_on,
                EXTRACT(YEAR FROM data_nascimento) AS ano_nascimento,

                LEFT(SPLIT_PART(nome, ' ', 1), 1)                                   -- Pega a primeira letra do primeiro nome
                || REPEAT('*', LENGTH(SPLIT_PART(nome, ' ', 1)) - 1)                -- || --> Concatenador  
                || CASE                                                             -- Similar ao IF
                    WHEN POSITION(' ' IN nome) > 0
                    THEN ' ' || SPLIT_PART(nome, ' ', 2)
                    ELSE ''
                END AS nome,

                SUBSTRING(cpf FROM 1 FOR 3) || '.***.***-**' AS cpf,

                LEFT(SPLIT_PART(email, '@', 1), 1)
                || REPEAT('*', LENGTH(SPLIT_PART(email, '@', 1)) - 1)
                || '@'
                || SPLIT_PART(email, '@', 2) AS email,

                RIGHT(REGEXP_REPLACE(telefone, '[^0-9]', '', 'g'), 4) AS telefone
                                                                                    -- telefone --> Coluna original
                                                                                    -- '[^0-9]' --> Tudo que não for número (em regex - expressões regulares - o ^ significa "não")
                                                                                    -- '' --> Substitui por vazio
                                                                                    -- 'g' → Global (substitui todas as ocorrências)                               
            FROM usuarios
        """))


        for registro in resultado_2: # Retorna cada registro (cada linha) do banco  
            ano = int(registro.ano_nascimento) # Converte o ano de cada registro para inteiro
            dados_por_ano[ano].append(registro) # No dicionário "d" , acessa uma lista de ano e adicina o registro nela


    for ano, registros in sorted(dados_por_ano.items()): # sorted --> Organiza em ordem crescente
        nome_arquivo = f"{ano}.csv" # Cria o nome do arquivo
        with open(nome_arquivo, mode="w", newline="", encoding="utf-8") as file:  
        # with open --> Abre/cria o arquivo
        # w --> Escrita
        # newline="" --> Evita linhas em branco a mais
        # utf-8 --> Permite acentos e caracteres especiais
            writer = csv.writer(file) # Cria o "escrevedor" (objeto) que escreve no csv
            writer.writerow([ # Escreve o cabeçalho do arquivo
                "id",
                "nome",
                "cpf",
                "email",
                "telefone",
                "ano_nascimento",
                "created_on",
                "updated_on"
            ])
            for r in registros: # Percorre todos os registros de um determinado ano
                writer.writerow([ # Escreve os dados de cada pessoa no csv
                    r.id,
                    r.nome,
                    r.cpf,
                    r.email,
                    r.telefone,
                    int(r.ano_nascimento),
                    r.created_on,
                    r.updated_on
                ])
        print(f"Arquivo {nome_arquivo} gerado com sucesso.")  


@medir_tempo  
def tempo_da_atividade_3_todos_csv():


    with engine.connect() as conexao_3:  
    # with ... as conn --> Garante que, depois, a conexão será fechada automaticamente
    # engine.connect() --> Cria uma conexão com o banco de dados


        resultado_3 = conexao_3.execute(text("""  
            SELECT
                nome,
                cpf
            FROM usuarios
        """))  
      

        nome_arquivo = "todos.csv" # Define o nome do arquivo 
   

        with open(nome_arquivo, mode="w", newline="", encoding="utf-8-sig") as file:  
        # with open --> Abre/cria o arquivo
        # w --> Escrita
        # newline="" --> Evita linhas em branco a mais
        # utf-8-sig --> Permite acentos e caracteres especiais (especialmente em Excel)


            writer = csv.writer(file) # Cria o "escrevedor" (objeto) que escreve no csv
            writer.writerow([ # Escreve o cabeçalho do arquivo
                "nome",
                "cpf"
            ])
            for row in resultado_3:  
                writer.writerow([
                    row.nome,
                    row.cpf
                ])  
    print(f"Arquivo {nome_arquivo} gerado com sucesso!")  


tempo_da_atividade_2_csv_por_ano()
tempo_da_atividade_3_todos_csv()

# python mini_projeto_2.py
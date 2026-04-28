# Os emoticons abaixo (🔴) foram   P R O P O S I T A L M E N T E   acrescentados como RECURSOS VISUAIS:
#    •Para salientar diferenças importantes;
#    •Para facilitar ♦a revisão e ♦os possíveis estudos futuros do código (por mim mesmo ou por outros).


from sqlalchemy import (
    # sqlalchemy:
    #    •Biblioteca do Python que permite trabalhar com banco de dados
    #    •Permite •conectar, •consultar, •inserir, •alterar e •apagar dados
    create_engine, # Cria uma conexão entre •o programa Python e •o banco de dados
    MetaData, # Objeto do sqlalchemy que guarda informações sobre as tabelas do banco de dados
    Table,
    Column,
    Integer, # Número inteiro
    String, # Texto
    Date, # Data --> YYYY-MM-DD
    DateTime, # Data e hora --> YYYY-MM-DD HH:MM:SS (🔴 USADO PARA   D E F I N I R   UMA COLUNA COMO DATA E HORA)
    insert, # Insere dados na tabela
    text # Permite usar linguagem SQL (DISU --> •Delete, •Insert, •Select, •Update)
)


from datetime import datetime # 🔴 USADO PARA   P R E E N C H E R   UMA COLUNA COM DATA E HORA


import time # Biblioteca que mede o tempo de execução do código


from functools import wraps # Wrap --> Envolver; embrulhar
# functools --> Módulo do Python que permite trabalhar com •decorators, •wraps •etc.
# Wraps --> Função do módulo functools que copia Metadados (W é M ao contrário):
#    •Ao usar um decorator, a função original é substituída por um wrapper...
#    •O problema --> Sem wraps, o wrapper perde os metadados da função original (nome etc.)...
#    •A solução --> O wraps resolve isso copiando esses metadados para o wrapper


def medir_tempo(func): # Decorator --> Função que modifica outra função
    @wraps(func) # Wrap --> Envolver; embrulhar (preserva os metadados da função original - no caso, LGPD)
    def wrapper_embrulhador(*args, **kwargs): # •args (vira uma tupla) <> •kwargs (vira um dicionário)
        inicio = time.perf_counter() # perf_counter --> Contador de alta performance (marca o início da execução)
        resultado = func(*args, **kwargs)
        # •Executa "func" (LGPD), •passando todos os argumentos recebidos pelo wrapper e •guarda o retorno em "resultado"
        fim = time.perf_counter() # perf_counter --> Contador de alta performance (marca o final da execução)
        duracao = fim - inicio # Calcula o tempo de execução
        print(f"A função '{func.__name__}' foi executada em {duracao:.6f} segundos.") # Printa o tempo de execução
        return resultado
    return wrapper_embrulhador


engine = create_engine(
    "postgresql+psycopg2://alunos:AlunoFatec@200.19.224.150:5432/atividade2",
    echo = False # Significado --> "Não mostre no terminal os comandos SQL que foram executados."
)
# create_engine --> Cria conexão com PostgreSQL
# Formato --> postgresql+psycopg2://usuario:senha@host:porta/banco


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


usersss = [] # Lista para guardar os resultados da consulta SQL depois de passar pela função LGPD


with engine.connect() as conn:
# with ... as conn --> Garante que, depois, a conexão será fechada automaticamente
# engine.connect() --> Cria uma conexão com o banco de dados
    result = conn.execute(text( # text --> Permite usar SQL puro
        "SELECT * FROM usuarios LIMIT 5;"
        )
    )
    for row in result: # Percorre os n registros encontrados na linha acima
        row = LGPD(row) 
        # LGPD(row) --> Chama a função LGPD, passando row como argumento
        # row = ... --> O valor retornado pela função substitui o row original
        # adiciona resultado na lista
        usersss.append(row) # Adiciona o resultado na lista "users"


for user in usersss:
    print(user)
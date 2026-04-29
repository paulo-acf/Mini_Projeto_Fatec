from dotenv import load_dotenv
load_dotenv()

import os
from sqlalchemy import create_engine

BANCO_DE_DADOS = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://alunos:AlunoFatec@200.19.224.150:5432/atividade2"
)

engine = create_engine(BANCO_DE_DADOS, echo=False)
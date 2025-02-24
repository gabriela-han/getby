import uvicorn
from fastapi import FastAPI
from fastapi_sqlalchemy import DBSessionMiddleware, db
from fastapi.middleware.cors import CORSMiddleware

from models import Usuario, Sentimento, Sentimento_usuario, Sugestao
from schema import Schema_usuario, Schema_sentimento, Schema_sentimento_usuario, Schema_sugestao
import os

getby = FastAPI()

db_name: str
db_user: str
db_pass: str

with open(os.environ['POSTGRES_DB_FILE'], 'r') as f:
    db_name = f.read().strip()

with open(os.environ['POSTGRES_USER_FILE'], 'r') as f:
    db_user = f.read().strip()

with open(os.environ['POSTGRES_PASSWORD_FILE'], 'r') as f:
    db_pass = f.read().strip()

db_url: str =  f'postgresql://{db_user}:{db_pass}@database/{db_name}'

# CORS error
getby.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# to avoid csrftokenError
getby.add_middleware(DBSessionMiddleware, db_url=db_url)

@getby.get('/')
def hello_world() -> dict[str, str]:
    return {'hello_world': 'hello_world'}

@getby.post('/usuario/', response_model=Schema_usuario)
async def add_usuario(usuario: Schema_usuario):
    novo_usuario = Usuario(nome=usuario.nome, email=usuario.email, senha=usuario.email)
    db.session.add(novo_usuario)
    db.session.commit()
    return novo_usuario

@getby.get('/usuario/')
async def get_usuario():
    usuarios = db.session.query(Usuario).all()
    return usuarios

@getby.post('/sentimento/', response_model=Schema_sentimento)
async def add_sentimento(sentimento: Schema_sentimento):
    novo_sentimento = Sentimento(sentimento=sentimento.sentimento)
    db.session.add(novo_sentimento)
    db.session.commit()
    return novo_sentimento

@getby.get('/sentimento/')
async def get_sentimento():
    sentimentos = db.session.query(Sentimento).all()
    return sentimentos

@getby.post('/sentimento_usuario/', response_model=Schema_sentimento_usuario)
async def add_sentimento_usuario(sentimento_usuario: Schema_sentimento_usuario):
    novo_sentimento_usuario = Sentimento_usuario(id_usuario=sentimento_usuario.id_usuario, id_sentimento=sentimento_usuario.id_sentimento)
    db.session.add(novo_sentimento_usuario)
    db.session.commit()
    return novo_sentimento_usuario

@getby.get('/sentimento_usuario/sentimento/{number}')
async def get_sentimento_usuario_sentimento(number: int):
    sentimentos_usuarios = db.session.query(Sentimento_usuario).filter(Sentimento_usuario.id_sentimento == number).all()
    return sentimentos_usuarios

@getby.get('/sentimento_usuario/usuario/{number}')
async def get_sentimento_usuario_usuario(number: int):
    sentimentos_usuarios = db.session.query(Sentimento_usuario).filter(Sentimento_usuario.id_usuario == number).all()
    return sentimentos_usuarios

@getby.post('/sugestao/', response_model=Schema_sugestao)
async def add_sugestao(sugestao: Schema_sugestao):
    nova_sugestao = Sugestao(id_usuario=sugestao.id_usuario, id_sentimento=sugestao.id_sentimento, sugestao=sugestao.sugestao)
    db.session.add(nova_sugestao)
    db.session.commit()
    return nova_sugestao

@getby.get('/sugestao/')
async def get_sugestao():
    sugestoes = db.session.query(Sugestao).all()
    return sugestoes


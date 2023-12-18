import datetime
import pprint
import pymongo as pyM

client = pyM.MongoClient("mongodb+srv://<pymongo>:password@cluster0.ih0440r.mongodb.net/?retryWrites=true&w=majority")
db = client.test

posts = db.posts

post = [
    {
        "nome": "Leonardo Mercadante",
        "cpf": "123.456.789.10",
        "agencia": "123456-78",
        "tipo": "Conta Corrente",
        "saldo": 1000.00,
    },
    {
        "nome": "Marcia Valetina",
        "cpf": "321.654.987.01",
        "agencia": "456789-10",
        "tipo": "Conta Corrente",
        "saldo": 500.00,
        "email": "marciav@email.com",
        "tags": ["conta", "agencia", "nome"],
        "date": datetime.datetime.utcnow()
    },
    {
        "nome": "Verônica Chaves",
        "cpf": "213.546.879-11",
        "agencia": "321.654-11",
        "tipo": "Conta Corrente",
        "saldo": 10000.00,
        "email": "veronicac@email.com",
        "tags": ["conta", "agencia", "nome"],
        "date": datetime.datetime.utcnow()
    }
]

# Preparando para submeter as infos
result = posts.insert_many(post)
print(result.inserted_ids)

pprint.pprint(posts.find_one())

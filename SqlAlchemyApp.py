import sqlalchemy
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import Session
from sqlalchemy.orm import relationship
from sqlalchemy import Column
from sqlalchemy import Float
from sqlalchemy import select
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy import create_engine
from sqlalchemy import inspect




Base = declarative_base()


class Cliente(Base):
    __tablename__ = "cliente_account"
    # atributos
    id = sqlalchemy.Column(Integer, primary_key=True)
    nome = sqlalchemy.Column(String, nullable=False)
    nomeCompleto = sqlalchemy.Column(String, nullable=False)
    cpf = sqlalchemy.Column(String, nullable=False)
    endereco = sqlalchemy.Column(String, nullable=False)
    email = sqlalchemy.Column(String)

    contas = relationship(
        "Conta", back_populates="cliente", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return (f"Cliente(id={self.id}, nome={self.nome}, nomeCompleto={self.nomeCompleto}, cpf = {self.cpf}, endereco = {self.endereco},"
                f"email={self.email})")

class Conta(Base):
    __tablename__ = "conta"
    id = sqlalchemy.Column(Integer, primary_key=True)
    tipo = sqlalchemy.Column(String(30), nullable=False, default="Conta Corrente")
    id_cliente = sqlalchemy.Column(Integer, ForeignKey("cliente_account.id"), nullable=False)
    numero = sqlalchemy.Column(Integer, nullable=False)
    saldo = sqlalchemy.Column(Float, nullable=False, default=0.00)
    agencia = sqlalchemy.Column(Integer, nullable=False)


    cliente = relationship("Cliente", back_populates="contas")


    def __repr__(self):
        return (f"Conta(id={self.id}, tipo={self.tipo}, id_cliente={self.id_cliente}, numero={self.numero},"
                f"saldo={self.saldo}, agencia={self.agencia})")

print(Cliente.__tablename__)
print(Conta.__tablename__)

# conexão com o bd
engine = create_engine("sqlite://")

# Criando as classes como tabelas no banco de dados
Base.metadata.create_all(engine)

# Investiga o esquema do banco de dados
inspetor_engine = inspect(engine)

print(inspetor_engine.has_table("cliente_account"))
print(inspetor_engine.get_table_names())
print(inspetor_engine.default_schema_name)

with Session(engine) as session:
    leonardo = Cliente(
        nome="leonardo",
        nomeCompleto="Leonardo Mercadante",
        cpf="123.456.789.10",
        endereco="Estrada do cafundó do Judas",
        email="leonardom@email.com",
        contas=[
            Conta(
                tipo="Conta Corrente",
                numero=12345678,
                saldo=500.00,
                agencia=123456
            )
        ]
    )

    marcia = Cliente(
        nome="marcia",
        nomeCompleto="Marcia Valentina",
        cpf="321.654.978.01",
        endereco="Estrada de onde Judas perdeu as botas",
        email="marciaval@email.com",
        contas=[
            Conta(
                tipo="Conta Corrente",
                numero=87654321,
                saldo=100.00,
                agencia=654321
            )
        ]
    )

    veronica = Cliente(
        nome="veronica",
        nomeCompleto="Verônica Chaves Mercadante",
        cpf="231.564.897.11",
        endereco="Estrada do canfundó do Judas",
        email="veronicacm@email.com",
        contas=[
            Conta(
                tipo="Conta Corrente",
                numero=768546213,
                saldo=10000.00,
                agencia=465231
            )
        ]
    )

    session.add_all([leonardo, marcia, veronica])
    session.commit()

    stmt_cliente = select(Cliente).where(Cliente.nome.in_(["leonardo", "marcia", "veronica"]))
    print('Recuperando clientes a partir de condição de filtragem')
    for cliente in session.scalars(stmt_cliente):
        print(cliente)

    stmt_conta = select(Conta).where(Conta.id_cliente.in_([1, 2, 3]))
    print('\nRecuperando as contas dos clientes')
    for conta in session.scalars(stmt_conta):
        print(conta)
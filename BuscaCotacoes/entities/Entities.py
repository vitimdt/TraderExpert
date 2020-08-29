from sqlalchemy import Column, Integer, String, DateTime, Date, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import text

Base = declarative_base()

class Acao(Base):
    __tablename__ = 'acao'
    id = Column(Integer, primary_key=True)
    codigo = Column(String(8))
    nome = Column(String(70))
    nome_api = Column(String(255))

    cotacoes = relationship('CotacaoTempoReal', backref="acoes")

    def __repr__(self):
        return f'Ação {self.nome}'

    @classmethod
    def find_all(cls, session):
        return session.query(cls).all()

    @classmethod
    def find_by_code(cls, session, codigo):
        return session.query(cls).filter_by(codigo=codigo).first()

    @classmethod
    def find_by_id(cls, session, id):
        return session.query(cls).filter_by(id=id).first()

class Configuracao(Base):
    __tablename__ = 'configuracao'
    id = Column(Integer, primary_key=True)
    chave = Column(String(50))
    valor = Column(String(500))

    def __repr__(self):
        return f'Configuração {self.chave}'

    @classmethod
    def find_by_key(cls, session, chave):
        return session.query(cls).filter_by(chave=chave).first()

class CotacaoTempoReal(Base):
    __tablename__ = 'cotacao_temporeal'
    id = Column(Integer, primary_key=True)
    acao_id = Column(Integer, ForeignKey('acao.id'))
    valor = Column(Float)
    data_atualizacao = Column(DateTime)
    hora_pregao = Column(String(10))
    acao = relationship('Acao')

    def __repr__(self):
        return f'CotacaoTempoReal {self.acao_id} - {self.valor} - {self.data_atualizacao}'

    @classmethod
    def clear_table(cls, conn, dataAtual):
        trn = conn.begin()
        conn.execute('DELETE FROM ' + cls.__tablename__ + ' WHERE id > 0 AND data_atualizacao < "' +
                     str(dataAtual.year) + '-' + str(dataAtual.month) + '-' + str(dataAtual.day) + ' 00:00:00"')
        trn.commit()

    @classmethod
    def find_by_acao(cls, session, id_acao):
        return session.query(cls).filter_by(acao_id=id_acao).all()

class Carteira(Base):
    __tablename__ = 'carteira'
    id = Column(Integer, primary_key=True)
    email = Column(String(100))
    acao_id = Column(Integer, ForeignKey('acao.id'))
    data_compra = Column(Date)
    quantidade = Column(Integer)
    valor = Column(Float)
    valor_taxas = Column(Float)
    valor_total = Column(Float)
    acao = relationship('Acao')

    def __repr__(self):
        return f'Carteira {self.acao_id} - {self.data_compra} - {self.quantidade} - {self.valor}'

    @classmethod
    def find_all(cls, session):
        return session.query(cls).all()

class Monitoramento(Base):
    __tablename__ = 'monitoramento'
    id = Column(Integer, primary_key=True)
    acao_id = Column(Integer, ForeignKey('acao.id'))
    valor_ref = Column(Float)
    operador = Column(String(2))
    valor_meta_dif = Column(Float)
    sugestao = Column(String(50))
    flg_percentual = Column(String(1))
    flg_ativo = Column(String(1))
    acao = relationship('Acao')

    def __repr__(self):
        return f'Monitoramento {self.acao_id} - {self.valor_ref} - {self.operador} - {self.valor_meta_dif}'

    @classmethod
    def find_by_ativos(cls, session):
        return session.query(cls).filter_by(flg_ativo='S').all()

    @classmethod
    def find_monitoramento_fora_carteira(cls, conn):
        qry = text("select monitoramento.id, monitoramento.acao_id, monitoramento.valor_ref, "
                   "monitoramento.operador, monitoramento.valor_meta_dif, monitoramento.sugestao, "
                   "monitoramento.flg_percentual, monitoramento.flg_ativo from monitoramento, acao "
                   "where monitoramento.acao_id = acao.id and "
                   "monitoramento.acao_id not in (select c.acao_id from carteira c) and "
                   "monitoramento.flg_ativo='S'")
        return conn.execute(qry).fetchall()

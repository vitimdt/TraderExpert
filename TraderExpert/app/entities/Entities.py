from app import db
from sqlalchemy.sql import text
from datetime import datetime

class Acao(db.Model):
    __tablename__ = 'acao'
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(8))
    nome = db.Column(db.String(70))
    nome_api = db.Column(db.String(255))

    cotacoes = db.relationship('CotacaoTempoReal', backref="acoes")

    def __repr__(self):
        return f'Ação {self.nome}'

    def find_all(self):
        return Acao.query.all()

    def find_by_code(self, codigo):
        return Acao.query.filter_by(codigo=codigo).first()

class Configuracao(db.Model):
    __tablename__ = 'configuracao'
    id = db.Column(db.Integer, primary_key=True)
    chave = db.Column(db.String(50))
    valor = db.Column(db.String(500))

    def __repr__(self):
        return f'Configuração {self.chave}'

    def find_by_key(self, chave):
        return Configuracao.query.filter_by(chave=chave).first()

class CotacaoTempoReal(db.Model):
    __tablename__ = 'cotacao_temporeal'
    id = db.Column(db.Integer, primary_key=True)
    acao_id = db.Column(db.Integer, db.ForeignKey('acao.id'))
    valor = db.Column(db.Float)
    data_atualizacao = db.Column(db.DateTime)
    hora_pregao = db.Column(db.String(10))
    acao = db.relationship('Acao')

    def __repr__(self):
        return f'CotacaoTempoReal {self.acao_id} - {self.valor} - {self.data_atualizacao}'

    @classmethod
    def clear_table(cls, conn, dataAtual):
        trn = conn.begin()
        conn.execute('DELETE FROM ' + cls.__tablename__ + ' WHERE id > 0 AND data_atualizacao < "' +
                     str(dataAtual.year) + '-' + str(dataAtual.month) + '-' + str(dataAtual.day) + ' 00:00:00"')
        trn.commit()

    def find_by_acao(self, id_acao):
        return CotacaoTempoReal.query.filter_by(acao_id=id_acao).all()

    @classmethod
    def buscaCotacaoTR(cls):
        qry = text("SELECT tab.codigo, tab.nome, tab.valor, tab.quantidade, tab.valor_cotacao, tab.DIF, "
                   "tab.Valor_Total_Invest, tab.Valor_Total_Bolsa, tab.Percentual, tab.data_atualizacao, "
                   "tab.hora_pregao FROM (SELECT ct.id, a.codigo, a.nome, c.valor, c.quantidade, "
                   "ct.valor as Valor_Cotacao, ct.data_atualizacao, ct.hora_pregao, "
                   "round(ct.valor - c.valor,2) as DIF, round(c.valor*c.quantidade,2) as Valor_Total_Invest, "
                   "round(ct.valor*c.quantidade,2) as Valor_Total_Bolsa, "
                   "CONCAT(round((((ct.valor*c.quantidade) - (c.valor*c.quantidade)) * 100) / "
                   "(c.valor*c.quantidade),2), ' %') as Percentual "
                   "FROM cotacao_temporeal ct, acao a, carteira c "
                   "WHERE ct.acao_id = a.id and c.acao_id = a.id and ct.data_atualizacao = "
                   "(select max(aux.data_atualizacao) from cotacao_temporeal aux where aux.acao_id = a.id) "
                   ") AS tab ORDER BY tab.id")
        columns = ['Código', 'Nome', 'Valor Compra', 'Quantidade', 'Cotação', 'Diferença',
                   'Investimento', 'Total Cotação', 'Percentual', 'Hora Atualização', 'Hora Cotação']
        cotacoesTR = db.engine.execute(qry).fetchall()
        resultSet = []
        totInvest = 0
        totCotacao = 0
        for lin in cotacoesTR:
            totInvest += lin[6]
            totCotacao += lin[7]
            resultSet.append({columns[0]: lin[0],
                              columns[1]: lin[1],
                              columns[2]: str(lin[2]).replace('.', ','),
                              columns[3]: lin[3],
                              columns[4]: str(lin[4]).replace('.', ','),
                              columns[5]: str(lin[5]).replace('.', ','),
                              columns[6]: str(lin[6]).replace('.', ','),
                              columns[7]: str(lin[7]).replace('.', ','),
                              columns[8]: str(lin[8]).replace('.', ','),
                              columns[9]: lin[9].strftime("%d/%m/%Y %H:%M:%S"),
                              columns[10]: lin[10]})
        totais = []
        totais.append(str(round(totInvest, 2)).replace('.', ','))
        totais.append(str(round(totCotacao, 2)).replace('.', ','))
        totais.append(str(round(totCotacao - totInvest, 2)).replace('.', ','))
        totais.append(str(round(((totCotacao - totInvest)*100)/totInvest, 2)).replace('.', ','))
        return columns, resultSet, totais

class Carteira(db.Model):
    __tablename__ = 'carteira'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100))
    acao_id = db.Column(db.Integer, db.ForeignKey('acao.id'))
    data_compra = db.Column(db.Date)
    quantidade = db.Column(db.Integer)
    valor = db.Column(db.Float)
    valor_taxas = db.Column(db.Float)
    valor_total = db.Column(db.Float)
    acao = db.relationship('Acao')

    def __repr__(self):
        return f'Carteira {self.acao_id} - {self.data_compra} - {self.quantidade} - {self.valor}'

    def find_all(self):
        return Carteira.query.all()

class Monitoramento(db.Model):
    __tablename__ = 'monitoramento'
    id = db.Column(db.Integer, primary_key=True)
    acao_id = db.Column(db.Integer, db.ForeignKey('acao.id'))
    valor_ref = db.Column(db.Float)
    operador = db.Column(db.String(2))
    valor_meta_dif = db.Column(db.Float)
    sugestao = db.Column(db.String(50))
    flg_percentual = db.Column(db.String(1))
    flg_ativo = db.Column(db.String(1))
    acao = db.relationship('Acao')

    def __repr__(self):
        return f'Monitoramento {self.acao_id} - {self.valor_ref} - {self.operador} - {self.valor_meta_dif}'

    def find_by_ativos(self):
        return Monitoramento.query.filter_by(flg_ativo='S').all()

    @classmethod
    def buscaMonitoramentos(cls):
        qry = text("SELECT a.codigo, a.nome, ct.valor, m.valor_ref, m.operador, m.valor_meta_dif, "
                   "m.sugestao, ct.data_atualizacao, ct.hora_pregao FROM cotacao_temporeal ct, "
                   "acao a, monitoramento m WHERE ct.acao_id = a.id AND m.acao_id = a.id AND "
                   "ct.data_atualizacao = (SELECT MAX(aux.data_atualizacao) "
                   "FROM cotacao_temporeal aux WHERE aux.acao_id = a.id)")
        columns = ['Código', 'Nome', 'Valor Cotação', 'Valor Alvo', 'Hora Atualização', "Hora Cotação"]
        monitores = db.engine.execute(qry).fetchall()
        resultSet = []
        for lin in monitores:
            if str(lin[4]) == '-':
                resultSet.append({columns[0]: lin[0],
                                  columns[1]: lin[1],
                                  columns[2]: str(lin[2]).replace('.', ','),
                                  columns[3]: str(round(lin[3]-lin[5], 2)).replace('.', ','),
                                  columns[4]: lin[7].strftime("%d/%m/%Y %H:%M:%S"),
                                  columns[5]: lin[8]})
            elif str(lin[4]) == '+':
                resultSet.append({columns[0]: lin[0],
                                  columns[1]: lin[1],
                                  columns[2]: str(lin[2]).replace('.', ','),
                                  columns[3]: str(round(lin[3] + lin[5], 2)).replace('.', ','),
                                  columns[4]: lin[7].strftime("%d/%m/%Y %H:%M:%S"),
                                  columns[5]: lin[8]})
        return columns, resultSet

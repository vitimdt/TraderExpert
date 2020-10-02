from app import db
from sqlalchemy.sql import text
from datetime import datetime

class Acao(db.Model):
    __tablename__ = 'acao'
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(8))
    nome = db.Column(db.String(70))

    cotacoes = db.relationship('CotacaoTempoReal', backref="acoes")

    def __repr__(self):
        return f'Ação {self.nome}'

    def find_all(self):
        return Acao.query.all()

    def retorna_lista_acoes(self):
        acoes = Acao.query.all()
        lista = []
        for acao in acoes:
            lista.append((acao.id, acao.nome))
        return lista

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
                   "tab.hora_pregao, tab.valor_taxas FROM (SELECT ct.id, a.codigo, a.nome, c.valor, c.quantidade, "
                   "ct.valor as Valor_Cotacao, ct.data_atualizacao, ct.hora_pregao, "
                   "round(ct.valor - c.valor,2) as DIF, round(c.valor*c.quantidade,2) as Valor_Total_Invest, "
                   "round(ct.valor*c.quantidade,2) as Valor_Total_Bolsa, "
                   "CONCAT(round((((ct.valor*c.quantidade) - (c.valor*c.quantidade)) * 100) / "
                   "(c.valor*c.quantidade),2), ' %') as Percentual, c.valor_taxas "
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
            totInvest += lin[6] + lin[11]
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
        if totInvest > 0:
            totais.append(str(round(((totCotacao - totInvest)*100)/totInvest, 2)).replace('.', ','))
        else:
            totais.append('0,00')
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

    def find_by_id(self, id_carteira):
        return Carteira.query.filter_by(id=id_carteira).first()

    @classmethod
    def retornarCarteira(cls):
        qry = text("SELECT c.id, a.codigo, a.nome, c.valor, c.quantidade, c.valor_taxas, "
                   "c.valor_total, c.data_compra FROM carteira c, acao a "
                   "WHERE c.acao_id = a.id ORDER BY a.codigo")
        columns = ['ID', 'Código', 'Nome', 'Valor Compra', 'Quantidade', 'Valor Taxas', "Total",
                   "Data Compra", "Excluir"]
        carteira = db.engine.execute(qry).fetchall()
        resultSet = []
        for lin in carteira:
            resultSet.append({columns[0]: lin[0],
                              columns[1]: lin[1],
                              columns[2]: lin[2],
                              columns[3]: str(lin[3]).replace('.', ','),
                              columns[4]: lin[4],
                              columns[5]: str(lin[5]).replace('.', ','),
                              columns[6]: str(lin[6]).replace('.', ','),
                              columns[7]: lin[7].strftime("%d/%m/%Y"),
                              columns[8]: lin[0]})
        return columns, resultSet

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

    def find_by_id(self, id_monitoramento):
        return Monitoramento.query.filter_by(id=id_monitoramento).first()

    @classmethod
    def todosMonitoramentos(cls):
        qry = text("SELECT m.id, a.codigo, a.nome, m.valor_ref, m.operador, m.valor_meta_dif, m.sugestao, "
                   "m.flg_percentual, m.flg_ativo FROM monitoramento m, acao a "
                   "WHERE m.acao_id = a.id ORDER BY a.codigo")
        columns = ['ID', 'Código', 'Nome', 'Valor Referência', 'Operador', 'Valor Diferença', "Sugestão",
                   "Percentual?", "Ativo?"]
        monitores = db.engine.execute(qry).fetchall()
        resultSet = []
        for lin in monitores:
            perc = 'SIM'
            ativo = 'SIM'
            if lin[7] == 'N':
                perc = 'Não'
            else:
                perc = 'Sim'
            if lin[8] == 'N':
                ativo = 'Não'
            else:
                ativo = 'Sim'
            resultSet.append({columns[0]: lin[0],
                              columns[1]: lin[1],
                              columns[2]: lin[2],
                              columns[3]: str(lin[3]).replace('.', ','),
                              columns[4]: lin[4],
                              columns[5]: str(lin[5]).replace('.', ','),
                              columns[6]: lin[6],
                              columns[7]: perc,
                              columns[8]: ativo})
        return columns, resultSet

    @classmethod
    def buscaMonitoramentos(cls):
        qry = text("SELECT m.id, a.codigo, a.nome, ct.valor, m.valor_ref, m.operador, m.valor_meta_dif, "
                   "m.sugestao, ct.data_atualizacao, ct.hora_pregao FROM cotacao_temporeal ct, "
                   "acao a, monitoramento m WHERE ct.acao_id = a.id AND m.acao_id = a.id AND "
                   "ct.data_atualizacao = (SELECT MAX(aux.data_atualizacao) "
                   "FROM cotacao_temporeal aux WHERE aux.acao_id = a.id) AND m.flg_ativo = 'S' "
                   "ORDER BY a.codigo")
        columns = ['ID', 'Código', 'Nome', 'Valor Cotação', 'Valor Alvo', 'Hora Atualização', "Hora Cotação", "Sugestão", "Status"]
        monitores = db.engine.execute(qry).fetchall()
        resultSet = []
        for lin in monitores:
            valor_alvo = 0
            status = "NOK"
            if str(lin[5]) == '-':
                valor_alvo = round(lin[4] - lin[6], 2)
            elif str(lin[5]) == '+':
                valor_alvo = round(lin[4] + lin[6], 2)
            if (lin[7] == "COMPRA") and (lin[3] < valor_alvo):
                status = "OK"
            elif (lin[7] == "VENDA") and (lin[3] > valor_alvo):
                status = "OK"
            resultSet.append({columns[0]: str(lin[0]),
                              columns[1]: lin[1],
                              columns[2]: lin[2],
                              columns[3]: str(lin[3]).replace('.', ','),
                              columns[4]: str(valor_alvo).replace('.', ','),
                              columns[5]: lin[8].strftime("%d/%m/%Y %H:%M:%S"),
                              columns[6]: lin[9],
                              columns[7]: lin[7],
                              columns[8]: status})
        return columns, resultSet

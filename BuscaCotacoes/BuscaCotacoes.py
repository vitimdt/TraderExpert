import re
import urllib3
import datetime
import time
import os
from dotenv import load_dotenv
from db.DBConnection import DBConnection
from entities.Entities import Configuracao, Carteira, CotacaoTempoReal

class BuscaCotacoes:

    api_key = None
    dbConn = None
    http = urllib3.PoolManager()
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'

    def __init__(self):
        project_folder = os.path.expanduser('.\\')
        load_dotenv(os.path.join(project_folder, 'params.env'))
        self.api_key = os.getenv("API_KEY")
        self.dbConn = DBConnection()
        if not self.dbConn.connectionCreated():
            self.dbConn.createConnection(os.getenv("STR_CONN"))

    def iniciarColetaCotacoes(self):
        data_hora = self.dateTimeNow()
        CotacaoTempoReal.clear_table(conn=self.dbConn.conn, dataAtual=data_hora)
        while 10 <= data_hora.hour <= 18:
            self.coletar_cotacoes()
            time.sleep(1800)
            data_hora = self.dateTimeNow()
        self.dbConn.disposeConnection()

    def coletar_cotacoes(self):
        config = Configuracao.find_by_key(self.dbConn.session, self.api_key)
        cart = Carteira.find_all(self.dbConn.session)
        headers = {'User-Agent': self.user_agent}

        for op in cart:
            url = config.valor.format(op.acao.nome_api)
            response = self.http.request('GET', url, headers)
            hora_pregao = self.extrairHoraAtualizacao(response.data.decode('utf-8'))
            try:
                valor = self.extrairValorCotacao(response.data.decode('utf-8'))
                cotacao = CotacaoTempoReal(acao_id=op.acao.id,
                                           valor=float(valor.replace(',', '.')),
                                           data_atualizacao=self.dateTimeNow(),
                                           hora_pregao=hora_pregao)
                self.dbConn.session.add(cotacao)
            except:
                print("Não foi possível recuperar cotação da ação: " + op.acao.codigo)
        self.dbConn.session.commit()
        print("[" + time.ctime() + "] Cotações coletadas com sucesso!")

    def extrairValorCotacao(self, msg):
        result = re.search(r'\<div class\=\"value\"\>\n                                    \<p\>[0-9\,]*\<\/p\>', msg).group()
        result = re.split(r'\<p\>|\<\/p\>', result)[1]
        return result

    def extrairHoraAtualizacao(self, msg):
        try:
            result = re.search(r'[0-9h0-9]+. Delay 15 min', msg).group()
            result = result.split('.')[0]
            result = result.replace('h', ':')
        except:
            result = ""
        return result

    def dateTimeNow(self):
        now = datetime.datetime.now()
        return now

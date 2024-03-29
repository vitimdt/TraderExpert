import re
import urllib3
import datetime
import time
import os
import sys
from dotenv import load_dotenv
from db.DBConnection import DBConnection
from entities.Entities import Configuracao, Carteira, CotacaoTempoReal, Monitoramento, Acao, AcessoAPI

class BuscaCotacoes:

    api_key = None
    time_sleep = None
    dbConn = None
    http = urllib3.PoolManager()
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'

    def __init__(self):
        project_folder = os.path.expanduser('.\\')
        load_dotenv(os.path.join(project_folder, 'params.env'))
        self.api_key = os.getenv("API_KEY")
        self.time_sleep = os.getenv("TIME_SLEEP")
        self.dbConn = DBConnection()
        if not self.dbConn.connectionCreated():
            self.dbConn.createConnection(os.getenv("STR_CONN"))

    def iniciarColetaCotacoes(self):
        data_hora = self.dateTimeNow()
        CotacaoTempoReal.clear_table(conn=self.dbConn.conn, dataAtual=data_hora)
        while 10 <= data_hora.hour <= 17:
            self.coletar_cotacoes()
            self.coletar_cotacoes_monitoramento()
            print("[" + time.ctime() + "] Cotações coletadas com sucesso!")
            time.sleep(int(self.time_sleep))
            data_hora = self.dateTimeNow()
        self.dbConn.disposeConnection()

    def coletar_cotacoes(self):
        config = Configuracao.find_by_key(self.dbConn.session, self.api_key)
        acao = Acao.find_acoes_carteira(conn=self.dbConn.session)
        headers = {'User-Agent': self.user_agent}

        for item in acao:
            acesso_api = AcessoAPI.find_by_api_acao(self.dbConn.session, api_id=config.id, acao_id=item.id)
            if acesso_api is not None:
                url = config.valor.format(acesso_api.nome_api)
                response = self.http.request('GET', url, preload_content=False, headers=headers)
                try:
                    hora_pregao = self.extrairHoraAtualizacao(response.data.decode('utf-8'))
                    valor = self.extrairValorCotacao(response.data.decode('utf-8'))
                    cotacao = CotacaoTempoReal(acao_id=item.id,
                                               valor=float(valor.replace(',', '.')),
                                               data_atualizacao=self.dateTimeNow(),
                                               hora_pregao=hora_pregao)
                    self.dbConn.session.add(cotacao)
                except:
                    print("Não foi possível recuperar cotação da ação: " + item.codigo + ".")
            else:
                print("Não existe Nome de API para ação: " + item.codigo)
        self.dbConn.session.commit()

    def coletar_cotacoes_monitoramento(self):
        config = Configuracao.find_by_key(self.dbConn.session, self.api_key)
        listaAcaoMonitor = Acao.find_acoes_monitoradas_fora_carteira(conn=self.dbConn.conn)
        headers = {'User-Agent': self.user_agent}

        for item in listaAcaoMonitor:
            acao = Acao.find_by_id(self.dbConn.session, item.id)
            acesso_api = AcessoAPI.find_by_api_acao(self.dbConn.session, api_id=config.id, acao_id=acao.id)
            if acesso_api is not None:
                url = config.valor.format(acesso_api.nome_api)
                response = self.http.request('GET', url, preload_content=False, headers=headers)
                try:
                    hora_pregao = self.extrairHoraAtualizacao(response.data.decode('utf-8'))
                    valor = self.extrairValorCotacao(response.data.decode('utf-8'))
                    cotacao = CotacaoTempoReal(acao_id=item.id,
                                               valor=float(valor.replace(',', '.')),
                                               data_atualizacao=self.dateTimeNow(),
                                               hora_pregao=hora_pregao)
                    self.dbConn.session.add(cotacao)
                except:
                    print("Não foi possível recuperar cotação da ação: " + acao.codigo + ".")
            else:
                print("Não existe Nome de API para ação: " + acao.codigo)
        self.dbConn.session.commit()

    def extrairValorCotacao(self, msg):
        try:
            if self.api_key == 'API_INFOM':
                result = re.search(r'\<div class\=\"value\"\>\n                                    \<p\>[0-9\,]*\<\/p\>',
                                   msg).group()
                result = re.split(r'\<p\>|\<\/p\>', result)[1]
            elif self.api_key == 'API_INVES':
                result = re.search(r'data-test\=\"instrument-price-last\"\>[0-9\,]*\<\/span\>',
                                   msg).group()
                result = re.split(r'\>|\<\/span\>', result)[1]
        except Exception as ex:
            print(ex)
            result = ""
        return result

    def extrairHoraAtualizacao(self, msg):
        try:
            if self.api_key == 'API_INFOM':
                result = re.search(r'[0-9h0-9]+. Delay 15 min', msg).group()
                result = result.split('.')[0]
                result = result.replace('h', ':')
            elif self.api_key == 'API_INVES':
                result = re.search(r'Z\"\>[0-9\:]*\<\/time\>', msg).group()
                result = re.split(r'\>|\<\/time\>', result)[1]
        except Exception as ex:
            print(ex)
            result = ""
        return result

    def dateTimeNow(self):
        now = datetime.datetime.now()
        return now

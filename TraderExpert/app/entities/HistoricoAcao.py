import requests
import sys
from datetime import date


class HistoricoAcao():
    arrDia = []
    arrCotacao = []

    def __init__(self):
        self.arrDia = []
        self.arrCotacao = []

    def buscarHistorico(self, codAcao, urlAPI, keyAPI):
        url = urlAPI
        params = dict(
            function='TIME_SERIES_DAILY',
            symbol=str(codAcao+'.sa'),
            outputsize='full',
            apikey=keyAPI
        )

        response = requests.get(url=url, params=params)
        try:
            json_data = response.json()
        except ValueError as exc:
            print(f"Exception: {exc}")
            # to find out why you have got this exception, you can see the response content and header
            print(str(response.content))
            print(str(response.headers))
            print(sys.exc_info())
            return False
        else:
            if json_data.get('Error Message') is not None:
                print(json_data.get('Error Message'))
                return False
            else:
                serieTemporal = json_data.get('Time Series (Daily)')
                for item in serieTemporal:
                    arrData = str(item).split('-')
                    '''if arrData[0] == '2021':'''
                    self.arrDia.append(date(*map(int, arrData)))
                    self.arrCotacao.append(float(serieTemporal[item].get('4. close')))
                self.arrDia.reverse()
                self.arrCotacao.reverse()
                return True

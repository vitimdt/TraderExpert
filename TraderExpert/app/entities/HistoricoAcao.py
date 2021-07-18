import requests
import sys
from datetime import date, datetime


class HistoricoAcao():
    arrDia = []
    arrCotacao = []

    def __init__(self):
        self.arrDia = []
        self.arrCotacao = []

    def buscarHistorico(self, codAcao, dataInicial, dataFinal, urlAPI, keyAPI):
        temDataInicial = False
        temDataFinal = False
        arrDataInicial = str(dataInicial).split(" ")
        objDataInicial = datetime.strptime(arrDataInicial[1] + " " +
                                           arrDataInicial[2] + " " +
                                           arrDataInicial[3], '%d %b %Y')
        arrDataFinal = str(dataFinal).split(" ")
        objDataFinal = datetime.strptime(arrDataFinal[1] + " " +
                                         arrDataFinal[2] + " " +
                                         arrDataFinal[3], '%d %b %Y')
        if objDataInicial.strftime("%d/%m/%Y") != "01/01/0001":
            temDataInicial = True
        if objDataFinal.strftime("%d/%m/%Y") != "01/01/0001":
            temDataFinal = True

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
                    dataCotacao = date(*map(int, arrData))
                    if temDataInicial and temDataFinal:
                        if objDataInicial.date() <= dataCotacao <= objDataFinal.date():
                            self.arrDia.append(dataCotacao)
                            self.arrCotacao.append(float(serieTemporal[item].get('4. close')))
                    elif temDataInicial and not temDataFinal:
                        if objDataInicial.date() <= dataCotacao:
                            self.arrDia.append(dataCotacao)
                            self.arrCotacao.append(float(serieTemporal[item].get('4. close')))
                    elif not temDataInicial and temDataFinal:
                        if dataCotacao <= objDataFinal.date():
                            self.arrDia.append(dataCotacao)
                            self.arrCotacao.append(float(serieTemporal[item].get('4. close')))
                    elif not temDataInicial and not temDataFinal:
                        self.arrDia.append(dataCotacao)
                        self.arrCotacao.append(float(serieTemporal[item].get('4. close')))

                self.arrDia.reverse()
                self.arrCotacao.reverse()
                return True

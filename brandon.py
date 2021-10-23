#!/usr/bin/env python3

#o server precisa estar rodando

import csv
from datetime import date

import re
import urllib.request
import urllib.parse
import http.cookiejar

from lxml.html import fragment_fromstring
from collections import OrderedDict
from decimal import Decimal

def get_data(*args, **kwargs):
    url = 'http://www.fundamentus.com.br/resultado.php'
    cookie_jar = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookie_jar))
    opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows; U; Windows NT 6.1; rv:2.2) Gecko/20110201'),
                         ('Accept', 'text/html, text/plain, text/css, text/sgml, */*;q=0.01')]

    # Aqui estão os parâmetros de busca das ações
    # Estão em branco para que retorne todas as disponíveis
    data = {'pl_min': '',
            'pl_max': '',
            'pvp_min': '',
            'pvp_max' : '',
            'psr_min': '',
            'psr_max': '',
            'divy_min': '',
            'divy_max': '',
            'pativos_min': '',
            'pativos_max': '',
            'pcapgiro_min': '',
            'pcapgiro_max': '',
            'pebit_min': '',
            'pebit_max': '',
            'fgrah_min': '',
            'fgrah_max': '',
            'firma_ebit_min': '',
            'firma_ebit_max': '',
            'margemebit_min': '',
            'margemebit_max': '',
            'margemliq_min': '',
            'margemliq_max': '',
            'liqcorr_min': '',
            'liqcorr_max': '',
            'roic_min': '',
            'roic_max': '',
            'roe_min': '',
            'roe_max': '',
            'liq_min': '',
            'liq_max': '',
            'patrim_min': '',
            'patrim_max': '',
            'divbruta_min': '',
            'divbruta_max': '',
            'tx_cresc_rec_min': '',
            'tx_cresc_rec_max': '',
            'setor': '',
            'negociada': 'ON',
            'ordem': '1',
            'x': '28',
            'y': '16'}

    with opener.open(url, urllib.parse.urlencode(data).encode('UTF-8')) as link:
        content = link.read().decode('ISO-8859-1')

    pattern = re.compile('<table id="resultado".*</table>', re.DOTALL)
    content = re.findall(pattern, content)[0]
    page = fragment_fromstring(content)
    result = OrderedDict()

    for rows in page.xpath('tbody')[0].findall("tr"):
        result.update({rows.getchildren()[0][0].getchildren()[0].text: {'Cotacao': todecimal(rows.getchildren()[1].text),
                                                                        'PL': todecimal(rows.getchildren()[2].text),
                                                                        'PVP': todecimal(rows.getchildren()[3].text),
                                                                        'PSR': todecimal(rows.getchildren()[4].text),
                                                                        'DY': todecimal(rows.getchildren()[5].text),
                                                                        'PAtivo': todecimal(rows.getchildren()[6].text),
                                                                        'PCapGiro': todecimal(rows.getchildren()[7].text),
                                                                        'PEBIT': todecimal(rows.getchildren()[8].text),
                                                                        'PACL': todecimal(rows.getchildren()[9].text),
                                                                        'EVEBIT': todecimal(rows.getchildren()[10].text),
                                                                        'EVEBITDA': todecimal(rows.getchildren()[11].text),
                                                                        'MrgEbit': todecimal(rows.getchildren()[12].text),
                                                                        'MrgLiq': todecimal(rows.getchildren()[13].text),
                                                                        'LiqCorr': todecimal(rows.getchildren()[14].text),
                                                                        'ROIC': todecimal(rows.getchildren()[15].text),
                                                                        'ROE': todecimal(rows.getchildren()[16].text),
                                                                        'Liq2meses': todecimal(rows.getchildren()[17].text),
                                                                        'PatLiq': todecimal(rows.getchildren()[18].text),
                                                                        'DivBrutPat': todecimal(rows.getchildren()[19].text),
                                                                        'Cresc5anos': todecimal(rows.getchildren()[20].text)}})
    
    return result
                                                                        
    
def todecimal(string):
  string = string.replace('.', '')
  string = string.replace(',', '.')

  if (string.endswith('%')):
    string = string[:-1]
    return Decimal(string) / 100
  else:
    return Decimal(string)

if __name__ == '__main__':
    from waitingbar import WaitingBar
    
    progress_bar = WaitingBar('[*] Downloading...')
    result = get_data()
    progress_bar.stop()

    #result_format = '{0:<7} {1:<7} {2:<10} {3:<7} {4:<10} {5:<7} {6:<10} {7:<10} {8:<10} {9:<11} {10:<11} {11:<7} {12:<11} {13:<11} {14:<7} {15:<11} {16:<5} {17:<7}'
    
                   
    



def format_name():
    
    return f"bigquerytable.csv"


#formata o nome da tabela



# vai escrever o csv !nao ter pontuacao em nada
def to_csv(result):
    with open(format_name(), mode='w') as file:
        writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        writer.writerow(['Posicao','acao', 'PL', 'cotacao', 'PVP', 'PSR','DY', 'PAtivo','PCapGiro','PEBIT','PACL','EVEBIT','EVEBITDA','MrgEbit','MrgLiq','LiqCorr','ROIC','ROE','Liq2meses','PatLiq','DivBrutPat','Cresc5anos'])

        index = 1
        for key, value in result.items():
            writer.writerow([
                index,
                key,
                value['PL'],
                value['Cotacao'],
                value['PVP'],
                value['PSR'],
                value['DY'],
                value['PAtivo'],
                value['PCapGiro'],
                value['PEBIT'],
                value['PACL'],
                value['EVEBIT'],
                value['EVEBITDA'],
                value['MrgEbit'],
                value['MrgLiq'],
                value['LiqCorr'],
                value['ROIC'],
                value['ROE'],
                value['Liq2meses'],
                value['PatLiq'],
                value['DivBrutPat'],
                value['Cresc5anos']
                ])
            index = index + 1

to_csv(result)













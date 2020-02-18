try:
    from urllib.request import urlopen
except ImportError:
    from urllib2 import urlopen
from bs4 import BeautifulSoup
import csv
import sys
reload(sys)
sys.setdefaultencoding('utf8') 


page = 'https://www.ssp.sp.gov.br/Estatistica/ViolenciaMulher.aspx'
content = urlopen(page)
soup = BeautifulSoup(content, 'html.parser')
tables = soup.findAll('table')
 
linesContent = []
for i in range(2, len(tables)+1):
    dataText = soup.find('span', {'id':'conteudo_repPeriodo_lblPeriodo_'+str(i)}).text
    mesAno = str(dataText).split(':')[1].replace('de','|').replace(' ','').split('|')
    table = soup.find('table',{'id':'conteudo_repPeriodo_grdOcorrencias_'+str(i)})
    rows = table.findAll('tr')
    for i in range(1, len(rows)):
        cells = rows[i].findAll('td')
        obj = {
            'mes': mesAno[0],
            'ano': mesAno[1],
            'tipo':str(cells[0].text),
            'regCapital':int(cells[1].text),
            'regDemacro':int(cells[2].text),
            'regInterior':int(cells[3].text),
            'total':int(cells[4].text)
        }
        linesContent.append(obj)
 
file = open('result.csv', 'w')
with file:
    fieldNames = ['mes', 'ano','tipo','regCapital','regDemacro','regInterior','total']
    writer = csv.DictWriter(file, fieldnames=fieldNames, quoting=csv.QUOTE_ALL)
    writer.writeheader()
    for line in linesContent:
        writer.writerow(line)
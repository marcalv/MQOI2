from read import getData
from launcher import  checkSolution, completeSolve
from write import writeSolution
from read import readlines
import os

def get_objetivos():
    objetivos = {}
    lines = readlines('objetivos.txt')
    for line in lines:
        split_line = line.split(': ')
        objetivos[split_line[0]] = split_line[1]
    return objetivos

def make_line(dataFileExample,objetivos,bestSolution):
    objetivo = float(objetivos[dataFileExample])
    percent_mejora = ((objetivo - bestSolution['totalCost']) / objetivo)*100

    lineitems=[]
    lineitems.append(dataFileExample)
    lineitems.append(objetivos[dataFileExample].replace('.',','))
    lineitems.append(str(bestSolution['totalCost']).replace('.',','))
    lineitems.append(str(percent_mejora).replace('.',','))
    lineitems.append(str(bestSolution['executionTime']).replace('.',','))
    lineitems.append(str(bestSolution['sortingMethod']))
    lineitems.append(str(bestSolution['placingMethod']))
    lineitems.append(str(bestSolution['localOpt']))
    lineitems.append(str(len(bestSolution['log'])-1))
    lineitems.append(str(bestSolution['timeOut']))
    lineitems.append(str(bestSolution['wentToRandom']))
    lineitems.append(str(bestSolution['randomImproved']))

    
    line = ''
    for item in lineitems:
        line = line + item + ';'
    return line

def make_cabecera():
    cabecera = '''Ejemplar;Objetivo;Resultado;Margen Mejora (%);Tiempo ejecución; Método Ordenación;
    Método Colocación; Optimización Local; Número Mejoras; Timeout; WentToRandom; RandomImproved'''.replace('\n','')
    return cabecera



csv_lines = []
csv_lines.append(make_cabecera())

objetivos = get_objetivos()

for fileIndex in range(1,101):
    dataFileExample = 'ejemplar_calibrado_'+str(fileIndex)+'.txt'
    print(dataFileExample)
    bestSolution=completeSolve(dataFileExample)
    checkSolution(dataFileExample,bestSolution)

    csv_line = make_line(dataFileExample,objetivos,bestSolution)
    csv_lines.append(csv_line)


for line in csv_lines:
    print(line)

with open(os.path.join('outputs', 'statics_report'+'.csv'), 'w') as f:
    for line in csv_lines:
        f.write("%s\n" % line)


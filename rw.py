import json
import re
import os

examplesFolder = 'dataExamples'


def pprint(obj):
    # Pretty print json objects

    json_formatted_str = json.dumps(obj, indent=1)
    print(re.sub(r'",\s+', '", ', json_formatted_str))
    return

def readlines(fileName):
    #Array holding text file lines

    lines = []

    with open(os.path.join(examplesFolder, fileName)) as fp:
        for lineNumber, line in enumerate(fp):
            #Append to line array without \n (line break)
            lines.append(line.replace('\n',''))             
    fp.close()

    return lines

def parseLines(lines):
    # Generate data dictionary from lines

    #Dict holding problem data
    data = {}    

    # Extraction: maxTime, numPieces, numMachines operationsByPiece 
    data["maxTime"] = float(lines[0])
    data["numPieces"] = int(lines[1])
    data["numMachines"] = int(lines[2])
    data["operationsByPiece"] = lines[3].split('*')

    # Extraction: Mij, machineByPieceAndOperation
    Mij=[]
    for linesIndex in range(4,4+data["numPieces"]):
        lineSplitted = [float(x) for x in lines[linesIndex].split('*')]
        Mij.append(lineSplitted)
    
    data["machineByPieceAndOperation"] = Mij

    # Extraction: TPij, durationByPieceAndOperation
    TPij=[]
    for linesIndex in range(4+data["numPieces"],4+data["numPieces"]*2):
        lineSplitted = [float(x) for x in lines[linesIndex].split('*')]
        TPij.append(lineSplitted)

    data["durationByPieceAndOperation"] = TPij

    # Extraction: CRi, ruptureCostByPiece
    CRindexLine = 4+data["numPieces"]*2
    CRi=[]
    CRi=lines[CRindexLine].split('*')
    data["ruptureCostByPiece"] = CRi

    # Extraction: TPij, workingCostByPieceAndOperation
    CTEij=[]
    for linesIndex in range(4+data["numPieces"]*2+1,4+data["numPieces"]*3+1):
        lineSplitted = [float(x) for x in lines[linesIndex].split('*')]
        CTEij.append(lineSplitted)

    data["workingCostByPieceAndOperation"] = CTEij
    return data


def getData(fileName):
    lines = readlines(fileName)
    data = parseLines(lines)
    return data

def writeToJson(data):
    # Debugging purposes
    # Writes to data.json file data json dictionary

    f = open("data.json","w")
    f.write( json.dumps(data) )
    f.close()  


data = getData("ejemplar_calibrado_2.txt")
writeToJson(data)
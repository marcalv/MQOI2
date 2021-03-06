from helper import pprint, writeToJson
import os
from math import sqrt

examplesFolder = 'dataExamples'


def readlines(fileName):
    #Array holding text file lines

    lines = []
    
    with open(os.path.join(examplesFolder, fileName)) as fp:
        for line in fp:
            #Append to line array without \n (line break)
            lines.append(line.replace('\n',''))             
    fp.close()

    return lines


def parseLines(lines):
    # Generate data dictionary from lines

    # Dict holding problem data
    data = {}    

    # Extraction: maxTime, numPieces, numMachines operationsByPiece 
    data["maxTime"] = float(lines[0])
    data["numPieces"] = int(lines[1])
    data["numMachines"] = int(lines[2])
    data["operationsByPiece"] = [int(x) for x in lines[3].split('*')]#lines[3].split('*')

    # Extraction: Mij, machineByPieceAndOperation
    Mij=[]
    for linesIndex in range(4,4+data["numPieces"]):
        lineSplitted = [int(x) for x in lines[linesIndex].split('*')]
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
    data["ruptureCostByPiece"] = [float(x) for x in lines[CRindexLine].split('*')]

    # Extraction: TPij, workingCostByPieceAndOperation
    CTEij=[]
    for linesIndex in range(4+data["numPieces"]*2+1,4+data["numPieces"]*3+1):
        lineSplitted = [float(x) for x in lines[linesIndex].split('*')]
        CTEij.append(lineSplitted)

    data["workingCostByPieceAndOperation"] = CTEij
    return data


def calculateExtra(data):
    # Extra calculations associated to data
    
    data["extra"] = {}

    # Calculate: totalPieceDurationByPiece
    durationByPieceAndOperation = []
    for piece in data["durationByPieceAndOperation"]:
        totalPieceDuration = 0
        for operationTime in piece:
            totalPieceDuration = totalPieceDuration + operationTime
        durationByPieceAndOperation.append(totalPieceDuration)
    data["extra"]["totalPieceDurationByPiece"]= durationByPieceAndOperation

    # Calculate: workingCostAverageByPiece
    workingCostAverageByPiece = []
    for piece in data["workingCostByPieceAndOperation"]:
        sumWorkingCost = 0
        for workingCost in piece:
            sumWorkingCost = sumWorkingCost + workingCost
        workingCostAverage = sumWorkingCost/len(piece)
        workingCostAverageByPiece.append(workingCostAverage)
    data["extra"]["workingCostAverageByPiece"]= workingCostAverageByPiece

    # Calculate: workingCostSumByPiece
    workingCostSumByPiece = []
    for piece in data["workingCostByPieceAndOperation"]:
        sumWorkingCost = 0
        for workingCost in piece:
            sumWorkingCost = sumWorkingCost + workingCost
        workingCostSumByPiece.append(sumWorkingCost)
    data["extra"]["workingCostSumByPiece"]= workingCostSumByPiece

    # Calculate: workingCostRMSByPiece
    workingCostRMSByPiece = []
    for piece in data["workingCostByPieceAndOperation"]:
        sumWorkingCost = 0
        for workingCost in piece:
            sumWorkingCost = sumWorkingCost + workingCost*workingCost
        workingCostRMS = sqrt(sumWorkingCost/len(piece))
        workingCostRMSByPiece.append(workingCostRMS)
    data["extra"]["workingCostRMSByPiece"]= workingCostRMSByPiece

    return data

    
def getData(fileName):
    lines = readlines(fileName)
    data = parseLines(lines)
    data = calculateExtra(data)
    return data




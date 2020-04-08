from helper import pprint, writeToJson, dprint
import os 

debug = False

def writeSolution(operationAsignmentByPieceAndOperation,totalCost,folder):
    lines = []
    solIni = str(totalCost)+'*'+'5'
    lines.append(solIni)

    numImprovements = 0
    lines.append(numImprovements)

    bestSolution = str(totalCost)+'*'+'5'
    lines.append(bestSolution)

    for piece in operationAsignmentByPieceAndOperation:
        pieceLine=''
        for operation in piece:
            pieceLine=pieceLine+str(operation['start'])+'*'
        lines.append(pieceLine[:-1])

    with open(os.path.join(folder, 'sol'+'.txt'), 'w') as f:
        for line in lines:
            f.write("%s\n" % line)

    dprint(lines,debug)





from helper import pprint, writeToJson, dprint
import os 

debug = False

def writeSolution(bestSolution,folder,fileName):
    totalCost = bestSolution['totalCost']
    operationAsignmentByPieceAndOperation = bestSolution['operationAsignmentByPieceAndOperation']



    lines = []

    for optimization in bestSolution['log']:
        line = str(optimization['totalCost'])+'*'+str(optimization['time'])
        lines.append(line)
    

    numImprovements = len(bestSolution['log'])-1
    lines.append(numImprovements)


    line = str(bestSolution['totalCost'])+'*'+str(bestSolution['executionTime'])
    lines.append(line)

    for piece in bestSolution['operationAsignmentByPieceAndOperation']:
        pieceLine=''
        for operation in piece:
            pieceLine=pieceLine+str(operation['start'])+'*'
        lines.append(pieceLine[:-1])

    with open(os.path.join(folder, fileName+'.txt'), 'w') as f:
        for line in lines:
            f.write("%s\n" % line)

    dprint(lines,debug)




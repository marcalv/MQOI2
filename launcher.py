from read import getData
from sorting import getPieceOrderBy
from placing import placePieces
from evaluate import calculateCost
from write import writeSolution
from helper import pprint, writeToJson, dprint
import os

debug = True

def checkSolution(dataFileExample,operationAsignmentByPieceAndOperation,totalCost):
    writeSolution(operationAsignmentByPieceAndOperation,totalCost,'tester','sol')
    from shutil import copyfile
    copyfile(os.path.join('dataExamples', dataFileExample), os.path.join('tester', 'data.txt'))

    myCmd = 'cd tester & java TEST_estudiante data.txt sol.txt'
    os.system(myCmd)


def simpleSolve(dataFileExample,sortingMethod,placingMethod):
    
    data = getData(dataFileExample)

    pieceOrder = getPieceOrderBy(data, sortingMethod)

    operationAsignmentByPieceAndOperation = placePieces(data,pieceOrder,placingMethod)

    totalCost = calculateCost(data,operationAsignmentByPieceAndOperation)

    return totalCost, operationAsignmentByPieceAndOperation



def batchSolve(dataFileExample):

    logAllSolutions = False

    bestSolution = {'totalCost': -1 }
    solutionLog = []

    sortingMethods = [
                        'TOTAL_PIECE_DURATION',
                        'TOTAL_PIECE_DURATION_INV',
                        'WORKING_COST_AVERAGE',
                        'WORKING_COST_AVERAGE_INV',
                        'WORKING_COST_SUM',
                        'WORKING_COST_SUM_INV',
                        'WORKING_COST_RMS',
                        'WORKING_COST_RMS_INV',
                        'RUPTURE_COST',
                        'RUPTURE_COST_INV',
                        'NUM_OPERATIONS',
                        'NUM_OPERATIONS_INV',
                        'RANDOM'
                     ]

    placingMethods = [  "END",
                        "SPOT",
                        "END_INV",
                        "SPOT_INV"
                     ]
    
    for sortingMethod in sortingMethods:
        for placingMethod in placingMethods:
            totalCost, operationAsignmentByPieceAndOperation = simpleSolve(dataFileExample,sortingMethod,placingMethod)
            if (bestSolution['totalCost'] == -1) or ( (bestSolution['totalCost'] >= 0) and (bestSolution['totalCost'] > totalCost) ):
                bestSolution = {'totalCost': totalCost, 
                                'sortingMethod':sortingMethod,
                                'placingMethod':placingMethod,
                                'operationAsignmentByPieceAndOperation': operationAsignmentByPieceAndOperation,
                                
                                }
                        
            if logAllSolutions:
                solution = {'totalCost': totalCost, 
                                'operationAsignmentByPieceAndOperation': operationAsignmentByPieceAndOperation,
                                'sortingMethod':sortingMethod,
                                'placingMethod':placingMethod
                                }
                solutionLog.append(solution)
                print('--------')
                print('sortingMethod: '+solution["sortingMethod"])
                print('placingMethod: '+solution["placingMethod"])
                print('totalCost: '+str(solution["totalCost"]))
    

    RANDOM_INTENTS = 100
    for placingMethod in placingMethods:
        for i in range(0,RANDOM_INTENTS):
            totalCost, operationAsignmentByPieceAndOperation = simpleSolve(dataFileExample,'RANDOM',placingMethod)
            if (bestSolution['totalCost'] == -1) or ( (bestSolution['totalCost'] >= 0) and (bestSolution['totalCost'] > totalCost) ):
                    bestSolution = {'totalCost': totalCost, 
                                    'sortingMethod':sortingMethod,
                                    'placingMethod':placingMethod,
                                    'operationAsignmentByPieceAndOperation': operationAsignmentByPieceAndOperation
                                    }
                
    print('')
    print('=======================================')
    print('|||||||||    Best Solution    |||||||||')
    print('=======================================')
    print('sortingMethod: '+bestSolution["sortingMethod"])
    print('placingMethod: '+bestSolution["placingMethod"])
    print('totalCost: '+str(bestSolution["totalCost"]))


    return bestSolution


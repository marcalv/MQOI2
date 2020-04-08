from read import getData
from sorting import getPieceOrderBy
from placing import placePieces
from evaluate import calculateCost
from write import writeSolution
from helper import pprint, writeToJson, dprint
import os

debug = True


def simpleSolve(dataFileExample,sortingMethod,placingMethod):

    
    data = getData(dataFileExample)
    
    pieceOrder = getPieceOrderBy(data, sortingMethod)

    operationAsignmentByMachineAndOperationSorted,operationAsignmentByPieceAndOperation = placePieces(data,pieceOrder,placingMethod)

    totalCost = calculateCost(data,operationAsignmentByMachineAndOperationSorted,operationAsignmentByPieceAndOperation)

    writeSolution(operationAsignmentByPieceAndOperation,totalCost,'tester')



    return


dataFileExample = 'ejemplar_calibrado_56.txt'
sortingMethod = "TOTAL_PIECE_DURATION"
placingMethod = "SPOT"

simpleSolve(dataFileExample,sortingMethod,placingMethod)
from shutil import copyfile
copyfile(os.path.join('dataExamples', dataFileExample), os.path.join('tester', 'data.txt'))

import os
myCmd = 'cd tester & java TEST_estudiante data.txt sol.txt'
os.system(myCmd)
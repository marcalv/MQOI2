from read import getData
from sorting import getPieceOrderBy
from placing import placePieces
from evaluate import calculateCost
from helper import pprint, writeToJson, dprint
import time
import numpy

debug = False
start_time = time.time()

# get data from file
dataFileExample = "ejemplar_calibrado_1.txt"
data = getData(dataFileExample)

# Get Piece Order
pieceOrder = getPieceOrderBy(data, "TOTAL_PIECE_DURATION", True)


# Get schedule
operationAsignmentByMachineAndOperationSorted,operationAsignmentByPieceAndOperation = placePieces(data,pieceOrder)

# calculate cost
totalCost = calculateCost(data,operationAsignmentByMachineAndOperationSorted,operationAsignmentByPieceAndOperation)


print("--- %s seconds ---" % (time.time() - start_time))


writeToJson(operationAsignmentByMachineAndOperationSorted,'resultMachineOperationSorted')
writeToJson(operationAsignmentByPieceAndOperation,'resultPieceOperation')
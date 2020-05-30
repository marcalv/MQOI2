from read import getData
from launcher import simpleSolve, checkSolution, batchSolve
from write import writeSolution


dataFileExample = 'ejemplar_calibrado_1.txt'
bestsolution=batchSolve(dataFileExample)

#checkSolution(dataFileExample,bestsolution['operationAsignmentByPieceAndOperation'],bestsolution['totalCost'])
#writeSolution(bestsolution['operationAsignmentByPieceAndOperation'],bestsolution['totalCost'],'')

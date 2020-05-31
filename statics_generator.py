from read import getData
from launcher import simpleSolve, checkSolution, batchSolve, completeSolve
from write import writeSolution


dataFileExample = 'ejemplar_calibrado_1.txt'
bestSolution=completeSolve(dataFileExample)

checkSolution(dataFileExample,bestSolution)
writeSolution(bestSolution,'outputs','sol')

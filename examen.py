from read import getData
from launcher import  checkSolution, completeSolve
from write import writeSolution
from read import readlines
import os
import sys

num = sys.argv[1]
dataFileExample = 'ejemplar_'+num+'.txt'
print(dataFileExample)
bestSolution=completeSolve(dataFileExample)
checkSolution(dataFileExample,bestSolution)
writeSolution(bestSolution,'final','sol_'+num)
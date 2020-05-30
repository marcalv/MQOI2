from read import getData
from sorting import getPieceOrderBy
from placing import placePieces
from evaluate import calculateCost
from write import writeSolution
from helper import pprint, writeToJson, dprint
import os
from launcher import batchSolve,simpleSolve,checkSolution
import time


dataFileExample = 'ejemplar_calibrado_1.txt'
bestsolution=batchSolve(dataFileExample)

# Calcular el orden de piezas de la solución ganadora
data = getData(dataFileExample)
pieceOrder_0 = getPieceOrderBy(data,bestsolution["sortingMethod"])
totalCost = bestsolution["totalCost"]

#print(pieceOrder)

# Generar nuevos ordenes de piezas

def list_generator(pieceOrder):
    orderList = []

    for longitudCambio in range(0,len(pieceOrder)):
        for i in range(0,len(pieceOrder)-longitudCambio):
            pieceOrderMod = list(pieceOrder)

            pieceOrderMod[i] = pieceOrder[i+longitudCambio]
            pieceOrderMod[i+longitudCambio] = pieceOrder[i]
            orderList.append(pieceOrderMod)
    
    return orderList

optimised = True


def random_mod(pieceOrder):
    import random
    pieceOrderMod = list(pieceOrder)
    random.randint(0, 9)
    pos1 = random.randint(0, len(pieceOrder)-1)
    pos2 = random.randint(0, len(pieceOrder)-1)
    pieceOrderMod[pos1], pieceOrderMod[pos2] = pieceOrderMod[pos2], pieceOrderMod[pos1] 
    return pieceOrderMod


max_fails = 3
fails = 0
pieceOrder_mother = pieceOrder_0
pieceOrder_mother_failed = []
while fails< max_fails:
    optimised = False
    orderList = list_generator(pieceOrder_mother)

    for new_pieceOrder in orderList:
        # Resolver
        new_operationAsignmentByPieceAndOperation = placePieces(data,new_pieceOrder,bestsolution["placingMethod"])
        new_totalCost = calculateCost(data,new_operationAsignmentByPieceAndOperation)

        # Si mejora
        if new_totalCost  < totalCost:
            print('optmized!')
            print(new_totalCost)

            totalCost = new_totalCost
            operationAsignmentByPieceAndOperation = new_operationAsignmentByPieceAndOperation
            best_pieceOrder = new_pieceOrder
            optimised = True 
    
            

    if not optimised:
        if pieceOrder_mother_failed == []:
            print('First No optimized :(')
            pieceOrder_mother_failed = pieceOrder_mother
            #print(pieceOrder_mother_failed)
            pieceOrder_mother = random_mod(pieceOrder_mother_failed)
        else:
            print('No optimized :(')
            pieceOrder_mother = random_mod(pieceOrder_mother_failed)
            #print(pieceOrder_mother)
            fails = fails+1
    else:
        pieceOrder_mother = best_pieceOrder
        pieceOrder_mother_failed = []
        fails = 0
        
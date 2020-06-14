from read import getData
from sorting import getPieceOrderBy
from placing import placePieces
from evaluate import calculateCost
from write import writeSolution
from helper import pprint, writeToJson, dprint
import os
import time
from control_panel import LOCAL_OPT_MAX_FAILS, TIMEOUT,RANDOM_SWITCH

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
    
    #orderList=[pieceOrder] #ELIMINAAAAAAAAAAAAR
    return orderList




def random_mod(pieceOrder):
    import random
    pieceOrderMod = list(pieceOrder)
    pos1 = random.randint(0, len(pieceOrder)-1)
    pos2 = random.randint(0, len(pieceOrder)-1)
    pieceOrderMod[pos1], pieceOrderMod[pos2] = pieceOrderMod[pos2], pieceOrderMod[pos1] 
    return pieceOrderMod




def local_opti(dataFileExample,bestSolution):
    bestSolution['localOpt'] = False

    # Calcular el orden de piezas de la solución ganadora
    data = getData(dataFileExample)

    pieceOrder_mother = getPieceOrderBy(data,bestSolution["sortingMethod"])
    best_totalCost = bestSolution['totalCost']

    max_fails = LOCAL_OPT_MAX_FAILS
    fails = 0
    pieceOrder_mother_failed = []
    timeout = False
    while fails < max_fails:
        

        optimised = False
        orderList = list_generator(pieceOrder_mother)

        for new_pieceOrder in orderList:
            # time control
            #print(time.time() - bestSolution['startTime'])
            if (time.time() - bestSolution['startTime']) > TIMEOUT:
                print('TIMEOUT')
                timeout = True
                break

            # Resolver
            new_operationAsignmentByPieceAndOperation = placePieces(data,new_pieceOrder,bestSolution["placingMethod"])
            new_totalCost = calculateCost(data,new_operationAsignmentByPieceAndOperation)

            # Si mejora
            if new_totalCost  < best_totalCost:
                print('optmized!')
                print(new_totalCost)

                best_totalCost = new_totalCost
                best_operationAsignmentByPieceAndOperation = new_operationAsignmentByPieceAndOperation
                best_pieceOrder = new_pieceOrder
                optimised = True 

                bestSolution['log'].append({'totalCost':best_totalCost,'time':time.time()})
        
        if timeout:
            break            

        if not optimised:
            if pieceOrder_mother_failed == []:
                print('First No optimized :(')
                pieceOrder_mother_failed = pieceOrder_mother
                #print('mother failed')
                #print(pieceOrder_mother_failed)
                #print(pieceOrder_mother_failed)
                pieceOrder_mother = random_mod(pieceOrder_mother_failed)
                #print('new random mother')
                #print(pieceOrder_mother)
            else:
                print('No optimized :(')
                pieceOrder_mother = random_mod(pieceOrder_mother_failed)
                #print('new random mother')
                #print(pieceOrder_mother)
                fails = fails+1
        else:
            pieceOrder_mother = best_pieceOrder
            pieceOrder_mother_failed = []
            fails = 0
    


    
    bestSolution['totalCost'] = best_totalCost
    bestSolution['timeOut'] = timeout

    if len(bestSolution['log'])>1:
        bestSolution['localOpt'] = True
        bestSolution['operationAsignmentByPieceAndOperation'] = best_operationAsignmentByPieceAndOperation
        
    ### Modo Random


    bestSolution['wentToRandom'] = 'No'
    bestSolution['randomImproved'] = '-'
    if RANDOM_SWITCH and not timeout:
        bestSolution['wentToRandom'] = 'Yes'
        bestSolution['randomImproved'] = 'No'
        print('entered in random')
        while True:
            placingMethods = [  "END",
                            "SPOT",
                            "END_INV",
                            "SPOT_INV"
                        ]

            for placingMethod in placingMethods:
                data = getData(dataFileExample)
                pieceOrder = getPieceOrderBy(data, 'RANDOM')
                operationAsignmentByPieceAndOperation = placePieces(data,pieceOrder,placingMethod)
                totalCost = calculateCost(data,operationAsignmentByPieceAndOperation)


                if bestSolution['totalCost'] > totalCost:
                        print(totalCost)
                        bestSolution['randomImproved'] = 'Yes'
                        bestSolution['log'].append({'totalCost':totalCost,'time':time.time()})
                        bestSolution['totalCost'] = totalCost
                        bestSolution['sortingMethod'] = 'RANDOM'
                        bestSolution['placingMethod'] = placingMethod
                        bestSolution['operationAsignmentByPieceAndOperation'] = operationAsignmentByPieceAndOperation
            
            # time control
            #print(time.time() - bestSolution['startTime'])
            if (time.time() - bestSolution['startTime']) > TIMEOUT:
                print('TIMEOUT')
                break
        






    return bestSolution

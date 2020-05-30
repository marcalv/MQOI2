from helper import pprint, writeToJson, dprint

debug = False

def placePieces(data,pieceOrder,method):

    if method == 'END':
        operationAsignmentByPieceAndOperation = placeEnd(data,pieceOrder)
    elif method == 'SPOT':
        operationAsignmentByPieceAndOperation = placeSpot(data,pieceOrder)
    elif method == 'END_INV':
        operationAsignmentByPieceAndOperation = placeINV('END',data,pieceOrder)
    elif method == 'SPOT_INV':
        operationAsignmentByPieceAndOperation = placeINV('SPOT',data,pieceOrder)



    # Trasladar a la izquierda
    marginTime = -1
    rupture = False
    for pieceIdx in range(0,len(operationAsignmentByPieceAndOperation)):
        lastOperation = operationAsignmentByPieceAndOperation[pieceIdx][len(operationAsignmentByPieceAndOperation[pieceIdx])-1]
        if lastOperation['end'] < data["maxTime"]:
            if (marginTime == -1) or (marginTime > (data["maxTime"] - lastOperation['end'])):
                marginTime = data["maxTime"] - lastOperation['end']
        else:
            rupture = True
            break
    
    if (rupture == False) and True:
        # Desplazar todo a la derecha marginTime
        for pieceIdx1 in range(0,len(operationAsignmentByPieceAndOperation)):
            piece = operationAsignmentByPieceAndOperation[pieceIdx1]
            for operationIdx1 in range(0,len(operationAsignmentByPieceAndOperation[pieceIdx1])):
                operation1 = piece[operationIdx1]
                operation1['start']=operation1['start']+marginTime
                operation1['end']=operation1['end']+marginTime 
                

    return operationAsignmentByPieceAndOperation


def initializeSolutionVars(data):
    # Create and initialize operationAsignmentByMachineAndOperationSorted and operationAsignmentByPieceAndOperation that store the solution
    operationAsignmentByMachineAndOperationSorted = [] 
    for machineIdx in range(0,data["numMachines"]):
        operationAsignmentByMachineAndOperationSorted.append([])

    operationAsignmentByPieceAndOperation = []
    for machineIdx in range(0,data["numPieces"]):
        operationAsignmentByPieceAndOperation.append([])
    
    return operationAsignmentByMachineAndOperationSorted,operationAsignmentByPieceAndOperation


def placeEnd(data,pieceOrder):

    operationAsignmentByMachineAndOperationSorted,operationAsignmentByPieceAndOperation = initializeSolutionVars(data)
    
    def add(start,duration,end,piece,operation):
        operationObject = {'start':start, 'duration':duration, 'end':end, 'piece':piece, 'operation':operation}
        operationAsignmentByMachineAndOperationSorted[machineIdx].append(operationObject)
        operationAsignmentByPieceAndOperation[pieceIdx].append(operationObject)

        lastOperationEnd =  operationObject['end']

        return lastOperationEnd

    # Segun el orden de piezas, y por cada operacion en la pieza
    for pieceIdx in pieceOrder:
        lastOperationEnd = 0
        for operationIdx in range(0,len(data['machineByPieceAndOperation'][pieceIdx])):
            machineIdx = data['machineByPieceAndOperation'][pieceIdx][operationIdx] - 1  #machine numbers start on 1, we work from 0
            duration = data['durationByPieceAndOperation'][pieceIdx][operationIdx]

            # Buscar hueco en la maquina
            # =================================
            # Al último hueco

            # Si está vacia
            if operationAsignmentByMachineAndOperationSorted[machineIdx] == []:
                lastOperationEnd = add(lastOperationEnd , duration , lastOperationEnd+duration , pieceIdx , operationIdx)
 
            # Si no esta vacia buscar el ultimo  hueco libre
            else:
                # Ir a la última posición e insertar, si es posible, sino mas tarde
                freeTime = operationAsignmentByMachineAndOperationSorted[machineIdx][len(operationAsignmentByMachineAndOperationSorted[machineIdx])-1]['end']
                if freeTime > lastOperationEnd:
                    start = freeTime
                else:
                    start = lastOperationEnd
                lastOperationEnd = add(start,duration,start+duration,pieceIdx,operationIdx)

    return operationAsignmentByPieceAndOperation



def placeSpot(data,pieceOrder):

    operationAsignmentByMachineAndOperationSorted,operationAsignmentByPieceAndOperation = initializeSolutionVars(data)

    def add(start,duration,end,piece,operation):
        operationObject = {'start':start, 'duration':duration, 'end':end, 'piece':piece, 'operation':operation}
        operationAsignmentByMachineAndOperationSorted[machineIdx].append(operationObject)
        operationAsignmentByPieceAndOperation[pieceIdx].append(operationObject)

        lastOperationEnd =  operationObject['end']

        return lastOperationEnd

    for pieceIdx in pieceOrder:
        lastOperationEnd = 0
        for operationIdx in range(0,len(data['machineByPieceAndOperation'][pieceIdx])):
            machineIdx = data['machineByPieceAndOperation'][pieceIdx][operationIdx] - 1  #machine numbers start on 1, we work from 0
            duration = data['durationByPieceAndOperation'][pieceIdx][operationIdx]

            # Si maquina esta vacia
            if operationAsignmentByMachineAndOperationSorted[machineIdx] == []:
                lastOperationEnd = add(lastOperationEnd , duration , lastOperationEnd+duration , pieceIdx , operationIdx)
            else:
            # si no esta vacia comenzar bucle por operaciones
                #mirar si cabe la primera
                if  duration < operationAsignmentByMachineAndOperationSorted[machineIdx][0]['start']:
                    lastOperationEnd = add(lastOperationEnd , duration , lastOperationEnd+duration , pieceIdx , operationIdx)
                else:
                    for operationInMachine in range(0,len(operationAsignmentByMachineAndOperationSorted[machineIdx])):
                        # si he llegado a la ultima pieza asignada, asigno al final
                        if operationInMachine == len(operationAsignmentByMachineAndOperationSorted[machineIdx])-1:
                            freeTime = operationAsignmentByMachineAndOperationSorted[machineIdx][operationInMachine]['end']
                            if freeTime > lastOperationEnd:
                                start = freeTime
                            else:
                                start = lastOperationEnd
                            lastOperationEnd = add(start,duration,start+duration,pieceIdx,operationIdx)
                            break

                         # si estoy entre medio, y la pieza que miro acaba antes de lo que necesito
                        startFreeSpace = operationAsignmentByMachineAndOperationSorted[machineIdx][operationInMachine]['end']
                        endFreeSpace = operationAsignmentByMachineAndOperationSorted[machineIdx][operationInMachine+1]['start']
                        freeSpace = endFreeSpace - startFreeSpace
                        if (lastOperationEnd <= startFreeSpace) and (freeSpace >= duration):
                            lastOperationEnd = add(startFreeSpace,duration,startFreeSpace+duration,pieceIdx,operationIdx)
                            break
                        elif (lastOperationEnd >= startFreeSpace) and (freeSpace-lastOperationEnd >= duration):
                            lastOperationEnd = add(lastOperationEnd,duration,lastOperationEnd+duration,pieceIdx,operationIdx)
                            break

        
            

    dprint(operationAsignmentByMachineAndOperationSorted,debug)
    
    return operationAsignmentByPieceAndOperation


def placeINV(placingMethod,data,pieceOrder):
    #1 Invertir orden operaciones en machineByPieceAndOperation y durationByPieceAndOperation
    for piece in range(0,data['numPieces']):
        data['durationByPieceAndOperation'][piece] = list(reversed(data['durationByPieceAndOperation'][piece]))
        data['machineByPieceAndOperation'][piece] = list(reversed(data['machineByPieceAndOperation'][piece]))

    #2 Ordernar con last
    if placingMethod == 'END':
        operationAsignmentByPieceAndOperation = placeEnd(data,pieceOrder)
    elif placingMethod == 'SPOT':
        operationAsignmentByPieceAndOperation = placeSpot(data,pieceOrder)

    #3 Pivotar 
    lowestStart = 1
    for pieceIdx in range(0,data['numPieces']):
        piece = operationAsignmentByPieceAndOperation[pieceIdx]
        for operationIdx in range(0,len(piece)):
            operation = piece[operationIdx]
            pivotTime = operation['duration'] + 2*operation['start']
            operation['start']=operation['start']-pivotTime
            operation['end']=operation['end']-pivotTime
            if ((lowestStart==1) or (lowestStart>operation['start'])):
                lowestStart = operation['start']

    # trasladar a 0
    for pieceIdx in range(0,data['numPieces']):
        piece = operationAsignmentByPieceAndOperation[pieceIdx]
        for operationIdx in range(0,len(piece)):
            operation = piece[operationIdx]
            operation['start']=operation['start']-lowestStart
            operation['end']=operation['end']-lowestStart
            operation['operation']=len(piece)-operationIdx-1     # Invertir operacion
    
    # Reordenar array
    for pieceIdx in range(0,data['numPieces']):
        operationAsignmentByPieceAndOperation[pieceIdx] = list(reversed(operationAsignmentByPieceAndOperation[pieceIdx]))

    return operationAsignmentByPieceAndOperation



""" 
from read import getData
from sorting import getPieceOrderBy
from evaluate import calculateCost

sortingMethod='TOTAL_PIECE_DURATION'
placingMethod='SPOT_INV'
dataFileExample='001_easy.txt'


data = getData(dataFileExample)

pieceOrder = getPieceOrderBy(data, sortingMethod)

operationAsignmentByPieceAndOperation = placePieces(data,pieceOrder,placingMethod)

totalCost = calculateCost(data,operationAsignmentByPieceAndOperation)


 """
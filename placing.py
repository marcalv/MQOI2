from helper import pprint, writeToJson, dprint

debug = False

def initializeSolutionVars(data):
    # Create and initialize operationAsignmentByMachineAndOperationSorted and operationAsignmentByPieceAndOperation that store the solution
    operationAsignmentByMachineAndOperationSorted = [] 
    for machineIdx in range(0,data["numMachines"]):
        operationAsignmentByMachineAndOperationSorted.append([])

    operationAsignmentByPieceAndOperation = []
    for machineIdx in range(0,data["numPieces"]):
        operationAsignmentByPieceAndOperation.append([])
    
    return operationAsignmentByMachineAndOperationSorted,operationAsignmentByPieceAndOperation

def placePieces(data,pieceOrder,method):

    if method == 'END':
        operationAsignmentByMachineAndOperationSorted,operationAsignmentByPieceAndOperation = placeEnd(data,pieceOrder)
    elif method == 'SPOT':
        operationAsignmentByMachineAndOperationSorted,operationAsignmentByPieceAndOperation = placeSpot(data,pieceOrder)

    return operationAsignmentByMachineAndOperationSorted,operationAsignmentByPieceAndOperation


def placeEnd(data,pieceOrder):

    operationAsignmentByMachineAndOperationSorted,operationAsignmentByPieceAndOperation = initializeSolutionVars(data)
    
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
                #A signar lo antes posible,  INICIO NO (expecto si es la primera operacion)
                operationObject = {'start':lastOperationEnd, 'duration':duration, 'end':lastOperationEnd+duration, 'piece':pieceIdx, 'operation':operationIdx}
                operationAsignmentByMachineAndOperationSorted[machineIdx].append(operationObject)
                operationAsignmentByPieceAndOperation[pieceIdx].append(operationObject) 
            # Si no esta vacia buscar el ultimo  hueco libre
            else:
                # Ir a la última posición e insertar, si es posible, sino mas tarde
                freeTime = operationAsignmentByMachineAndOperationSorted[machineIdx][len(operationAsignmentByMachineAndOperationSorted[machineIdx])-1]['end']
                if freeTime > lastOperationEnd:
                    start = freeTime
                else:
                    start = lastOperationEnd
                operationObject = {'start':start, 'duration':duration, 'end':start+duration, 'piece':pieceIdx, 'operation':operationIdx}
                operationAsignmentByMachineAndOperationSorted[machineIdx].append(operationObject)
                operationAsignmentByPieceAndOperation[pieceIdx].append(operationObject)

            lastOperationEnd =  operationObject['end']

    return operationAsignmentByMachineAndOperationSorted,operationAsignmentByPieceAndOperation



def placeSpot(data,pieceOrder):
    operationAsignmentByMachineAndOperationSorted,operationAsignmentByPieceAndOperation = initializeSolutionVars(data)

    for pieceIdx in pieceOrder:
        lastOperationEnd = 0
        for operationIdx in range(0,len(data['machineByPieceAndOperation'][pieceIdx])):
            machineIdx = data['machineByPieceAndOperation'][pieceIdx][operationIdx] - 1  #machine numbers start on 1, we work from 0
            duration = data['durationByPieceAndOperation'][pieceIdx][operationIdx]

            # Si maquina esta vacia
            if operationAsignmentByMachineAndOperationSorted[machineIdx] == []:
                operationObject = {'start':lastOperationEnd, 'duration':duration, 'end':lastOperationEnd+duration, 'piece':pieceIdx, 'operation':operationIdx}
                operationAsignmentByMachineAndOperationSorted[machineIdx].append(operationObject)
                operationAsignmentByPieceAndOperation[pieceIdx].append(operationObject) 
            else:
            # si no esta vacia comenzar bucle por operaciones
                #mirar si cabe la primera
                if  duration < operationAsignmentByMachineAndOperationSorted[machineIdx][0]['start']:
                    operationObject = {'start':lastOperationEnd, 'duration':duration, 'end':lastOperationEnd+duration, 'piece':pieceIdx, 'operation':operationIdx}
                    operationAsignmentByMachineAndOperationSorted[machineIdx].insert(0,operationObject)
                    operationAsignmentByPieceAndOperation[pieceIdx].append(operationObject)
                else:
                    for operationInMachine in range(0,len(operationAsignmentByMachineAndOperationSorted[machineIdx])):
                        # si he llegado a la ultima pieza asignada, asigno al final
                        if operationInMachine == len(operationAsignmentByMachineAndOperationSorted[machineIdx])-1:
                            freeTime = operationAsignmentByMachineAndOperationSorted[machineIdx][operationInMachine]['end']
                            if freeTime > lastOperationEnd:
                                start = freeTime
                            else:
                                start = lastOperationEnd
                            operationObject = {'start':start, 'duration':duration, 'end':start+duration, 'piece':pieceIdx, 'operation':operationIdx}
                            operationAsignmentByMachineAndOperationSorted[machineIdx].append(operationObject)
                            operationAsignmentByPieceAndOperation[pieceIdx].append(operationObject)
                            break

                         # si estoy entre medio, y la pieza que miro acaba antes de lo que necesito
                        startFreeSpace = operationAsignmentByMachineAndOperationSorted[machineIdx][operationInMachine]['end']
                        endFreeSpace = operationAsignmentByMachineAndOperationSorted[machineIdx][operationInMachine+1]['start']
                        freeSpace = endFreeSpace - startFreeSpace
                        if (lastOperationEnd <= startFreeSpace) and (freeSpace >= duration):
                                operationObject = {'start':startFreeSpace, 'duration':duration, 'end':startFreeSpace+duration, 'piece':pieceIdx, 'operation':operationIdx}
                                operationAsignmentByMachineAndOperationSorted[machineIdx].insert(operationInMachine+1,operationObject)
                                operationAsignmentByPieceAndOperation[pieceIdx].append(operationObject) 
                                break
                        elif (lastOperationEnd >= startFreeSpace) and (freeSpace-lastOperationEnd >= duration):
                                operationObject = {'start':lastOperationEnd, 'duration':duration, 'end':lastOperationEnd+duration, 'piece':pieceIdx, 'operation':operationIdx}
                                operationAsignmentByMachineAndOperationSorted[machineIdx].insert(operationInMachine+1,operationObject)
                                operationAsignmentByPieceAndOperation[pieceIdx].append(operationObject)
                                break

        
            lastOperationEnd =  operationObject['end']

    dprint(operationAsignmentByMachineAndOperationSorted,debug)
    
    return operationAsignmentByMachineAndOperationSorted,operationAsignmentByPieceAndOperation


from helper import pprint, writeToJson, dprint


def initializeSolutionVars(data):
    # Create and initialize operationAsignmentByMachineAndOperationSorted and operationAsignmentByPieceAndOperation that store the solution
    operationAsignmentByMachineAndOperationSorted = [] 
    for machineIdx in range(0,data["numMachines"]):
        operationAsignmentByMachineAndOperationSorted.append([])

    operationAsignmentByPieceAndOperation = []
    for machineIdx in range(0,data["numPieces"]):
        operationAsignmentByPieceAndOperation.append([])
    
    return operationAsignmentByMachineAndOperationSorted,operationAsignmentByPieceAndOperation

def placePieces(data,pieceOrder):
    
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
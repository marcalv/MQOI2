from helper import dprint

debug = False

def calculateShippingTime(data,operationAsignmentByPieceAndOperation):
    # Calcular  fecha  de entrega
    shippingTime = data["maxTime"]
    for pieceIdx in range(0,len(operationAsignmentByPieceAndOperation)):
        lastOperation = operationAsignmentByPieceAndOperation[pieceIdx][len(operationAsignmentByPieceAndOperation[pieceIdx])-1]
        if lastOperation['end'] > shippingTime:
            shippingTime = lastOperation['end']
    
    return shippingTime

def calculateCost(data,operationAsignmentByPieceAndOperation):

    shippingTime = calculateShippingTime(data,operationAsignmentByPieceAndOperation)

    #Working Cost
    acumulatedWorkingCost = 0
    for pieceIdx in range(0,len(operationAsignmentByPieceAndOperation)):
        piece = operationAsignmentByPieceAndOperation[pieceIdx]
        for operationIdx in range(0,len(piece)):
            operation = piece[operationIdx]
            # Si es la última operación
            if operation['operation'] == (data['operationsByPiece'][operation['piece']] - 1):
                operationWorkingTime = shippingTime - operation['end']
            else:
                operationWorkingTime = piece[operationIdx + 1]['end'] - operation['end']
            
            operationWorkingCost = operationWorkingTime * data['workingCostByPieceAndOperation'][pieceIdx][operationIdx]
            acumulatedWorkingCost = acumulatedWorkingCost + operationWorkingCost
            dprint('Tiempo de trabajo pieza '+str(pieceIdx)+str(operationIdx)+' = '+str(operationWorkingTime),debug)

    dprint('workingCost: '+str(acumulatedWorkingCost),debug)

    if shippingTime > data["maxTime"]:
        # Rupture Cost
        acumulatedRuptureCost = 0
        for pieceIdx in range(0,len(operationAsignmentByPieceAndOperation)):
            ruptureTime = shippingTime - data["maxTime"]
            ruptureCost = ruptureTime * data['ruptureCostByPiece'][pieceIdx]
            acumulatedRuptureCost = acumulatedRuptureCost + ruptureCost
            dprint('Tiempo de ruptura pieza '+str(pieceIdx)+' = '+str(ruptureTime),debug)
    else:
        acumulatedRuptureCost = 0

    dprint('ruptureCost: '+str(acumulatedRuptureCost),debug)

    totalCost = acumulatedWorkingCost + acumulatedRuptureCost

    return totalCost



def getPieceOrderBy(data, order, reverse):
    # Total duration: Order by totalPieceDurationByPiece
    # reverse: True (high to low)
    if order == "TOTAL_PIECE_DURATION":
        pieceOrder = getIndexSorted(data["extra"]['totalPieceDurationByPiece'],reverse)
    
    elif order == "WORKING_COST_AVERAGE":
        pieceOrder = getIndexSorted(data["extra"]['workingCostAverageByPiece'],reverse)
    
    return pieceOrder


def getIndexSorted(array,reverse):
    #Convert list into list of json objects that contain same values and position in array
    indexedList = []
    for piece, value in enumerate(array):
        obj = {'value':value, 'piece':piece}
        indexedList.append(obj)
    
    #Sort indexedList
    dataSorted = sorted(indexedList, key=lambda x : x["value"], reverse=reverse)

    #Extract index previously generated from the sorted array.
    pieceOrder=[]
    for item in dataSorted:
        pieceOrder.append(item["piece"])

    return pieceOrder
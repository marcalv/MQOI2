from helper import dprint

debug=False

def getPieceOrderBy(data, order):
    # Total duration: Order by totalPieceDurationByPiece
    # reverse: True (high to low)
    if order[-4:] == "_INV":
        reverse = False
        order = order[:-4]
    else:
        reverse = True

    

    if order == "TOTAL_PIECE_DURATION":
        pieceOrder = getIndexSorted(data["extra"]['totalPieceDurationByPiece'],reverse)
    
    elif order == "WORKING_COST_AVERAGE":
        pieceOrder = getIndexSorted(data["extra"]['workingCostAverageByPiece'],reverse)


    dprint('pieceOrder: '+str(pieceOrder),debug)
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
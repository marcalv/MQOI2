from rw import getData
from sorting import getPieceOrderBy


# txt file to open
dataFileExample = "ejemplar_calibrado_1.txt"
# get data from file
data = getData(dataFileExample)

# Get piece order by TOTAL_PIECE_DURATION or WORKING_COST_AVERAGE ascending or descending
pieceOrder1 = getPieceOrderBy(data, "TOTAL_PIECE_DURATION", True)
pieceOrder2 = getPieceOrderBy(data, "TOTAL_PIECE_DURATION", False)
pieceOrder3 = getPieceOrderBy(data, "WORKING_COST_AVERAGE", True)
pieceOrder4 = getPieceOrderBy(data, "WORKING_COST_AVERAGE", False)
print(pieceOrder1)
print(pieceOrder2)
print(pieceOrder3)
print(pieceOrder4)
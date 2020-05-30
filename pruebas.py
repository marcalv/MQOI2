



pieceOrder = [1,2,3,4,5,6,7]

import random
pieceOrderMod = list(pieceOrder)
random.randint(0, 9)
pos1 = random.randint(0, len(pieceOrder)-1)
pos2 = random.randint(0, len(pieceOrder)-1)
pieceOrderMod[pos1], pieceOrderMod[pos2] = pieceOrderMod[pos2], pieceOrderMod[pos1] 

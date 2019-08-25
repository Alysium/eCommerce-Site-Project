#Note: Currently not in use, for reference

def loopCalculator (totalLength, elementsPerRow):
	indexSize = totalLength - 1
	remainder = indexSize % elementsPerRow
	quotient = indexSize - remainder
	looped = (quotient / elementsPerRow)+1	
	return looped
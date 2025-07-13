
# custom data structure to hold the state of a Canny edge filter
class EdgeFilter:

    def __init__(self, kernelSize=5, erodeIter=None, dilateIter=2, canny1=200,
                    canny2=500):
        self.kernelSize = kernelSize
        self.erodeIter = erodeIter
        self.dilateIter = dilateIter
        self.canny1 = canny1
        self.canny2 = canny2
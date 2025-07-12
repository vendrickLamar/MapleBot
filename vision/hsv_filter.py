class HsvFilter:

    def __init__(self, h_min=None, s_min=None, v_min=None, h_max=None, s_max=None, v_max=None,
                 s_add=None, s_sub=None, v_add=None, v_sub=None):
        self.hMin = h_min
        self.sMin = s_min
        self.vMin = v_min
        self.hMax = h_max
        self.sMax = s_max
        self.vMax = v_max
        self.sAdd = s_add
        self.sSub = s_sub
        self.vAdd = v_add
        self.vSub = v_sub
# -*- coding: utf-8 -*-
"""
Modified by Group 04
"""

import random
import time
from halma_player import HalmaPlayer

class HalmaPlayer01(HalmaPlayer):

    def __init(self, nama):
        super().__init__(nama)

    # Called API for model
    # Return: (selected final position, initial position, action type)
    def main(self, model):
        time_mulai = time.process_time()
        
        # Dummy algorithm to simulate time
        a = 0
        for i in range(0,10000000):
            a += i
        
        # Random seed for pseudorandom select
        seed1 = random.sample(range(10,1000), 20)
        random.seed(random.choice(seed1))

        # Pick random move choice
        l = []
        g = []
        papan = model.getPapan()        
        b0 = model.getPosisiBidak(self.index)
        while l == [] or g == []:
            b = random.choice(b0)
            # Calculate move possibilities
            g,l = self.bisaMain(model, papan, b[0], b[1])
        
        print('algorithm time: ', time.process_time()-time_mulai)
        
        # Return move
        # LONCAT
        if l != []:
            return [l[0]], b, model.A_LONCAT

        # GESER
        elif g != []:
            return g, b, model.A_GESER
        
        # If no move left (BERHENTI)
        return None, None, model.A_BERHENTI
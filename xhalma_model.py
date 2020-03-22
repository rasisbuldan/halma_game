# -*- coding: utf-8 -*-
"""

Halma

@author: Mursito
"""

from halma_model import HalmaModel

model = HalmaModel()

model.awal(0,0)

p = model.getPapan()

print("PAPAN---------------------------")
print(p)

b0 = model.getPosisiBidak(1)
print("POSISI BIDAK---------------------------")
print(b0)

for b in b0:
    print("BIDAK: ", model.getBidak(b[0], b[1]), b, "----------------")
    g,l = model.bisaMain(b[0], b[1])
    print("Geser : ", g)
    print("Loncat: ", l)


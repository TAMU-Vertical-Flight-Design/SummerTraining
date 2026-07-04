
$ python Gianna/week_4_training_Gianna.py
=============================================
# Wing Optimization Results
```
=============================================
Wing optimization Results 1 
=============================================
Span: 20.00 m
Root chord: 0.30 m
Tip chord: 0.21 m
Taper ratio: 0.710
Tip twist: -6.45 deg
Wing area: 5.13 m²
Aspect ratio: 77.99

New CL: 0.5934
New CD (induced): 0.0017
New L/D:  356.03
=============================================
```

# Wing Optimization Results
```
=============================================
Wing Optimization Results 2
=============================================
Span: 25.00 m
Root chord: 0.30 m
Tip chord: 0.18 m
Taper ratio: 0.600
Tip twist: -10.00 deg
Wing area: 6.00 m²
Aspect ratio: 104.17

New CL: 0.6049
New CD (induced): 0.0018
New L/D:  337.12
=============================================
```

Paragraph on what I learned: 
The taper is the ratio of the tip cord to the root cord end of the propeller blade, and having a lower taper causes a more rectangular wing. The optimization compensated for this by making the tip cord smaller so it actually made the wing area smaller. The optimization will always opt for a longer span and a more narrow wing with less area. This is more aerodynamically favorable because there is less drag with this design and it takes less energy to manipulate the air around them giving a better L/D ratio. The VLM is a mesh of panels that break down the provided shape to give an accurate analysis on the physics acting on the shape given the input of the shape and environment. If you give it too few panels like 6 for example you will get very inaccurate results, but if you give it 24 you get more accurate results but the simulation takes forever to process. When I changed the objective from minimizing (-CL/CD) to just CD the simulation reduced the CD by twisting the tip to the max allowance. By doing that it reduced the lift significantly, but lift wasn’t a priority as long as the CD was improved. Overall it created a worse wing with a worse L/D ratio. Telling the optimizer what the objective is is a key determinant on the quality of the output. I also learned that CTRL + Z is the most useful command there is. 
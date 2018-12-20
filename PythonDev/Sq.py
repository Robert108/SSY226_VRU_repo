# takes the quaterion and calcualte the derivative of the quaternions

import numpy as np

def Sq(q):
    # The matrix S(q)
    q0=q[0,0]
    q1=q[1,0]
    q2=q[2,0]
    q3=q[3,0]

    S=np.array([[-q1, -q2, -q3],
       [q0, -q3,  q2],
       [q3,  q0, -q1],
       [-q2,  q1,  q0]])

    return S

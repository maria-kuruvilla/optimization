"""
goal - to formulate a cplex optimization problem for optimal threshold for fish
"""

import numpy as np

#parameters

n = 3 # number of fish
a = 5 #mean of threat curve
b = 6 #mean of non threat curve
a1 = 3.5
a2 = 6.5
b1 = 2.5
b2 = 5.5
m = -1/3
c1 = 6.5/3
c2 = 5.5/3
alpha = 0.5
action = [1,0]
binary = '0' + str(n) + 'b'
possibilities = 2**n

#formulation 

objective1 = ''
objective2 = ''
nonlinear = []
poss =[]

for i in range(n):
    nonlinear.append('k1_1_' + str(i+1) +': t_' + str(i+1) +' - 6 k_1_' + str(i+1) +' <= ' + str(a1) )
    nonlinear.append('k1_2_' + str(i+1) +': t_' + str(i+1) +' - ' + str(a1) +' k_1_' + str(i+1) +' > 0')
    nonlinear.append('k2_1_' + str(i+1) +': t_' + str(i+1) +' - 6 k_2_' + str(i+1) +' < ' + str(a2) )
    nonlinear.append('k2_2_' + str(i+1) +': t_' + str(i+1) +' - ' + str(a2) +' k_2_' + str(i+1) +' >= 0')
    nonlinear.append('psecond1_' + str(i+1) +': p_' + str(i+1) +' + ' + str(-m) + ' t_' + str(i+1) +' + 3 k_1_' + str(i+1) +' - 3 k_2_' + str(i+1) +' <= ' + str(c1 + 3) )
    nonlinear.append('psecond2_' + str(i+1) +': p_' + str(i+1) +' + ' + str(-m) +' t_' + str(i+1) +' - 3 k_1_' + str(i+1) +' + 3 k_2_' + str(i+1) +' >= ' + str(c1 - 3) )
    nonlinear.append('pthird1_' + str(i+1) +': p_' + str(i+1) +' + k_1_' + str(i+1) +' + k_2_' + str(i+1) +' <= 2')
    nonlinear.append('pthird2_' + str(i+1) +': p_' + str(i+1) +' - k_1_' + str(i+1) +' - k_2_' + str(i+1) +' >= -2')
    nonlinear.append('pfirst1_' + str(i+1) +': p_' + str(i+1) +' + k_1_' + str(i+1) +' + k_2_' + str(i+1) +' >= 1')
    nonlinear.append('pfirst2_' + str(i+1) +': p_' + str(i+1) +' <= 1')

    nonlinear.append('k3_1_' + str(i+1) +': t_' + str(i+1) +' - 6 k_3_' + str(i+1) +' <= ' + str(b1) )
    nonlinear.append('k3_2_' + str(i+1) +': t_' + str(i+1) +' - ' + str(b1) +' k_3_' + str(i+1) +' > 0')
    nonlinear.append('k4_1_' + str(i+1) +': t_' + str(i+1) +' - 6 k_4_' + str(i+1) +' < ' + str(b2) )
    nonlinear.append('k4_2_' + str(i+1) +': t_' + str(i+1) +' - ' + str(b2) +' k_4_' + str(i+1) +' >= 0')
    nonlinear.append('qsecond1_' + str(i+1) +': q_' + str(i+1) +' + ' + str(-m) +' t_' + str(i+1) +' + 2.5 k_3_' + str(i+1) +' - 2.5 k_4_' + str(i+1) +' <= ' + str(c2 + 2.5) )
    nonlinear.append('qsecond2_' + str(i+1) +': q_' + str(i+1) +' + ' + str(-m) +' t_' + str(i+1) +' - 2.5 k_3_' + str(i+1) +' + 2.5 k_4_' + str(i+1) +' >= ' + str(c2 - 2.5) )
    nonlinear.append('qthird1_' + str(i+1) +': q_' + str(i+1) +' + k_3_' + str(i+1) +' + k_4_' + str(i+1) +' <= 2')
    nonlinear.append('qthird2_' + str(i+1) +': q_' + str(i+1) +' - k_3_' + str(i+1) +' - k_4_' + str(i+1) +' >= -2')
    nonlinear.append('qfirst1_' + str(i+1) +': q_' + str(i+1) +' + k_3_' + str(i+1) +' + k_4_' + str(i+1) +' >= 1')
    nonlinear.append('qfirst2_' + str(i+1) +': q_' + str(i+1) +' <= 1')

    nonlinear.append('threshold_' + str(i+1) +': t_' + str(i+1) +' <= 6')





"""
k1_2 = 
k2_1 = 
k2_2 = 
psecond1 = 
psecond2 = 
pthird1 =
pthird2 = 
pfirst1 = 
pfirst2 = 
    nonlinear.append('k1_1: t - 6 k_1 <= 4')
    nonlinear.append('k1_2: t - 4 k_1 > 0')
    nonlinear.append('k2_1: t - 6 k_2 < 6')
    nonlinear.append('k2_2: t - 6 k_2 >= 0')
    nonlinear.append('psecond1: p + 0.5 t + 3 k_1 - 3 k_2 <= 6')
    nonlinear.append('psecond2: p + 0.5t - 3 k_1 + 3 k_2 >= 0')
    nonlinear.append('pthird1: p + k_1 + k_2 <= 2')
    nonlinear.append('pthird2: p - k_1 - k_2 >= -2')
    nonlinear.append('pfirst1: p + k_1 + k_2 >= 1')
    nonlinear.append('pfirst2: p <= 1')

    nonlinear.append('k3_1: t - 6 k_3 <= 3')
    nonlinear.append('k3_2: t - 3 k_3 > 0')
    nonlinear.append('k4_1: t - 6 k_4 < 5')
    nonlinear.append('k4_2: t - 5 k_4 >= 0')
    nonlinear.append('qsecond1: q + 0.5 t + 2.5 k_3 - 2.5 k_4 <= 5')
    nonlinear.append('qsecond2: q + 0.5t - 2.5 k_3 + 2.5 k_4 >= 0')
    nonlinear.append('qthird1: q + k_3 + k_4 <= 2')
    nonlinear.append('qthird2: q - k_3 - k_4 >= -2')
    nonlinear.append('qfirst1: q + k_3 + k_4 >= 1')
    nonlinear.append('qfirst2: q <= 1')

    nonlinear.append('threshold: t <= 6')


"""
for i in range(n):
    objective1 += ' + ' + str(alpha) + ' p_' + str(i+1) + ' - ' + str(1-alpha) + ' q_' + str(i+1)

for i in range(possibilities):
    poss.append(str(format(i,binary)))
    w = 0
    for j in range(n):
        w += int(format(i,binary)[j])
    c1 = 2 * (n-w)/n 
    c2 = w/n   
    objective2 += ' + ' + str(c1) + ' y_' + str(format(i,binary)) + ' + ' + str(c2) + ' z_' + str(format(i,binary))  +'\r\n'



sum_y = 'sum_y: '
sum_z = 'sum_z: '
for i in range(len(poss)):
    
    if i == (len(poss) - 1):
        sum_y += ' + ' + 'y_' + poss[i] + ' = 1'
        sum_z += ' + ' + 'z_' + poss[i] + ' = 1'
    else :
        sum_y += ' + ' + 'y_' + poss[i] 
        sum_z += ' + ' + 'z_' + poss[i] 
   

pconstraint = []
qconstraint = []

for j in range(n):
    pi = 'p' + str(j+1) +': '
    qi = 'q' + str(j+1) +': '
    for i in range(len(poss)):
        if i == (len(poss)-1):
            if poss[i][j] == '1':
                pi += ' + ' + 'y_' + poss[i] + ' - p_' + str(j+1) + ' = 0'
                qi += ' + ' + 'z_' + poss[i] + ' - q_' + str(j+1) + ' = 0'
        else:
            if poss[i][j] == '1':
                pi += ' + ' + 'y_' + poss[i] 
                qi += ' + ' + 'z_' + poss[i] 



        
    pconstraint.append(pi)
    qconstraint.append(qi)


    


# print
text_file = open("../../output/optimization/Output_project.cpx", "w")
text_file.writelines(['MIN','\r\n','OBJECTIVE:','\r\n',objective2,'\r\n','\r\n','Subject To:','\r\n'])
for i in range(len(nonlinear)):
    text_file.writelines([nonlinear[i],'\r\n'])
for i in range(len(pconstraint)):
    text_file.writelines([pconstraint[i],'\r\n'])
for i in range(len(qconstraint)):
    text_file.writelines([qconstraint[i],'\r\n'])

text_file.writelines([sum_y,'\r\n'])
text_file.writelines([sum_z,'\r\n'])
text_file.writelines(['Binary','\r\n'])
for i in range(n):
    text_file.writelines(['k_1_' + str(i+1),'\r\n','k_2_' + str(i+1),'\r\n','k_3_' + str(i+1),'\r\n','k_4_' + str(i+1),'\r\n'])

text_file.writelines(['\r\n','End'])

text_file.close()

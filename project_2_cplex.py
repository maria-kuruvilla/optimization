"""
goal - to formulate the updated cplex optimization problem for optimal threshold for fish
"""

import numpy as np
import math

#parameters

n = 3 # number of fish
a = 5 #mean of threat curve
b = 4 #mean of non threat curve

tau = np.linspace(2,6,41)


possibilities = 2**n

kp_list = []
k_list = []
kq_list = []

for j in range(n):
    count = 1
    p_i_tau = []
    q_i_tau = []
    kp = ''
    k = ''
    kq = ''

    for i in np.linspace(2,6,41):
        i = round(i,1)
        if (count%5 == 0):
            p_i_tau.append(round(1-0.5*(1+math.erf((i-5)/np.sqrt(2))),2))
            q_i_tau.append(round(1-0.5*(1+math.erf((i-4)/np.sqrt(2))),2))
            k +=  'k_' + str (j+1) + '_' + str(i) + '+' + '\r\n'
            kp +=  str(p_i_tau[count -1]) + 'k_' + str (j+1) + '_' + str(i) + ' + ' + '\r\n'
            kq +=  str(q_i_tau[count -1]) + 'k_' + str (j+1) + '_' + str(i) + ' + ' + '\r\n'
        if (i == 6):
            p_i_tau.append(round(1-0.5*(1+math.erf((i-5)/np.sqrt(2))),2))
            q_i_tau.append(round(1-0.5*(1+math.erf((i-4)/np.sqrt(2))),2))
            k +=  'k_' + str (j+1) + '_' + str(i) + ' = 1'
            kp +=  str(p_i_tau[count -1]) + 'k_' + str (j+1) + '_' + str(i)  + ' - p_' + str(j+1) + ' = 0'
            kq +=  str(q_i_tau[count -1]) + 'k_' + str (j+1) + '_' + str(i)  + ' - q_' + str(j+1) + ' = 0'
        else:
            p_i_tau.append(round(1-0.5*(1+math.erf((i-5)/np.sqrt(2))),2))
            q_i_tau.append(round(1-0.5*(1+math.erf((i-4)/np.sqrt(2))),2))
            k +=  'k_' + str (j+1) + '_' + str(i) + ' + '
            kp +=  str(p_i_tau[count -1]) + 'k_' + str (j+1) + '_' + str(i) + ' + ' 
            kq +=  str(q_i_tau[count -1]) + 'k_' + str (j+1) + '_' + str(i) + ' + ' 

        count += 1
    k_list.append(k)
    kp_list.append(kp)
    kq_list.append(kq)


    
objective1 = ''
objective2 = ''
binary = '0' + str(n) + 'b'
poss =[]
alpha = 0.5


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


    




"""
    if (count%5 == 0):
        p_i_tau.append(1-0.5*(1+math.erf((i-5)/np.sqrt(2))))
        q_i_tau.append(1-0.5*(1+math.erf((i-4)/np.sqrt(2))))
        kp +=  'k_i_' + str(i) + '+' + '\r\n'
    if (i == 6):
        p_i_tau.append(1-0.5*(1+math.erf((i-5)/np.sqrt(2))))
        q_i_tau.append(1-0.5*(1+math.erf((i-4)/np.sqrt(2))))
        kp +=  'k_i_' + str(i) + ' = 1'
    else:
        p_i_tau.append(1-0.5*(1+math.erf((i-5)/np.sqrt(2))))
        q_i_tau.append(1-0.5*(1+math.erf((i-4)/np.sqrt(2))))
        kp +=  'k_i_' + str(i) + '+'


"""

# print
text_file = open("../../output/optimization/Output_project_2.cpx", "w")
text_file.writelines(['MIN','\r\n','OBJECTIVE:','\r\n',objective2,'\r\n','\r\n','Subject To:','\r\n'])

for i in range(len(pconstraint)):
    text_file.writelines([pconstraint[i],'\r\n'])
for i in range(len(qconstraint)):
    text_file.writelines([qconstraint[i],'\r\n'])

text_file.writelines([sum_y,'\r\n'])
text_file.writelines([sum_z,'\r\n'])
for i in range(n):
    text_file.writelines([k_list[i],'\r\n'])
    text_file.writelines([kp_list[i],'\r\n'])
    text_file.writelines([kq_list[i],'\r\n'])

text_file.writelines(['Binary','\r\n'])
for j in range(n):
    for i in np.linspace(2,6,41):
        i = round(i,1)
        text_file.writelines(['k_' + str (j+1) + '_' + str(i),'\r\n'])


text_file.writelines(['\r\n','End'])

text_file.close()



    


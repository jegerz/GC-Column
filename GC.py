
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time

import streamlit as st
import time
import matplotlib.pyplot as plt





def initialization(sol,Mol_Num,Plate_num):
    Gas_phase =[]
    Liq_phase =[]
    for Plate in range(Plate_num - 1):
        Gas_phase.insert(Plate, 0)
        Liq_phase.insert(Plate, 0)
    Gas_phase.insert(0, (1 - sol) * Mol_Num)
    Liq_phase.insert(0, sol * Mol_Num)
    return Gas_phase,Liq_phase

def mycomp(sol,Mol_Num,Plate_num,Gas_phase,Liq_Phase):
    for equibria in range(1):
        Gas_phase[1:len(Gas_phase)] = Gas_phase[0:len(Gas_phase)-1]
        Gas_phase[0] = 0
        for itter in range(Plate_num):
            inGas = (1 - sol) * (Gas_phase[itter]+ Liq_Phase[itter])
            inLiq = sol * (Gas_phase[itter]+ Liq_Phase[itter])
            if inLiq<=1 and inLiq >0:
                Liq_Phase[itter] = 0
            else:
                Liq_Phase[itter] = int(inLiq)
            if inGas<=1 and inGas >0:
                Gas_phase[itter] = 1
            else:
                Gas_phase[itter] = int(inGas)
    return Gas_phase,Liq_Phase




# hier begins the main


#plt.ion()


#Input Parameters
# Placeholder for the plot


col_len = int(st.number_input('Enter Column Length(in CM):',0,100,50))
Car_Velo = float(st.number_input('Enter Column Carrier velocity(m/s):',0.0,10.0,0.1))
Holdup_time = 0.01 * col_len / Car_Velo # Calcualte the Hold up time in Seconds

Plate_num =128    # I've deliberatly fixed the plate number to avoid the programme running slow

Mol_Num = int(st.number_input('Enter Number of Molecules: ',1,3200000,32))
# for the sake of visualization, Concentration is importatn. otherwiese it doesn't influence the calculations


placeholder = st.empty()

equlib_time = 4/Plate_num        #Equilibrium time in sec
sol =[0.0,0.25,0.5,0.75]        #Solubility
#Component 1
[Gas_phase1,Liq_phase1] = initialization(sol[0],Mol_Num,Plate_num)
#Component 2
[Gas_phase2,Liq_phase2] = initialization(sol[1],Mol_Num,Plate_num)
#Component 3
[Gas_phase3,Liq_phase3] = initialization(sol[2],Mol_Num,Plate_num)
#Component 4
[Gas_phase4,Liq_phase4] = initialization(sol[3],Mol_Num,Plate_num)




# Creat Start and Stop button
flag = 0

Start= st.button("Start")
Stop = st.button("Stop")
if Start:
    flag = 1
elif Stop:
    flag =0

# sliders to set the Solubility
sol[1] = 0.01 * st.slider('Comp1 Solubility', 0, 100, 25)
sol[2] = 0.01 * st.slider('Comp2 Solubility', 0, 100, 50)
sol[3] = 0.01 * st.slider('Comp3 Solubility', 0, 100, 75)


fig,ax = plt.subplots()
# if Start is pressed
if flag:

    for iter in range(Plate_num*4):

        [Gas_phase1, Liq_phase1] = mycomp(sol[0],Mol_Num,Plate_num,Gas_phase1,Liq_phase1)
        [Gas_phase2, Liq_phase2] = mycomp(sol[1], Mol_Num, Plate_num, Gas_phase2, Liq_phase2)
        [Gas_phase3, Liq_phase3] = mycomp(sol[2], Mol_Num, Plate_num, Gas_phase3, Liq_phase3)
        [Gas_phase4, Liq_phase4] = mycomp(sol[3], Mol_Num, Plate_num, Gas_phase4, Liq_phase4)
        fig, ax = plt.subplots()


        fig, ax = plt.subplots()
        ax.plot(np.linspace(0,col_len,Plate_num),Gas_phase1,label='wave1')
        ax.plot(np.linspace(0,col_len,Plate_num),Gas_phase2,label = 'wave2')
        ax.plot(np.linspace(0,col_len,Plate_num),Gas_phase3,label = 'wave3')
        ax.plot(np.linspace(0,col_len,Plate_num),Gas_phase4,label = 'wave4')
        placeholder.pyplot(fig)
        # Clear the plot to avoid slowdowns
        plt.close(fig)
        time.sleep(Holdup_time/Plate_num)

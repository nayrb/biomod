from brian import *
import matplotlib.pyplot as plt
import brian
import numpy


def LIF_Step(I_tstart = 0, I_tend = 100, I_amp=5, tend=300):
      
    """
Run the LIF and give a step current input.

Parameters:
tend = 100    (ms) - is the end time of the model    
I_tstart = 20 (ms) - start of current step
I_tend = 70   (ms) - end of current step
I_amp = 1.005 (nA) - amplitude of current step
    """
    
    # neuron parameters
    R = 20*Mohm
    v_reset = 0*mV
    v_rest = 0*mV
    v_threshold = 30*mV
    tau_m = 30*ms
    tau_syn = 10*ms
    tau_ref = 4*ms
    El = 0*mV
    
    # producing step current
    Step_current = numpy.zeros(tend)
    for t in range(tend):
        if(I_tstart <= t and t <= I_tend):
            Step_current[t] = I_amp*nA
    
    
    # differential equation of Leaky Integrate-and-Fire model    
    eqs = '''
    dv/dt = (-(v-El)+R*I)/tau m : volt
    I = I_syn + I_stim : amp
    dI syn/dt = -I_syn/tau_syn : amp
    I_stim : amp
    '''

	
    # making neuron using Brian library

    IF = NeuronGroup(100, model=eqs,reset=v_reset,threshold=v_threshold)
    connections=Connection(IF,IF,'ge')
    connections.connect_random(IF,IF,sparseness=0.3,weight=5*nS)
    IF.v = v_rest
    IF.I = TimedArray(Step_current,dt=1*ms)
    
    # monitoring membrane potential of neuron and injecting current
    Mv = StateMonitor(IF, 'v', record=True)
    Current = StateMonitor(IF, 'I', record=True)
    
    # initialization of simulator
    reinit()
    
    # run the simulation
    run(tend * ms)
        
    # plotting figures
    subplot(211)
    plot(Mv.times/ms, Mv[0]/mV,lw=2)
    plot([0,tend],[v_threshold/mV,v_threshold/mV],'r--',lw=2)
    xlabel('t')
    ylabel('v')
    ylim(0,(v_threshold/mV)*1.2)
    grid()
    
    subplot(212)
    plot(Current.times/ms, Current[0]/nA,lw=2)
    xlabel('t')
    ylabel('I')
    grid()
    
    show()
    
string = "***********************************************************"
string += "\r\n"
string += "***** Ecole polytechnique federale de Lausanne (EPFL) *****"
string += "\r\n"
string += "***** Laboratory of computational neuroscience (LCN)  *****"
string += "\r\n"
string += "*****     Biological modeling of neural networks      *****"
string += "\r\n"
string += "***********************************************************"
string += "\r\n"
string += "This file implements leaky intergrate-and-fire(LIF) model."
string += "\r\n"
string += "You can inject a step current or sinusoidal current into" 
string += "\r\n"
string += "neuron using LIF_Step() or LIF_Sinus() methods respectively."
string += "\r\n"
string += "\r\n"
string += "In order to know parameters and default values for each method"
string += "\r\n"
string += "use symbol ? after the name of method. For example: LIF_Step?"
string += "\r\n\r\n"
string += "-------------2013 EPFL-LCN all rights reserved----------------"
string += "\r\n"

print string

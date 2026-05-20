
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 21 15:05:24 2024

@author: edbra
"""
import numpy as np
import scipy.integrate as si
import matplotlib.pyplot as plt

MyInput = '0'
while MyInput != 'q':
    MyInput = input('Enter a choice, "1", "2" or "q" to quit: ')
    print('You entered the choice: ',MyInput)
    
    if MyInput == '1':
        print('You have chosen part (1): simulation of a lunar orbit')
        
        
        # Function definitions
        
        
    
        def derivatives(time, state, Me, Mm, G): 
            
            
            """
            Function to compute the derivatives for an orbital motion problem
            in 2-D. 
            ----------
            time : Float
                Independent variable, not used as force is time-independant. (s)
            state : Tuple of floats
                Containing (xm, ym, vmx, vmy).
            Me : Float 
                Mass of the earth (kg)
            Mm : Float
                Mass of the moon (kg)
            G : Float
                Gravitational constant 
            
            -------
            Returns: tuple of floats
                Derivatives (dxm/dt, dym/dt, dvmx/dt, dvmy/dt).
            """
            xm, ym, vmx, vmy = state# the 2d state vector of variables at time t
            f1 = vmx#dxm/dt velocity in x direction
            f2 = vmy#dym/dt velocity in y direction
            rm = np.sqrt(xm**2+ym**2) #defining the magnitude of the position vector between two points in 3d space
            f3 = -Me * G * xm/rm**3 # acceleration in the x direction dvmx/dt
            f4 = -Me * G * ym/rm**3 # acceleration in the y direction dvmy/dt
            return (f1, f2, f3, f4)
        
        #============================================================================
        # Main code
        
        # Setting initial conditions
        
        
        # Setting constants
        G = 6.67430e-11 # gravitational constant
        Me = 5.972e24 #mass of earth in kg
        Mm = 7.348e22 # mass of moon, kg
        
        #Initial conditions
        xm0 = 384400e3 # initial x position of the moon ( distance from earth in m)
        ym0 = 0 # Initial y position of the moon in m. moon starts at max x
        vmx0 = 0 # moon starts at max x so initial velocity in x direction is 0 (m/s)
        vmy0 = 1023 # initial velocity in y direction from velocity of moon (m/s)
        #vmy0 = 500
        initial_state = (xm0, ym0, vmx0 , vmy0)
        
        #Time conditions
        t_min = 0 # start time in seconds
        t_max = 30 * 24 * 3600  # slightly over one lunar orbit in seconds
        times = np.linspace(t_min, t_max, num=5000) # time interval function for plot, can be varied to change temporal resolution
        t_interval = (t_min, t_max) # time interval
        
        # Solving the motion
        
        results = si.solve_ivp(derivatives, (t_min,t_max), initial_state, t_eval=times, args=(G, Mm, Me), atol = 1e-8, rtol = 1e-8) # solves the differential for the motion of the moon over time
        
        
        # Plotting the results
        
        x = results.y[0,:] #taking the x coordinate of the moon from results
        y = results.y[1,:] #taking the y coordinate of the moon from results
        
        plt.figure(figsize=(8, 8)) # size of the figure 
        plt.plot(0, 0, 'bo', label='Earth') # plotting the Earth at origin to make the graph look nice
        plt.plot(x, y, 'r-', label='Moon Orbit') # plotting the moons trajectory
        plt.xlabel("x position (m)") # labelling the x axis
        plt.ylabel("y position (m)") # labelling the y axis
        plt.title("2D Motion of the Moon Orbiting the Earth") # title
        plt.legend()
        plt.axis('equal') #ensuring the axis are scaled equally
        plt.grid(True) # showing a grid 
        plt.show()

    elif MyInput == '2':
        print('You have chosen part(2): earth-moon-probe system')
        
        #Function Definitions
        
        def derivatives(time, statep, Me, Mm, G): 
            
            
            """
            Function to compute the derivatives for an orbital motion problem
            in 2-D. 
            ----------
            time : Float
                Independent variable, not used as force is time-independant. (s)
            statep : Tuple of floats
                Containing (xm, ym, vmx, vmy, xp, yp, vpx, vpy).
            Me : Float 
                Mass of the earth (kg)
            Mm : Float
                Mass of the moon (kg)
            G : Float
                Gravitational constant 
            
            -------
            Returns: tuple of floats
                Derivatives (dxm/dt, dym/dt, dvmx/dt, dvmy/dt, dxp/dt, dyp/dt, dvpx/dt, dvpy/dt).
            """
        
            xm, ym, vmx, vmy, xp, yp, vpx, vpy = statep# the 2d state vector of variables at time t
            
            #moon equations of motion
            
            f1 = vmx#dxm/dt velocity in x direction
            f2 = vmy#dym/dt velocity in y direction
            rm = np.sqrt(xm**2+ym**2) #defining the magnitude of the position vector between two points in 3d space
            f3 = -Me * G * xm/rm**3 # acceleration in the x direction dvmx/dt
            f4 = -Me * G * ym/rm**3 # acceleration in the y direction dvmy/dt
            
            #probe equations of motion
            xpm = xp-xm # position in the x direction (m)
            ypm = yp-ym # position in the y direction (m)
            rpe = np.sqrt(xp**2+yp**2) # probe to earth distance(m)
            rpm = np.sqrt(xpm**2 + ypm**2) # probe to moon radius distance (m)
            f5 = vpx #dxp/dt velocity of the probe in the x direction 
            f6 = vpy #dyp/dt velocity of the probe in the y direction 
            f7 = -Me*G*xp/rpe**3 - Mm*G*xpm/rpm**3 #acceleration in the x direction dvpx / dt 
            f8 = -Me*G*yp/rpe**3 - Mm*G*ypm/rpm**3 #acceleration in the y direction dvpy / dt 
            
            return (f1, f2, f3, f4, f5, f6, f7, f8)
        #===================================================================================================       

        # Main Code
        
        #Setting constants
        
        # Setting constants
        G = 6.67430e-11 # gravitational constant
        Me = 5.972e24 #mass of earth in kg
        Mm = 7.348e22 # mass of moon, kg
        
        #Initial conditions of moon
        xm0 = 3.844e8 # initial x position of the moon ( distance from earth in m)
        ym0 = 0 # Initial y position of the moon in m. moon starts at max x
        vmx0 = 0 # moon starts at max x so initial velocity in x direction is 0 (m/s)
        vmy0 = np.sqrt(Me*G/xm0) # initial velocity in y direction from velocity of moon (m/s)
        #vmy0 = 1500
        
        #Probe initial conditions from the moon
        rpm =  20e6 # radius of the probes orbit around the moon(m)
        xpm0 = 0 # distance between probe and moon in x direction (m)
        ypm0 = rpm # distance between probe and moon in y direction (m)
        vpmx0 = np.sqrt(G*Mm/abs(rpm)) # velocity of the probe in the x direction (m/s)
        #vpmx0 = 2
        vpmy0 = 0 # velocitry of the probe in the y direction (m/s)
        
        #Probe initial conditions from the earth
        
        xpe0 = xm0+xpm0 # initial position of probe in x direction (m)
        ype0 = ym0+ypm0 # initial position of probe in y direction (m)
        vpex0 = vmx0+vpmx0 # initial velocity of probe in x direction (m/s)
        vpey0 = vmy0+vpmy0 # initial velocity of probe in y direction (m/s)
        
        initial_statep = (xm0, ym0, vmx0, vmy0, xpe0, ype0, vpex0, vpey0) # initial conditions state
        
        #Time conditions
        t_min = 0 # start time in seconds
        t_max = 28 * 24 * 3600  # slightly over one lunar orbit in seconds
        times = np.linspace(t_min, t_max, num=5000) # time interval function for plot, can be varied to change temporal resolution
        t_interval = (t_min, t_max) # time interval

        #Solving the motion
        
        results = si.solve_ivp(derivatives, t_interval, initial_statep, t_eval=times, args=(Me, Mm, G), atol=1e-6, rtol=1e-6)

        #Plotting results
        
        xm = results.y[0, :]  # x position of Moon
        ym = results.y[1, :]  # y position of Moon
        
        xp = results.y[4, :]  # x position of Probe
        yp = results.y[5, :]  # y position of Probe
    
        plt.figure(figsize=(10, 10))  #Increasing the figure size
        plt.plot(0, 0, 'bo', label='Earth')  #plotting Earth at origin
        plt.plot(xm, ym, 'r-', label='Moon Orbit')#plotting moon's trajectory
        plt.plot(xp, yp, 'g-', label='Probe Orbit')# plotting probe's trajectory
        plt.xlabel("x position (m)")#labelling the x axis
        plt.ylabel("y position (m)")#labelling the y axis
        plt.title("2D motion of a probe orbiting the moon in motion around the Earth")
        plt.legend() #adding the legend 
        plt.axis('equal') #ensuring axis has equal scaling
        plt.grid(True) #adding grid
        
        # Show the plot
        plt.show()
        
    elif MyInput != 'q':
        print('This is not a valid choice')
print('You have chosen to finish - goodbye.')
        
import numpy as np
from math import exp, sqrt

class Grain:

    def __init__(self):
        self.g_size = np.array([])
        self.stat = np.array([[0, 0, 0, 0, 0, 0]])
        pass
        
    def CalcControl(self, temp, stfe, liqv, ctsv, mode1, mode2):
        #set-up temperature related variables
        if temp != self.def_temp:
            t_A = 1.0 * exp(-1.0 * self.def_Act/(self.def_temp + 273))
            t_a = 1.0 * exp(-1.0 * self.def_Act/(temp + 273))
            self.f_B = t_a / t_A
            self.f_C = 1.0 * (self.def_temp + 273) /(temp + 273)
            self.f_A = self.f_B * self.f_C
            new_sfe = 1.0 * exp(-1.0 * self.def_rta/sqrt(self.def_rtt - temp - 273))
            self.s_e = new_sfe * new_sfe / self.def_sfe / self.def_sfe
            self.s_s = self.def_sfe / new_sfe
        #set-up step free energy
        if stfe != self.def_sfe:
            self.s_e = stfe * stfe / self.def_sfe / self.def_sfe
            self.s_s = self.def_sfe / stfe
        #set-up liquid volume fraction (Ardell's) (actually, s_1 should be 0 when liqv=1)
        self.s_l = 26.0 - 25.0*liqv
        self.h_time = ctsv
        self.mode = mode1
        self.screw = mode2

    def __rstat(self, cts_num):
        self.g_num = len(self.g_size)
        self.rav = self.g_size.mean()
        rstd = self.g_size.std()
        rmax = self.g_size.max()
        stat_add = np.array([[cts_num, self.rstar, self.rav, rstd, rmax, self.g_num]])
        self.stat = np.append(self.stat, stat_add, axis=0)

    def GetStatistics(self):
        return self.stat

    def CalcGrowth(self, cts_num):
        #calc rave rstd gnum
        self.__rstat(cts_num)
        #calc rstar
        self.rstar = self.__rstar()
        #vary the grain size
        self.g_size += self.CalcJacobian(self.rstar)
        # r<=0.05nm means no grain
        for i in range(self.g_num):
            if self.g_size[i] > self.rstar:
                break
            elif self.g_size[i] < 5.0e-3:
                self.g_size[i] = 0
        np.trim_zeros(self.g_size)

    def LoadGrain(self, cts_num):
        self.cts = cts_num
        #filename = 'd_0000000.txt.npy'
        filename = 'd_' + '{:07d}'.format(cts_num) + '.txt.npy'
        self.g_size = np.load(filename)
        #in case of using ascii format
        #filename = 'd_' + '{:07d}'.format(cts_num) + '.txt'
        #read line by line, and append to _grain
    
    def SaveGrain(self, cts_num):
        #filename = 'd_0000000.txt.npy'
        filename = 'd_' + '{:07d}'.format(cts_num) + '.txt'
        np.save(filename, self.g_size)
        #in case of using ascii format
        #filename = 'd_' + '{:07d}'.format(cts_num) + '.txt'
        #read line by line, and append to _grain

    def CalcJacobian(self, r):
        MAX = len(self.g_size)
        g_vary = np.empty(MAX)
        #in case AGG
        if self.mode == True:
            for i in range(MAX):
                if self.g_size[i] == 0 or self.g_size[i] == r:
                    g_vary[i] = 0.0
                elif self.g_size[i] < r:
                    g_vary[i] = self.h_time * self.c_A * self.f_A * 1.0/self.g_size[i] * (1.0/r - 1.0/self.g_size[i]) * (1.0+ self.s_l * self.g_size[i]/r)
                    if (g_vary[i] + self.g_size[i]) < 0:
                        g_vary[i] = -1.0 * self.g_size[i]
                else:
                    k11 = self.h_time * self.c_A * self.f_A * 1.0/self.g_size[i] * (1.0/r - 1.0/self.g_size[i]) * (1.0+ self.s_l * self.g_size[i]/r)
                    k12 = self.h_time * self.c_A * self.f_A * 1.0/(self.g_size[i]+ 0.5*k11) * (1.0/r - 1.0/(self.g_size[i]+ 0.5*k11)) * (1.0+ self.s_l * (self.g_size[i]+ 0.5*k11)/r)
                    k13 = self.h_time * self.c_A * self.f_A * 1.0/(self.g_size[i]+ 0.5*k12) * (1.0/r - 1.0/(self.g_size[i]+ 0.5*k12)) * (1.0+ self.s_l * (self.g_size[i]+ 0.5*k12)/r)
                    k14 = self.h_time * self.c_A * self.f_A * 1.0/(self.g_size[i]+ 1.0*k13) * (1.0/r - 1.0/(self.g_size[i]+ 1.0*k13)) * (1.0+ self.s_l * (self.g_size[i]+ 1.0*k13)/r)
                    g_vn = (k11 + 2.0*k12 + 2.0*k13 + k14)/6.0
                    k21 = self.h_time * self.c_B * self.f_B * exp(-1.0* self.s_e * self.f_C * self.c_C /(1.0/r - 1.0/self.g_size[i]))
                    k22 = self.h_time * self.c_B * self.f_B * exp(-1.0* self.s_e * self.f_C * self.c_C /(1.0/r - 1.0/(self.g_size[i]+ 0.5*k21)))
                    k23 = self.h_time * self.c_B * self.f_B * exp(-1.0* self.s_e * self.f_C * self.c_C /(1.0/r - 1.0/(self.g_size[i]+ 0.5*k22)))
                    k24 = self.h_time * self.c_B * self.f_B * exp(-1.0* self.s_e * self.f_C * self.c_C /(1.0/r - 1.0/(self.g_size[i]+ 1.0*k23)))
                    g_va = (k21 + 2.0*k22 + 2.0*k23 + k24)/6.0
                    if g_va > g_vn:
                        g_vary[i] = 1.0/(1.0/g_va + 1.0/g_vn)
                    else:
                        g_vary[i] = g_va
                        if self.screw == True:
                            k31 = self.h_time * self.c_D * self.f_A * self.s_s * 1.0/self.g_size[i] * pow(1.0/r - 1.0/self.g_size[i],2.0)
                            k32 = self.h_time * self.c_D * self.f_A * self.s_s * 1.0/(self.g_size[i]+ 0.5*k31) * pow(1.0/r - 1.0/(self.g_size[i]+ 0.5*k31),2.0)
                            k33 = self.h_time * self.c_D * self.f_A * self.s_s * 1.0/(self.g_size[i]+ 0.5*k32) * pow(1.0/r - 1.0/(self.g_size[i]+ 0.5*k32),2.0)
                            k34 = self.h_time * self.c_D * self.f_A * self.s_s * 1.0/(self.g_size[i]+ 1.0*k33) * pow(1.0/r - 1.0/(self.g_size[i]+ 1.0*k33),2.0)
                            g_vs = (k31 + 2.0*k32 + 2.0*k33 + k34)/6.0
                            g_vary[i] += g_vs
                            if g_vary[i] > g_vn:
                                g_vary[i] = g_vn
        #in case NGG (self.mode == False)
        else:
            for i in range(MAX):
                if self.g_size[i] == 0 or self.g_size[i] == r:
                    g_vary[i] = 0.0
                elif self.g_size[i] < r:
                    g_vary[i] = self.h_time * self.c_A * self.f_A * 1.0/self.g_size[i] * (1.0/r - 1.0/self.g_size[i]) * (1.0+ self.s_l * self.g_size[i]/r)
                    if (g_vary[i] + self.g_size[i]) < 0:
                        g_vary[i] = -1.0 * self.g_size[i]
                else:
                    k1 = self.h_time * self.c_A * self.f_A * 1.0/self.g_size[i] * (1.0/r - 1.0/self.g_size[i]) * (1.0+ self.s_l * self.g_size[i]/r)
                    k2 = self.h_time * self.c_A * self.f_A * 1.0/(self.g_size[i]+ 0.5*k1) * (1.0/r - 1.0/(self.g_size[i]+ 0.5*k1)) * (1.0+ self.s_l * (self.g_size[i]+ 0.5*k1)/r)
                    k3 = self.h_time * self.c_A * self.f_A * 1.0/(self.g_size[i]+ 0.5*k2) * (1.0/r - 1.0/(self.g_size[i]+ 0.5*k2)) * (1.0+ self.s_l * (self.g_size[i]+ 0.5*k2)/r)
                    k4 = self.h_time * self.c_A * self.f_A * 1.0/(self.g_size[i]+ 1.0*k3) * (1.0/r - 1.0/(self.g_size[i]+ 1.0*k3)) * (1.0+ self.s_l * (self.g_size[i]+ 1.0*k3)/r)
                    g_vary[i] = (k1 + 2.0*k2 + 2.0*k3 + k4)/6.0
        return g_vary

    def __mass(self, r):
        #calculate mass (volume)
        MAX = len(self.g_size)
        v_mass = 0.0
        gm_v = np.array(self.CalcJacobian(r))
        for j in range(MAX):
            v_mass += self.c_M * self.g_size[j] * self.g_size[j] * gm_v[j]
        return v_mass

    def __rstar(self):
        v_r = self.rav
        v_mass = self.__mass(v_r)
        print('TRACE v-mass: ', v_mass)
        d_r = 5.0
        while v_mass > 0.1 or v_mass < -0.1:
            if v_mass > 0:
                v_r += d_r
                v_mass = self.__mass(v_r)
                if v_mass < 0:
                    d_r /= 2
            else:
                v_r -= d_r
                v_mass = self.__mass(v_r)
                if v_mass > 0:
                    d_r /= 2
        print('rstar= ', v_r)
        return v_r
        
    ##constants
    c_A = 10.0e3    # 2 gamma V_m C_inf D_f / RT (conversion from 10e-21)
    c_B = 1.0e33    # const incl. D_f (conversion from 1.0e25)
    c_C = 0.27965   # pi sigma^2 / 6k T h gamma (conversion from 2.7965e7)
    c_D = 100.00    # 2 A gamma h^2 / pi sigma
    c_M = 2.0e-4
    # gamma = 0.1 J/m
    # h = 1.2e-10 m
    # D_f = 1e-9 m2/s
    # C_inf = 0.1
    # V_m = 10e-6 m3
    # R = 8.314
    # k = 1.38e-23
    ##variables
    def_temp = 1500 # 1500C = 1773K
    def_sfe = 0.33
    def_Act = 10.0e3
    def_rta = 16.7
    def_rtt = 2000  # 2000K
    ##calculations
    g_num = 0       # number of grain in system
    rstar = 0.0     # critical grain size also in Radius
    rav = 0.0       # average Radius
    mode = True     # calculation modes 1: AGG, 0: NGG 
    screw = False 
    h_time = 0.1    # calculation step increment
    s_l = 1.0       # liquid volume fraction
    s_e = 1.0       # step free energy (0.62hG)
    s_s = 1.0       # step free energy (0.62hG)
    f_A = 1.0       # temperature on diffusion (1500C=1773K)
    f_B = 1.0       # temperature on diffusion (1500C=1773K)
    f_C = 1.0       #
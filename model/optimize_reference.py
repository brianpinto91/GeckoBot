# -*- coding: utf-8 -*-
"""
Created on Tue Jul 03 14:33:49 2018

@author: Lars Schiller (AmP)
"""
import kinematic_model_fun as model
from scipy.optimize import minimize
from scipy.optimize import basinhopping
import numpy as np


def gnerate_ptrn_symmetric(X, n_cycles):
    ptrn = []
    for n in range(n_cycles):
        p = X
        ptrn.append([[p[0], p[1], p[2], p[3], p[4]], [1, 0, 0, 1]])
        ptrn.append([[p[1], p[0], -p[2], p[4], p[3]], [0, 1, 1, 0]])
    return ptrn


def gnerate_ptrn(X, n_cycles):
    ptrn = []
    for n in range(n_cycles):
        p = X
        ptrn.append([[p[0], p[1], p[2], p[3], p[4]], [1, 0, 0, 1]])
        ptrn.append([[p[5], p[6], p[7], p[8], p[9]], [0, 1, 1, 0]])
    return ptrn


def gnerate_ptrn_3fixed_1(X, n_cycles):
    ptrn = []
    for n in range(n_cycles):
        p = X
        ptrn.append([[p[0], p[1], p[2], p[3], p[4]], [1, 0, 1, 1]])
        ptrn.append([[p[5], p[6], p[7], p[8], p[9]], [0, 1, 1, 1]])
        ptrn.append([[p[10], p[11], p[12], p[13], p[14]], [1, 1, 0, 1]])
        ptrn.append([[p[15], p[16], p[17], p[18], p[19]], [1, 1, 1, 0]])
    return ptrn


def gnerate_ptrn_3fixed_2(X, n_cycles):
    ptrn = []
    for n in range(n_cycles):
        p = X
        ptrn.append([[p[0], p[1], p[2], p[3], p[4]], [1, 1, 0, 1]])
        ptrn.append([[p[5], p[6], p[7], p[8], p[9]], [0, 1, 1, 1]])
        ptrn.append([[p[10], p[11], p[12], p[13], p[14]], [1, 0, 1, 1]])
        ptrn.append([[p[15], p[16], p[17], p[18], p[19]], [1, 1, 1, 0]])
    return ptrn


def gnerate_ptrn_3fixed_3(X, n_cycles):
    ptrn = []
    for n in range(n_cycles):
        p = X
        ptrn.append([[p[0], p[1], p[2], p[3], p[4]], [1, 1, 1, 0]])
        ptrn.append([[p[5], p[6], p[7], p[8], p[9]], [0, 1, 1, 1]])
        ptrn.append([[p[10], p[11], p[12], p[13], p[14]], [1, 0, 1, 1]])
        ptrn.append([[p[15], p[16], p[17], p[18], p[19]], [1, 1, 0, 1]])
    return ptrn


def optimize_gait_3fixed(n_cycles, initial_pose, method='COBYLA',
                         x0=[90, .1, -90, 90, .1]):
    obj_history = []
    bleg = (0.1, 120)
    btor = (-120, 120)
    bnds = [bleg, bleg, btor, bleg, bleg]*4
    X0 = x0*4

    def objective_3fixed(X):
        ptrn = gnerate_ptrn_3fixed_1(X, n_cycles)
        xfinal, rfinal, _, _ = model.predict_pose(ptrn, initial_pose)
        xfp, yfp = rfinal
        obj = -np.sqrt((sum(yfp))**2 + (sum(xfp))**2)
        obj_history.append(obj)
        print 'step', len(obj_history), '\t', obj
        return obj

    solution = minimize(objective_3fixed, X0, method=method, bounds=bnds)
    X = solution.x
    ptrn = gnerate_ptrn_3fixed_1(X, n_cycles)
    return ptrn, obj_history, objective_3fixed(X)


def optimize_gait_straight(n_cycles, initial_pose, method='COBYLA',
                           x0=[90, .1, -90, 90, .1]):
    obj_history = []
    bleg = (0.1, 120)
    btor = (-120, 120)
    bnds = [bleg, bleg, btor, bleg, bleg]
    X0 = x0

    def objective_straight(X):
        ptrn = gnerate_ptrn_symmetric(X, n_cycles)
        xfinal, rfinal, _, _ = model.predict_pose(ptrn, initial_pose)
        xfp, yfp = rfinal
        obj = sum(yfp)
        obj_history.append(obj)
        print 'step', len(obj_history), '\t', obj
        return -obj

    solution = minimize(objective_straight, X0, method=method, bounds=bnds)
    X = solution.x
    ptrn = gnerate_ptrn_symmetric(X, n_cycles)
    return ptrn, obj_history, objective_straight(X)


def optimize_gait_curve(n_cycles, initial_pose, method='COBYLA',
                        x0=[90, .1, -90, 90, .1]):
    obj_history = []
    bleg = (0.01, 120)
    btor = (-120, 120)
    bnds, X0 = [], []
    bnds = [bleg, bleg, btor, bleg, bleg, bleg, bleg, btor, bleg, bleg]
    X0 = model.flat_list([x0, x0])

    def objective_curve(X):
        ptrn = gnerate_ptrn(X, n_cycles)
        xfinal, rfinal, _, _ = model.predict_pose(ptrn, initial_pose)
        eps = xfinal[-1]
        obj = eps
        obj_history.append(obj)
        print 'step', len(obj_history), '\t', obj
        return obj

    solution = minimize(objective_curve, X0, method=method, bounds=bnds)
    X = solution.x
    ptrn = gnerate_ptrn(X, n_cycles)
    return ptrn, obj_history, objective_curve(X)


if __name__ == '__main__':
    import matplotlib.pyplot as plt

    """
    for the initial pose:
        init_pose = [[.1, 90, 90, .1, 90], 90, (0, 3)]
        n_cycles = 1
        X0 = [90, .1, -90, 90, .1,
              .1, 90, 90, .1, 90]
    the following stats are recorded:

    method | nfev | obj
    -------|------|-------
    COBYLA | 200  | 10.9
    TNC    | 480  | 12.85 (na)
    CG     | 324  | 12.85 (na)
    Powell | 1891 | 16.09

    _______________________________________________________________

    for the initial pose:
        init_pose = [[.1, 90, 90, .1, 90], 90, (0, 3)]
        n_cycles = 1
        X0 = [50, .1, -50, 50, .1,
              .1, 50, 50, .1, 50]
    the following stats are recorded:

    method | nfev | obj
    -------|------|-------
    COBYLA | 257  | 16.85
    TNC    | 157  | 11.09 (na)
    CG     | 1093 | 11.09 (na)
    Powell | 1587 | 14.09
    """

    methods = ['Powell', 'COBYLA', 'CG', 'TNC', 'SLSQP']
    x0 = [10, .1, -10, 10, .1]
    init_pose = [[.1, 90, 90, .1, 90], 90, (0, 3)]
    method = methods[1]
    n_cycles = 5
#    opt_ptrn, obj_hist, opt_obj = optimize_gait_straight(n_cycles, init_pose, 
#                                                         method, x0=x0)
#    opt_ptrn, obj_hist, opt_obj = optimize_gait_curve(n_cycles, init_pose, 
#                                                      method, x0=x0)
    opt_ptrn, obj_hist, opt_obj = optimize_gait_3fixed(n_cycles, init_pose,
                                                       method, x0=x0)
    opt_ptrn = opt_ptrn[:4]

#    opt_ptrn = [[[92.85, -3.54, -92.29, 87.07, -2.70], [1, 0, 0, 1]],
#                [[-7.55, -11.88, -10.39, -16.22, 3.09], [0, 1, 1, 0]],
#                [[90.34, 1.32, -90.01, 91.28, -0.60], [1, 0, 0, 1]],
#                [[-3.12, 3.31, -5.64, 2.08, 2.45], [0, 1, 1, 0]]]


# _______________________________________________________________
#    Straight tries
#    opt_ptrn = [[[60, 12, -100, 60, 12], [1, 0, 0, 1]],  # slightly modified
#                [[12, 60, 100, 12, 60], [0, 1, 1, 0]]]

#    opt_ptrn = [[[39, 22, -110, 25, 13], [1, 0, 0, 1]],  # opt sym sol
#                [[22, 39, 110, 13, 25], [0, 1, 1, 0]]]


#    Straight opt pattrns:
#    opt_ptrn = [[[35, 12, -97, 40, 12], [1, 0, 0, 1]],  # 1 cycle
#                [[12, 35, 97, 12, 40], [0, 1, 1, 0]]]

#    opt_ptrn = [[[35, 12, -97, 41, 15], [1, 0, 0, 1]],  # 2 cycle
#                [[12, 35, 97, 15, 41], [0, 1, 1, 0]]]

#    opt_ptrn = [[[34, 10, -98, 41, 14], [1, 0, 0, 1]],  # 3 cycle **
#                [[10, 34, 98, 14, 41], [0, 1, 1, 0]]]

# _______________________________________________________________
#    Curve opt pattrns
#    opt_ptrn = [[[16, -57, -35, -7, -40], [1, 0, 0, 1]],  # 1 cycle
#                [[52, 74, -60, 100, 5], [0, 1, 1, 0]]]

#    opt_ptrn = [[[16, -60, -37, -3, -37], [1, 0, 0, 1]],  # 2 cycle
#                [[77, 66, -93, 90, 30], [0, 1, 1, 0]]]

#    opt_ptrn = [[[-13, -87, -45, -30, -72], [1, 0, 0, 1]],  # 3 cycle
#                [[95, 80, -65, 120, 54], [0, 1, 1, 0]]]

# _______________________________________________________________
#    Curve opt pattrns after bounded alpref
#    opt_ptrn = [[[0.01, 0.01, -23, 0.01, 0.01], [1, 0, 0, 1]],  # 1 cycle
#                [[50, 67, -60, 114, 0.01], [0, 1, 1, 0]]]

#    opt_ptrn = [[[0.01, 0.01, -12, 0.01, 0.01], [1, 0, 0, 1]],  # 2 cycle
#                [[203, 152, -76, 257, 160], [0, 1, 1, 0]]]

#    opt_ptrn = [[[1, 0.01, -7, 0.01, 0.01], [1, 0, 0, 1]],  # 3 cycle *****
#                [[114, 109, -101, 146, 82], [0, 1, 1, 0]]]

    filled_ptrn = model.fill_ptrn(opt_ptrn, n_cycles=2)

    x, r, data, cst = model.predict_pose(filled_ptrn, init_pose, stats=1, debug=1)
    model.plot_gait(*data)

    plt.figure()
    plt.plot(cst)

    print x0
    print method, '\t| ', len(obj_hist), '\t| ', round(opt_obj, 4),  '\t| ', n_cycles
    print '\n', opt_ptrn, '\n'



    fig = plt.figure()
    lin = model.animate_gait(fig, *data)
    plt.show()
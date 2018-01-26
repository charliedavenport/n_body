from __future__ import print_function
import matplotlib.pyplot as plt
import numpy as np
import numpy.random as random
import math
import timeit


class body:
    def __init__(self, pos, mass, vel, color='cyan'):
        self.pos = pos # shape (2,)
        self.mass = mass
        self.vel = vel # shape (2,)
        self.color = color # string passed into plt.plot()

def get_accell(bodies, target_ind):
    G = 6.67408e-11 # gravitational constant
    accell = np.array([0.0,0.0])
    target = bodies[target_ind]
    # Euler-Cromer method
    for ind, bod in enumerate(bodies):
        if ind != target_ind:
            r = math.sqrt((target.pos[0] - bod.pos[0])**2 + (target.pos[1] - bod.pos[1])**2)
            dx = bod.pos[0] - target.pos[0]
            dy = bod.pos[1] - target.pos[1]
            accell[0] += G * bod.mass / r**3 * dx
            accell[1] += G * bod.mass / r**3 * dy
    #print "acc ", accell
    # if accelleration is too high, return 0 vector. This prevents sudden 'flinging'
    if max(accell.max(), abs(accell.min())) > 75: return [0,0]
    return accell

def update_vel(bodies, time_step = 1.0):
    for i, bod in enumerate(bodies):
        a = get_accell(bodies, i)
        bod.vel[0] += a[0] * time_step
        bod.vel[1] += a[1] * time_step
        #print "vel ", bod.vel

def update_pos(bodies, time_step = 1.0):
    for bod in bodies:
        bod.pos[0] += bod.vel[0] * time_step
        bod.pos[1] += bod.vel[1] * time_step
        #print "pos ", bod.pos

def run_simulation(bodies, time_step = 1.0, max_steps = 10):
    # create array for histories, used for plotting trails
    #hists = [[[b.pos[0], b.pos[1]]] for b in bodies]
    hists = np.zeros((len(bodies), max_steps, 2))
    fig = plt.figure()
    ax = plt.subplot(facecolor='white')
    maxrange = 5.0
    times = np.zeros((max_steps))
    for i in range(max_steps):
        start_time = timeit.default_timer()
        plt.cla()
        plt.axis([-maxrange, maxrange, -maxrange, maxrange])
        for j, b in enumerate(bodies):
            for x in b.pos:
                if abs(x) > maxrange: maxrange *= 1.2
            ax.plot(b.pos[0], b.pos[1], color=b.color, marker="o")
            hists[j, i, :] = b.pos
            ax.plot(hists[j, max(0,i-50):i, 0], hists[j, max(0,i-50):i, 1], color=b.color)
        # brute force (emphasis on brute) only need to compute 1/2 as many
        # forces, because of newton's 3rd law
        update_vel(bodies, time_step)
        update_pos(bodies, time_step)
        plt.pause(0.01)
        times[i] = timeit.default_timer() - start_time
        print (times[i])
    plt.close()
    print ("average time to draw frame: ", times.mean())
    print ("std dev of times: ", times.std())
    print ("max fps: ", np.floor(1.0/times.mean()))

def test_run():
    """
    bodies = [
            body([ 0, 0],   2e11, [0, 0],   'green'),
            body([ 0, 2.5], 1e10, [1.5, 0], 'red'),
            body([-2, -4],  2e10, [-1, 1.5],  'blue'),
            body([ 2, 4],   2e10, [1, -1.5],  'magenta'),
            body([ -4, 1],  1e10, [0, 0.75],  'cyan')
            ]
    """
    #bodies = [body([4 * random.rand(2) - 1], random.rand() * 4e10, [0.0]) for i in range(10)]
    bodies = []
    for i in range(10):
        bodies.append(body(8*random.rand(2)-4,
                           random.rand() * 4e10,
                           3*random.rand(2)-1.5,
                           random.rand(3)))
    run_simulation(bodies, 0.05, 300)
    #time_test(bodies)

def time_test(bodies):
    times = np.zeros((10))
    for i in range(10):
        start_time = timeit.default_timer()
        update_vel(bodies)
        update_pos(bodies)
        times[i] = timeit.default_timer() - start_time
        print (times[i])
    print ("avg time for one step: ", times.mean())
    print ("std dev of times: ", times.std())
    print ("max iterations per second: ", np.floor(1.0/times.mean()))

if __name__ == '__main__':
    test_run()

"""Computes best deployment schedule."""
from __future__ import print_function, unicode_literals
import os
import subprocess
from copy import deepcopy
from multiprocessing import Pool
from argparse import ArgumentParser
from contextlib import contextmanager
try:
    import simplejson as json
except ImportError:
    import json

import numpy as np
import pandas as pd
import cymetric as cym

import base

@contextmanager
def indir(d):
    cwd = os.getcwd()
    os.chdir(d)
    yield
    os.chdir(cwd)


def simbasename(t, lwr=0, fr=0):
    lwr = '{0:+02}'.format(lwr).replace('+', 'p').replace('-', 'm')
    fr = '{0:+02}'.format(fr).replace('+', 'p').replace('-', 'm')
    name = 'eg01-eg23-t{t:03}-lwr{lwr}-fr{fr}'.format(t=t, lwr=lwr, fr=fr)
    return name


def make_simulation(t, lwr=0, fr=0, deployment=None):
    """Makes a simulation for a given perturbed time and LWR or FR number."""
    if deployment is None:
        deployment = deepcopy(base.bo_deployment)
    deployment['LWR'][t] = max(0, deployment['LWR'][t] + lwr)
    deployment['FR'][t] = max(0, deployment['FR'][t] + fr*0.4)
    sim = base.make_simulation('cycamore', deployment=deployment)
    fname = simbasename(t, lwr=lwr, fr=fr) + '.json'
    with open(fname, 'w') as f:
        json.dump(sim, f, sort_keys=True, indent=1, separators=(', ', ': '))
    with open(fname.replace('eg01-eg23', 'deployment'), 'w') as f:
        json.dump(deployment, f, sort_keys=True, indent=1, 
                  separators=(', ', ': '))
    return fname


def make_simulations():
    print("Making simulations...")
    tmin, tmax = 50, 251
    sims = [make_simulation(t, lwr=1) for t in range(tmin, tmax)]
    sims += [make_simulation(t, fr=1) for t in range(tmin, tmax)]
    sims += [make_simulation(t, lwr=-1) for t in range(tmin, tmax)]
    sims += [make_simulation(t, fr=-1) for t in range(tmin, tmax)]
    print("...done")
    return sims


def run_simulation(fname):
    print("  " + fname)
    basename = os.path.splitext(fname)[0]
    oname = basename + '.sqlite'
    outname = basename + '.out'
    resname = basename + '-res.json'
    if os.path.isfile(resname):
        with open(resname, 'r') as f:
            res = json.load(f)
        return res
    out = ''
    cmd = ['cyclus', '-o', oname, fname]
    try:
        out = subprocess.check_output(cmd, universal_newlines=True, 
                                      stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError:
        if os.path.isfile(oname):
            os.remove(oname)
        return None
    with open(outname, 'w') as f:
        f.write(out)
    score = objective(oname)
    res = [oname, score]
    with open(resname, 'w') as f:
        json.dump(res, f)
    if os.path.isfile(oname):
        os.remove(oname)
    return res


def run_simulations(j=1):
    print("Running simulations...")
    sims = make_simulations()
    pool = Pool(j)
    res = pool.map(run_simulation, sims)
    print("...done")
    if any(map((lambda x: x is None), res)):
        print('Some simulations failed:')
        for sim, r in zip(sims, res):
            if r is None:
                print('  ' + sim)

def demand_curve(v0, r, tmax):
    return v0 * (1 + r)**np.arange(tmax)


def objective(sim):
    with cym.dbopen(sim) as db:
        evaler = cym.Evaluator(db)
        elec_gen = evaler.eval('FcoElectricityGenerated')
    elec_gen = elec_gen[-200:]
    demand = demand_curve(90, 0.01, 200)
    score = sum((elec_gen.Power - demand).abs())
    return score


def compute_best(sims, scores):
    print("sorting objective values:")
    results = sorted(zip(sims, scores), key=lambda x: x[1])
    print(results)


def main():
    parser = ArgumentParser('scheduler')
    parser.add_argument('-j', default=1, type=int, 
                        help='degree of parallelism')
    parser.add_argument('-w', default='temp',
                        help='working directory')
    ns = parser.parse_args()

    if not os.path.isdir(ns.w):
        os.mkdir(ns.w)
    with indir(ns.w):
        results = run_simulations(j=ns.j)
        compute_best(*results)


if __name__ == '__main__':
    main()

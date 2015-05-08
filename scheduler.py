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

from argparse import ArgumentParser


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
    tmin, tmax = 50, 251
    sims = [make_simulation(t, lwr=1) for t in range(tmin, tmax)]
    sims += [make_simulation(t, fr=1) for t in range(tmin, tmax)]
    sims += [make_simulation(t, lwr=-1) for t in range(tmin, tmax)]
    sims += [make_simulation(t, fr=-1) for t in range(tmin, tmax)]
    return sims


def run_simulation(fname):
    basename = os.path.splitext(fname)[0]
    oname = basename + '.sqlite'
    outname = basename + '.out'
    if os.path.isfile(oname):
        return oname
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
    return oname


def run_simulations(j=1):
    sims = make_simulations()
    pool = Pool(j)
    onames = pool.map(run_simulation, sims)
    if any(map((lambda x: x is None), onames)):
        print('Some simulations failed:')
        for sim, oname in zip(sims, onames):
            if oname is None:
                print('  ' + sim)


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
        run_simulations(j=ns.j)


if __name__ == '__main__':
    main()

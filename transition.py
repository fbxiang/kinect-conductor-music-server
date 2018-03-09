import os
import random
import json

def read_fsm(filepath, states):
    transition = {}
    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()
            if line.startswith('#') or line == '':
                continue
            names = line.split(',')

            # check states are valid
            for n in names:
                assert n in states

            # check there is a transition
            assert len(names) > 1

            transition[names[0]] = names[1:]
    return transition


def read_json(filepath):
    with open(filepath, 'r') as f:
        t = f.readlines()[0]
        t = json.loads(t)
    return t


class FSM:

    def __init__(self):
        states = {}
        ver = 'v2'
        files = [f for f in os.listdir(ver) if '.json' in f]
        names = [f[:-5] for f in files]
        for n, f in zip(names, files):
            states[n] = read_json(os.path.join(ver, f))
        self.transition = read_fsm('fsm.txt', states)
        self.states = states
        self.current = 't3'

    def get_next(self):
        result = self.states[self.current]
        self.current = random.choice(self.transition[self.current])
        # return self.states[self.current]
        return result

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../uniform')))

import uniform_simple as us

class UniformTester :

    def init(self) :
        self.uf_gen = us.uniform_simple()

    def no_reset(self) :
        self.uf_gen.apply_h(0)
        self.uf_gen.apply_h(0)
        self.uf_gen.apply_h(0)

        self.uf_gen.apply_m(0)
        self.uf_gen.apply_m(0)
        self.uf_gen.apply_m(0)

        self.uf_gen.run_simulator()

        # reuse qubit 0
        self.uf_gen.apply_h(0)

        self.uf_gen.run_simulator()

        print("No reset test case complete")

    def partial_reset(self) :
        self.uf_gen.apply_h(0)
        self.uf_gen.apply_h(0)
        self.uf_gen.apply_h(0)

        self.uf_gen.apply_m(0)
        self.uf_gen.apply_m(0)
        self.uf_gen.apply_m(0)

        self.uf_gen.run_simulator()

        self.uf_gen.apply_reset(0)
        self.uf_gen.apply_reset(2)

        # use qubit 0
        self.uf_gen.apply_h(0)
        # reuse qubit 1
        self.uf_gen.apply_h(1)

        self.uf_gen.run_simulator()

        print("Partial reset test case complete")

    def reset(self) :
        self.uf_gen.apply_h(0)
        self.uf_gen.apply_h(0)
        self.uf_gen.apply_h(0)

        self.uf_gen.apply_m(0)
        self.uf_gen.apply_m(0)
        self.uf_gen.apply_m(0)

        self.uf_gen.run_simulator()

        self.uf_gen.apply_reset(0)
        self.uf_gen.apply_reset(1)
        self.uf_gen.apply_reset(2)

        # reuse qubit 0
        self.uf_gen.apply_h(0)
        # reuse qubit 1
        self.uf_gen.apply_h(1)
        # reuse qubit 2
        self.uf_gen.apply_h(2)

        self.uf_gen.run_simulator()

        print("Reset test case complete")

tester = UniformTester()
tester.init()

print("Running No Reset tests:")
tester.no_reset()

print("Running Partial Reset tests:")
tester.partial_reset()

print("Running Reset tests:")
tester.reset()

        

# case 1: no reset
# current_term = 0
# {0:[0], 1: [0], 2:[0]}
# no reset 
# current_term = 1
# {0:[0], 1: [0], 2:[0]}
# current_term and key's last value doesnt match - throw error

# case 2: partial reset 
# current_term = 0
# {0:[0], 1: [0], 2:[0]}
# reset on 0 and 2
# {0:[], 1: [0], 2:[]}
# current_term = 1
# operation on 0 and 2
# {0:[1], 1: [0], 2:[1]}
# operation on 1
# current_term and key's last value doesnt match - throw error

# case 3: reset 
# current_term = 0
# {0:[0], 1: [0], 2:[0]}
# reset on 0, 1 and 2
# {0:[], 1: [], 2:[]}
# current_term = 1
# {0:[1], 1: [1], 2:[1]}
# one more operation in same current_term 1
# current_term and key's last value match - no problem

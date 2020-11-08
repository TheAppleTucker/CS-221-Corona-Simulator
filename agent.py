import random
import collections
random.seed(0)


infectionRate = collections.defaultdict(str)
infectionRate['elderly'] = 0.01
infectionRate['middle aged'] = 0.01
infectionRate['youth'] = 0.02

class GovPolicies:
    # policies = {'Lockdown'}
    def lockdown(self, state):
        print("Lockdown")
    def limitedOpening(self, state):
        print("Limited Opening")

class Government:
    policyList = {}
    # does nothing for now
    def choosePolicy(self, action):
        return None
    def getPolicies(self):
        return 
        

class Covid:
    ''' Only action is'''
    print('not implemented yet')
    def __init__(self, i):
        self.index = i
        


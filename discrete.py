from tulip import transys, spec, synth

# Create a finite transition system
sys = transys.FTS()

# Define the states of the system
sys.states.add_from(['X0', 'X1', 'X2', 'X3', 'X4', 'X5'])
sys.states.initial.add('X0')    # start in state X0

# Define the allowable transitions
#! TODO (IF): can arguments be a singleton instead of a list?
#! TODO (IF): can we use lists instead of sets?
#!   * use optional flag to allow list as label
sys.transitions.add_comb({'X0'}, {'X1', 'X3'})
sys.transitions.add_comb({'X1'}, {'X0', 'X4', 'X2'})
sys.transitions.add_comb({'X2'}, {'X1', 'X5'})
sys.transitions.add_comb({'X3'}, {'X0', 'X4'})
sys.transitions.add_comb({'X4'}, {'X3', 'X1', 'X5'})
sys.transitions.add_comb({'X5'}, {'X4', 'X2'})

# Add atomic propositions to the states
sys.atomic_propositions.add_from({'home', 'lot'})
sys.states.add('X0', ap={'home'})
sys.states.add('X5', ap={'lot'})

env_vars = {'park'}
env_init = set()                # empty set
env_prog = '!park'
env_safe = set()                # empty set

# Augment the system description to make it GR(1)
#! TODO: create a function to convert this type of spec automatically
sys_vars = {'X0reach'}          # infer the rest from TS
sys_init = {'X0reach'}
sys_prog = {'home'}             # []<>home
sys_safe = {'(X (X0reach) <-> lot) || (X0reach && !park)'}
sys_prog |= {'X0reach'}

# Create the specification
specs = spec.GRSpec(env_vars, sys_vars, env_init, sys_init,
                    env_safe, sys_safe, env_prog, sys_prog)
ctrl = synth.synthesize('gr1c', specs, sys=sys)
####################################################
"""
from_state = 'Sinit'
inputseq = [1, 1, 1, 1, 1, 1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
for input_val in inputseq:
	inputs = {'park' : input_val}
	retval = ctrl.reaction(from_state,inputs)
	print retval
	print retval[1]['loc'] 
	from_state = retval[0];
"""
#print "hello"
#print ctrl
#print ctrl.reaction(from_state,inputs)
#return ctrl
#if not ctrl.save('discrete.png'):
	#    print(ctrl)

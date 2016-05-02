#!/usr/bin/env python
# discrete.py - example using transition system dynamics
#
# RMM, 20 Jul 2013
"""
This example illustrates the use of TuLiP to synthesize a reactive
controller for system whose dynamics are described by a discrete
transition system.
"""
#
# Note: This code is commented to allow components to be extracted into
# the tutorial that is part of the users manual.  Comments containing
# strings of the form @label@ are used for this purpose.
#

#import logging
#logging.basicConfig(level=logging.INFO)
#logging.getLogger('tulip.spec.lexyacc').setLevel(logging.WARNING)
#logging.getLogger('tulip.synth').setLevel(logging.DEBUG)
#logging.getLogger('tulip.interfaces.gr1c').setLevel(logging.DEBUG - 3)

# @import_section@
# Import the packages that we need
from tulip import transys, spec, synth
# @import_section_end@

#
# System dynamics
#
# The system is modeled as a discrete transition system in which the
# robot can be located anyplace on a 2x3 grid of cells.  Transitions
# between adjacent cells are allowed, which we model as a transition
# system in this example (it would also be possible to do this via a
# formula)
#
# We label the states using the following picture
#
#     +----+----+----+
#     | X3 | X4 | X5 |
#     +----+----+----+
#     | X0 | X1 | X2 |
#     +----+----+----+
#

# @system_dynamics_section@
# Create a finite transition system
sys = transys.FTS()

# Define the states of the system
sys.states.add_from(['X0', 'X1', 'X2', 'X3', 'X4', 'X5'])
sys.states.initial.add('X0')    # start in state X0

# Define the allowable transitions
#! TODO (IF): can arguments be a singleton instead of a list?
#! TODO (IF): can we use lists instead of sets?
#!   * use optional flag to allow list as label
sys.transitions.add_comb({'X0'}, {'X0', 'X1', 'X3'})
sys.transitions.add_comb({'X1'}, {'X1', 'X0', 'X4', 'X2'})
sys.transitions.add_comb({'X2'}, {'X2', 'X1', 'X5'})
sys.transitions.add_comb({'X3'}, {'X3', 'X0', 'X4'})
sys.transitions.add_comb({'X4'}, {'X4', 'X3', 'X1', 'X5'})
sys.transitions.add_comb({'X5'}, {'X5', 'X4', 'X2'})
# @system_dynamics_section_end@

# @system_labels_section@
# Add atomic propositions to the states
sys.atomic_propositions.add_from({'home', 'goal', 'midtop', 'midbottom'})
sys.states.add('X0', ap={'home'})
sys.states.add('X5', ap={'goal'})
sys.states.add('X4', ap={'midtop'})
sys.states.add('X1', ap={'midbottom'})
# @system_labels_section_end@

# if IPython and Matplotlib available
#sys.plot()

#
# Environment variables and specification
#

##
# @environ_section@
env_vars = {'X1reach', 'park'}
env_init = {'X1reach'}                # Obstacle at X1
env_prog = '!park'
env_safe = '!(!X1reach && (X (!X1reach)))'    # Obstacle does not stay more than one step at X4
# @environ_section_end@

#
# System specification
#
# The system specification is that the robot should repeatedly revisit
# the upper right corner of the grid while at the same time responding
# to the park signal by visiting the lower left corner.  The LTL
# specification is given by
#
#     []<> home && [](park -> <>goal)
#
# Since this specification is not in GR(1) form, we introduce the
# variable X0reach that is initialized to True and the specification
# [](park -> <>lot) becomes
#
#     [](X (X0reach) <-> lot || (X0reach && !park))
#

# @specs_setup_section@
# Augment the system description to make it GR(1)
#! TODO: create a function to convert this type of spec automatically
sys_vars = {'X0reach'}
sys_init = {'X0reach'}
sys_prog = {'home'}             # []<>home
sys_safe = {'(X (X0reach) <-> goal) || (X0reach && !park)', '!(!X1reach && midtop)', '!(X1reach && midbottom)' }
sys_prog |= {'X0reach'}
# @specs_setup_section_end@

# @specs_create_section@
# Create the specification
specs = spec.GRSpec(env_vars, sys_vars, env_init, sys_init,
                    env_safe, sys_safe, env_prog, sys_prog)
# @specs_create_section_end@

#
# Controller synthesis
#
# At this point we can synthesize the controller using one of the available
# methods.  Here we make use of gr1c.
#
# @synthesize@
ctrl = synth.synthesize('gr1c', specs, sys=sys)
# @synthesize_end@

#
# Generate a graphical representation of the controller for viewing,
# or a textual representation if pydot is missing.
#
# @plot_print@
#if not ctrl.save('turtlescenario.png'):
    #print(ctrl)
# @plot_print_end@

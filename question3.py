"""
This is the python script for question 3. In this script, you are required to implement a multi agent path-finding algorithm that also replans when agents malfunction
"""

from lib_piglet.utils.tools import eprint
from typing import List, Tuple
import glob, os, sys, time, json

# import necessary modules that this python scripts need.
try:
    from flatland.core.transition_map import GridTransitionMap
    from flatland.envs.agent_utils import EnvAgent
    from flatland.utils.controller import (
        get_action,
        Train_Actions,
        Directions,
        check_conflict,
        path_controller,
        evaluator,
        remote_evaluator,
        VisualiserOptions,
    )
except Exception as e:
    eprint("Cannot load flatland modules!")
    eprint(e)
    exit(1)


#########################
# Debugger and visualiser options
#########################

# Set debug to True for a step-by-step account of the run: what was planned,
# which agents malfunctioned or were blocked, and why each episode ended.
debug = False

# Controls the visualiser:
#   False                  -> run headless (fastest)
#   True                   -> watch the run with the default settings
#   VisualiserOptions(...) -> watch the run with your own settings, e.g.
#       VisualiserOptions(
#           delay=0.3,      # seconds to pause between timesteps; 0 runs at full speed
#           headless=False, # True: no window, serve to your browser instead
#           wait=True,      # hold the first frame until you are watching
#           port=8080,      # serve on a fixed port (headless mode)
#           cell_size=40,   # pixels per grid cell
#       )
visualizer = False

# Stop each episode after this many timesteps. None uses the test case's own
# limit.
max_steps = None

# If you want to test on specific instance, turn test_single_instance to True and specify the level and test number
test_single_instance = False
level = 0
test = 0

#########################
# Reimplement the contents of the get_path() function and the replan() function.
#
# They both return a list of paths. A path is a list of (x,y) location tuples.
# The paths should be conflict free.
# Hint, you could use some global variables to reuse resources across get_path/replan function calls.
#########################


# This function returns one path per agent as the solution.
# @param agents A list of EnvAgent.
# @param rail The flatland railway GridTransitionMap
# @param max_timestep The max timestep of this episode.
# @return path_all A list of paths, one per agent, each a list of (x,y) tuples.
def get_path(agents: List[EnvAgent], rail: GridTransitionMap, max_timestep: int):
    ############
    # Below is a dummy path finding implementation,
    # which always chooses the first available transition from the current state.
    #
    # Replace it with your implementation and return a list of paths. Each path is a list of (x,y) tuples as your plan.
    # Your plan should avoid conflicts between the paths.
    ############

    # initialize path list
    path_all = []

    # for each agent in env
    for agent_id in range(0, len(agents)):
        path = []
        loc = agents[agent_id].initial_position
        direction = agents[agent_id].initial_direction

        for t in range(0, int(max_timestep / 10)):
            # add loc to path list
            path.append(loc)
            if loc == agents[agent_id].target:
                break

            # get available transitions from Rail_Env object.
            valid_transitions = rail.get_transitions(loc[0], loc[1], direction)
            for i in range(0, len(valid_transitions)):
                if valid_transitions[i]:
                    new_x = loc[0]
                    new_y = loc[1]
                    action = i
                    if action == Directions.NORTH:
                        new_x -= 1
                    elif action == Directions.EAST:
                        new_y += 1
                    elif action == Directions.SOUTH:
                        new_x += 1
                    elif action == Directions.WEST:
                        new_y -= 1

                    conflict = False
                    for p in path_all:
                        if t + 1 < len(p) and p[t + 1] == (new_x, new_y):
                            conflict = True
                        if (
                            t + 1 < len(p)
                            and p[t + 1] == (loc[0], loc[1])
                            and p[t] == (new_x, new_y)
                        ):
                            conflict = True
                    if conflict:
                        continue

                    loc = (new_x, new_y)
                    direction = action
                    break
        path_all.append(path)

    return path_all


# This function returns one updated path per agent as the solution.
# @param agents A list of EnvAgent.
# @param rail The flatland railway GridTransitionMap
# @param current_timestep The timestep at which the malfunction/collision happens.
# @param existing_paths The existing paths from the previous get_path or replan.
# @param max_timestep The max timestep of this episode.
# @param new_malfunction_agents The ids of the agents whose malfunction started at the current timestep (does not include agents that were already malfunctioning in past timesteps)
# @param failed_agents The ids of the agents that failed to reach the location on their path at the current timestep.
# @return path_all A list of paths whose locations from current_timestep onwards are updated to handle the malfunctions and failed executions.
def replan(
    agents: List[EnvAgent],
    rail: GridTransitionMap,
    current_timestep: int,
    existing_paths: List[List[Tuple]],
    max_timestep: int,
    new_malfunction_agents: List[int],
    failed_agents: List[int],
):
    if debug:
        print("Replan function not implemented yet!", file=sys.stderr)
    return existing_paths


#####################################################################
# Instantiate a Remote Client
# You should not modify the code below, unless you want to change test_cases to test a specific instance.
#####################################################################
if __name__ == "__main__":
    if len(sys.argv) > 1:
        remote_evaluator(get_path, sys.argv, replan=replan)
    else:
        script_path = os.path.dirname(os.path.abspath(__file__))
        test_cases = glob.glob(
            os.path.join(script_path, "multi_test_case/level*_test_*.pkl")
        )
        if test_single_instance:
            test_cases = glob.glob(
                os.path.join(
                    script_path,
                    "multi_test_case/level{}_test_{}.pkl".format(level, test),
                )
            )
        test_cases.sort()
        deadline_files = [test.replace(".pkl", ".ddl") for test in test_cases]
        evaluator(
            get_path,
            test_cases,
            debug=debug,
            visualizer=visualizer,
            question_type=3,
            ddl=deadline_files,
            replan=replan,
            max_steps=max_steps,
        )

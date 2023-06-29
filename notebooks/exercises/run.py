import json
import time

import git
import numpy as np

import context_map
from walker import Walker

# Use the following parameters to simulate and save a trajectory of the walker

with open("inputs.json", 'r') as f:
    inputs = json.load(f)

seed = inputs['seed']
sigma_i = inputs['sigma_i']
sigma_j = inputs['sigma_j']
size = inputs['size']
i, j = inputs['i'], inputs['j']
n_iterations = inputs['n_iterations']
# USE map_type hills
random_state = np.random.RandomState(seed)

# STEP 1: Create a context map
context_map_builder = context_map.map_builder[inputs['map_type']]

# STEP 2: Create a Walker
context = context_map_builder(size)
walker = Walker(sigma_i, sigma_j, context_map=context)


# STEP 3: Simulate the walk
trajectory = []
for _ in range(n_iterations):
    i, j = walker.sample_next_step(i, j)
    trajectory.append((i, j))


# STEP 4: Save the trajectory
curr_time = time.strftime("%Y%m%d-%H%M%S")
# save the npy file here!

np.save( 'traj'+str(curr_time), trajectory)


# STEP 5: Save the metadata
# lookup git repository
repo = git.Repo(search_parent_directories=True)
sha = repo.head.object.hexsha

with open('meta.txt', 'w') as f:
    f.write(f'I estimated parameters at {curr_time}.\n')
    f.write(f'The git repo was at commit {sha}')
    # you can add any other information you want here!

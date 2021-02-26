from PyAnvilEditor.pyanvil import world
from pathlib import Path
import json
import math
import timeit

TIME_START_GLOBAL = timeit.default_timer()

# Load the world folder relative to the current working dir
WORLD_NAME = '21w08b'
total_r = 512
r = 128 # Split ops into these 'blocks' to save memory.
block_fac = math.floor(total_r/r)

output_path = Path('etc/'+WORLD_NAME+'__output')
output_path.mkdir(exist_ok=True)

input_path = Path('Inputs/'+WORLD_NAME)

height_range = range(-64,321)
# height_range = range(0,256)

distribution = [ {} for x in height_range ]
for blk_i in range(-block_fac,block_fac):
    for blk_k in range(-block_fac,block_fac):
        print("\n\nBLOCK ",blk_i,blk_k, flush=True)
        time_start_block = timeit.default_timer()
        with world.World(input_path, write=False) as WORLD:
            z = 0
            for j in height_range: #Adjust if you're using different worldheights.
                print(j, end=' ', flush=True)
                for i in range(-r+blk_i*r,r+blk_i*r):
                    for k in range(-r+blk_k*r,r+blk_k*r):
                        block = WORLD.get_block((i, j, k))._state.name
                        if block in distribution[z]:
                            distribution[z][block] += 1
                        else:
                            distribution[z].update({block:1})
                z += 1
            # print("\nDone iterating. ", blk_i, blk_k, 'done in', (timeit.default_timer() - time_start_block), 'seconds')
        print("\nBLOCK ", blk_i, blk_k, 'done in', (timeit.default_timer() - time_start_block), 'seconds')
    with open(output_path / Path('SUM_leq_block_'+str(blk_i)+'.'+str(blk_k)+'.json'), 'w') as file:
        file.write(json.dumps(distribution))

print('Done in', (timeit.default_timer() - TIME_START_GLOBAL), 'seconds')

with open('./RESULTS_ALL__'+WORLD_NAME+'.json', 'w') as file:
    file.write(json.dumps(distribution))

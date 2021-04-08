# -- coding: utf-8 -*-

import os
import subprocess
import multiprocessing
import argparse

GPUs = [0, 3, 5]
parser = argparse.ArgumentParser()
parser.add_argument("--result-dir", required=True)
parser.add_argument("--seed", default=20)
parser.add_argument("--save-every", required=True)
args, cfgs = parser.parse_known_args()

cfgs = [os.path.abspath(cfg) for cfg in cfgs]
common_path = os.path.commonpath(cfgs)
os.makedirs(args.result_dir, exist_ok=True)
rel_res_dirs = [os.path.relpath(cfg, common_path).replace(".yaml", "") for cfg in cfgs]
res_dirs = [os.path.join(args.result_dir, rel_dir) for rel_dir in rel_res_dirs]

for res_dir in res_dirs:
    os.makedirs(res_dir, exist_ok=True)

num_processes = len(GPUs)
print("Num process: {}. Num exp: {}. Would save to: {}".format(num_processes, len(cfgs), res_dirs))

queue = multiprocessing.Queue(maxsize=num_processes)
def _worker(p_id, gpu_id, queue):
    while 1:
        token = queue.get()
        if token is None:
            break
        cfg_file, res_dir = token
        # os.makedirs(res_dir, exist_ok=True)
        # log_file = os.path.join(res_dir, "search_tail.log")
        cmd = ("awnas search {} --gpu {} --seed {} --save-every {} --train-dir {}"
               " >/dev/null 2>&1").format(
                   cfg_file, gpu_id, args.seed, args.save_every, res_dir) #, log_file)
        print("Process #{}: cfg {}; CMD: {}".format(p_id, cfg_file, cmd))
        subprocess.check_call(cmd, shell=True)
    print("Process #{} end".format(p_id))

for p_id in range(num_processes):
    p = multiprocessing.Process(target=_worker, args=(p_id, GPUs[p_id], queue))
    p.start()

for cfg, res_dir in zip(cfgs, res_dirs):
    queue.put((cfg, res_dir))

# close all the workers
for _ in range(num_processes):
    queue.put(None)

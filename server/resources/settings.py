INSTANCES = ["inst0", "inst1", "inst2", "inst3", "inst4", "inst5", "inst6", "inst7", "inst8", "inst9", "inst10"]

GPUS = ["gpu0", "gpu1", "gpu2", "gpu3", "gpu4", "gpu5", "gpu6", "gpu7"]

PORTS = list(range(20000, 20000 + len(INSTANCES)))

from .instance import Instance
from .gpu import GPU

PRE_CREATED_INSTANCES = [Instance(None, name, -1, 10, port=port) for name, port in zip(INSTANCES, PORTS)]

ALL_GPUS = [GPU(gid) for gid in range(len(GPUS))]

def exceed_user_quota(insts):
  if len(insts) >= 3:
    return True
  else:
    total_gpu_num = sum([inst.gpu_num for inst in insts])
    if total_gpu_num >= 4:
      return True
  return False

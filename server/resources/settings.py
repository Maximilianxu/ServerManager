INSTANCES = ["inst0", "inst1", "inst2", "inst3", "inst4", "inst5", "inst6", "inst7", "inst8", "inst9", "inst10"]

GPUS = ["gpu0", "gpu1", "gpu2", "gpu3", "gpu4", "gpu5", "gpu6", "gpu7"]

USER_NUMBERS = ['mg20330044', 'DZ20330026', 'MF20330103', 'mg1601001', 'MF21330106', 'MF21330073', 'MG20330031', 'dz1633008', 'DZ1833029', 'MG20330041', 'MG21330005', 'DZ1733020', 'DZ1933025', 'MF20330068', 'MG21330053', 'mf20330099', "UNKNOWN", "MF21330063", "MF20330068"]

# prof. wang students
WW_GROUP = ['DZ1833029', 'MF20330103', 'DZ1733020', 'mf20330099', 'mg20330044', 'DZ1933025', 'MG21330005', 'MF21330106']

GROUP_TOTAL_QUOTA = 4

PORTS = list(range(20000, 20000 + len(INSTANCES)))

from .instance import Instance
from .gpu import GPU

PRE_CREATED_INSTANCES = [Instance(None, name, -1, 10, port=port) for name, port in zip(INSTANCES, PORTS)]

ALL_GPUS = [GPU(gid) for gid in range(len(GPUS))]

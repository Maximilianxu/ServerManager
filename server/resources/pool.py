import json
import copy
from .instance import Instance
from .gpu import GPU
from .user import User
from utils import DB, dumper, allocate_gpu_for_instance, \
  free_all_gpu_of_instance, change_password, get_random_password
from .settings import GROUP_TOTAL_QUOTA, PRE_CREATED_INSTANCES, ALL_GPUS, USER_NUMBERS, WW_GROUP

GPU_NUM = 8
alloc_res_col = DB["alloc_res"]
wait_res_col = DB["wait_res"]

class Pool:
  def __init__(self) -> None:
    pass
  
  @classmethod
  def allocated_resources(cls, gpu=True):
    alloc_res = alloc_res_col.find()
    if gpu:
      gpus = []
      for inst_data in alloc_res:
        inst_gpu_data = inst_data["gpus"]
        gpus.extend([GPU.from_json(i) for i in inst_gpu_data])
      return gpus
    else:
      insts = []
      for inst_data in alloc_res:
        inst = Instance.from_json(inst_data)
        insts.append(inst)
      return insts
  
  @classmethod
  def busy_instances(cls, user=None):
    query_params = {"user.id_number": user.id_number} if user is not None else {}
    busy_insts = []
    wait_insts = wait_res_col.find(query_params)
    for inst_data in wait_insts:
      inst = Instance.from_json(inst_data)
      busy_insts.append(inst)
    alloc_insts = alloc_res_col.find(query_params)
    for inst_data in alloc_insts:
      inst = Instance.from_json(inst_data)
      busy_insts.append(inst)
    return busy_insts
  
  @classmethod
  def exceed_group_quota(cls, user, alloc_gpu_num):
    if alloc_gpu_num == 0:
      return False
    all_insts = cls.busy_instances()
    is_ww_group = user.id_number in WW_GROUP
    print("is ww group:", is_ww_group)
    ww_alloc, dhp_alloc = alloc_gpu_num, alloc_gpu_num
    for inst in all_insts:
      if is_ww_group and inst.user.id_number in WW_GROUP:
        print("busy inst:", inst.user.id_number, inst.gpu_num, inst.user.name, ww_alloc)
        ww_alloc += inst.gpu_num
        if ww_alloc > GROUP_TOTAL_QUOTA:
          return True
      elif not is_ww_group and inst.user.id_number not in WW_GROUP:
        dhp_alloc += inst.gpu_num
        if dhp_alloc > GROUP_TOTAL_QUOTA:
          return True
    return False

  @classmethod
  def exceed_user_quota(cls, user, alloc_gpu_num):
    insts = cls.busy_instances(user)
    if len(insts) >= 4:
      return True
    else:
      if alloc_gpu_num == 0:
        return False
      total_gpu_num = sum([inst.gpu_num for inst in insts])
      if total_gpu_num + alloc_gpu_num > 4:
        return True
    return False

  @classmethod
  def idle_resources(cls, gpu=True):
    allocated_resources = cls.allocated_resources(gpu=gpu)
    print("allocated:", *allocated_resources)
    if gpu:
      idle_res = []
      for res in ALL_GPUS:
        if res not in allocated_resources:
          idle_res.append(res)
      return idle_res
    else:
      idle_res = []
      for res in PRE_CREATED_INSTANCES:
        if res not in allocated_resources:
          idle_res.append(res)
      return idle_res

  @classmethod
  def put_instance(cls, user, inst_name, gpu_num):
    busy_insts = cls.busy_instances()
    if inst_name in busy_insts:
      return False
    inst_idx = PRE_CREATED_INSTANCES.index(inst_name)
    instance = copy.copy(PRE_CREATED_INSTANCES[inst_idx])
    instance.status = "wait"
    instance.user = user
    instance.gpu_num = gpu_num
    if gpu_num <= 1:
      instance.left_time = 15
    wait_res_col.insert_one(json.loads(json.dumps(instance, default=dumper, indent=2)))
    return True
  
  @classmethod
  def free_instance(cls, inst_name):
    inst_idx = PRE_CREATED_INSTANCES.index(inst_name)
    instance = PRE_CREATED_INSTANCES[inst_idx]
    alloc_res_col.delete_one({"name": instance.name})
    wait_res_col.delete_one({"name": instance.name})
    free_all_gpu_of_instance(inst_name)
    change_password(inst_name, get_random_password(length=8))
  
  @classmethod
  def share_instance(cls, inst_name, target_id_number):
    print("share", inst_name)
    if target_id_number not in USER_NUMBERS:
      raise RuntimeError("unknown target user!")
    target_user = User.from_id_number(target_id_number)
    inst = alloc_res_col.find_one({"name": inst_name})
    inst = Instance.from_json(inst)
    if inst.user.id_number == target_id_number:
      raise RuntimeError("same user cannot be shared")
    if target_id_number in inst.shares:
      raise RuntimeError("has already been shared, do not operate repeatedly")
    inst.shares.append(target_id_number)
    alloc_res_col.update_one({"name": inst_name}, {"$set": {"shares": json.loads(json.dumps(inst.shares, default=dumper, indent=2))}})

  @classmethod
  def applied_instances(cls, user):
    insts = []
    alloc_inss = alloc_res_col.find()
    for ins in alloc_inss:
      inst = Instance.from_json(ins)
      if inst.user == user or user.id_number in inst.shares:
        insts.append(inst)
    wait_inss = wait_res_col.find({"user.id_number": user.id_number})
    insts.extend([Instance.from_json(ins) for ins in wait_inss])
    return insts

  # this method should be invoked after each time of calling put_ or free_ instance
  @classmethod
  def try_allocate(cls):
    idle_res = cls.idle_resources()
    print("idle:", *idle_res)
    wait_insts = list(wait_res_col.find())
    wait_insts = list(map(lambda ins: Instance.from_json(ins), wait_insts))
    
    if len(wait_insts) > 0:
      # roll over the queue to check which instance can be filled
      alloc_inst_idx = -1
      for inst_idx, inst in enumerate(wait_insts):
        if int(inst.gpu_num) <= len(idle_res):
          if inst.gpu_num > 0:
            print("allocate:", *idle_res[:int(inst.gpu_num)])
            inst.fill_gpus(*idle_res[:int(inst.gpu_num)])
            allocate_gpu_for_instance(inst.name, idle_res[:int(inst.gpu_num)])
          new_password = change_password(inst.name, get_random_password(length=8))
          alloc_inst_idx = inst_idx
          break
      if alloc_inst_idx > -1:
        alloc_inst = wait_insts[alloc_inst_idx]
        alloc_inst.status = "allocated"
        alloc_inst.password = new_password
        alloc_res_col.insert_one(json.loads(json.dumps(alloc_inst, default=dumper, indent=2)))
        wait_res_col.delete_one({"name": alloc_inst.name})
      if alloc_inst_idx > -1:
        return True
    return False

#def update_instance_left_time():
#  print("update left time")
#  alloc_res = alloc_res_col.find()
#  for inst_data in alloc_res:
#    inst = Instance.from_json(inst_data)
#    left_time = inst.left_time
#    if left_time <= 0:
#      Pool.free_instance(inst.name)
#    else:
#      update = { "$set": { "left_time": left_time - 1} }
#      alloc_res_col.update_one({"name": inst.name}, update)
#
#from threading import Thread, Event
#
#class TimerThread(Thread):
#  def __init__(self, interval, event):
#    Thread.__init__(self)
#    self.interval = interval
#    self.stopped = event
#
#  def run(self):
#    while not self.stopped.wait(self.interval):
#      update_instance_left_time()

# s.repeat_on_days('MTWTFSS', time(0, 0), 0, update_instance_left_time)
#stopFlag = Event()
#thread = TimerThread(3600 *24, stopFlag)
#thread.start()

from .user import User
from .gpu import GPU

class Instance:
  max_timespan = 10
  def __init__(self, user, inst_name, wait_gpu_num, timespan, priority=10, gpus=[], status="free", \
    port=20000, password="root") -> None:
    if timespan > self.max_timespan:
      raise RuntimeError("timespan exceeds the limit")
    self.user = user
    self.name = inst_name
    self.gpu_num = wait_gpu_num
    self.left_time = timespan
    self.priority = priority
    self.gpus = gpus
    self.status = status
    self.password = password
    self.port = port

  @classmethod
  def from_json(cls, json_str):
    return Instance(User.from_json(json_str["user"]), json_str["name"], \
      int(json_str["gpu_num"]), int(json_str["left_time"]), int(json_str["priority"]), \
      [GPU.from_json(g) for g in (json_str["gpus"])], json_str["status"], \
      int(json_str["port"]), json_str["password"])

  def fill_gpus(self, *args):
    self.gpus.extend(args)

  def __eq__(self, o: object) -> bool:
    if isinstance(o, Instance):
      return self.name == o.name
    else:
      return self.name == o

  def __gt__(self, o):
    return self.priority > o.priority
  
  def __lt__(self, o):
    return self.priority < o.priority
  
  def __ge__(self, o):
    return self.priority >= o.priority

  def __le__(self, o):
    return self.priority <= o.priority
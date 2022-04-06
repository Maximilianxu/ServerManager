from resources import *

def update_instance_left_time():
  print("update left time")
  alloc_res = alloc_res_col.find()
  for inst_data in alloc_res:
    inst = Instance.from_json(inst_data)
    left_time = inst.left_time
    if left_time <= 0:
      Pool.free_instance(inst.name)
    else:
      update = { "$set": { "left_time": left_time - 1} }
      alloc_res_col.update_one({"name": inst.name}, update)

from threading import Thread, Event

class TimerThread(Thread):
  def __init__(self, interval, event):
    Thread.__init__(self)
    self.interval = interval
    self.stopped = event

  def run(self):
    while not self.stopped.wait(self.interval):
      update_instance_left_time()

# s.repeat_on_days('MTWTFSS', time(0, 0), 0, update_instance_left_time)
stopFlag = Event()
thread = TimerThread(3600 *24, stopFlag)
thread.start()


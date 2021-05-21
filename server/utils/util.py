import numpy as np
import subprocess
import random
import string

PCI_INFO = ["0000:1a:00.0", "0000:1b:00.0", \
  "0000:3d:00.0", "0000:3e:00.0", \
  "0000:88:00.0", "0000:89:00.0", \
  "0000:b1:00.0", "0000:b2:00.0"]

sudo_password = "blabla"

def allocate_gpu_for_instance(inst_name, gpu_list):
  passwd_cmd = "echo {}".format(sudo_password)
  pswd = subprocess.run(passwd_cmd.split(" "), check=True, capture_output=True)
  cmd_tplt = "sudo lxc config device add {} gpu{} gpu pci={}"
  for gpu in gpu_list:
    gid = gpu.gid
    cmd = cmd_tplt.format(inst_name, gid, PCI_INFO[gid])
    print("exec", cmd)
    subprocess.run(cmd.split(" "), input=pswd.stdout)

def free_all_gpu_of_instance(inst_name):
  list_dev_cmd_tplt = "sudo lxc config device list {}"
  free_dev_cmd_tplt = "sudo lxc config device remove {} {}"
  passwd_cmd = "echo {}".format(sudo_password)
  pswd = subprocess.run(passwd_cmd.split(" "), check=True, capture_output=True)
  devs = subprocess.run(list_dev_cmd_tplt.format(inst_name).split(" "), \
    capture_output=True, input=pswd.stdout).stdout.decode().split("\n")
  for dev in devs:
    if dev != "" and "gpu" in dev:
      cmd = free_dev_cmd_tplt.format(inst_name, dev)
      print("exec", cmd)
      subprocess.run(cmd.split(" "))

def change_password(inst_name, new_password):
  passwd_cmd = "echo {}\n{}".format(new_password, new_password)
  pswd = subprocess.run(passwd_cmd.split(" "), check=True, capture_output=True)
  print("echo output:", pswd.stdout.decode())
  cmd_tplt = "lxc exec {} -- passwd ubuntu"
  cmd = cmd_tplt.format(inst_name)
  print("exec", cmd)
  subprocess.run(cmd.split(" "), input=pswd.stdout)
  return new_password

def get_random_password(length=8):
  # With combination of lower and upper case
  result_str = ''.join(random.choice(string.ascii_letters) for _ in range(length))
  # print random string
  return result_str

def dumper(obj):
  if "toJSON" in dir(obj):
    return obj.toJSON()
  if "__dict__" in dir(obj):
    return obj.__dict__
  if isinstance(obj, (np.int, np.int32)):
    return int(obj)
  if isinstance(obj, (np.float, np.float32)):
    return float(obj)
  return str(obj)

import pymongo
dbclient = pymongo.MongoClient("mongodb://127.0.0.1:27017")
DB = dbclient["server_management"]
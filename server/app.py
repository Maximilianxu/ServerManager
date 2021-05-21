from copy import copy
from flask import Flask, request
import json
from flask_cors import CORS
from utils import dumper
from resources import *

DEBUG = True

app = Flask(__name__)
app.config.from_object(__name__)

CORS(app, resources={r"/*": {"origins": '*'}})

def request_user(request):
  token = request.headers["Authorization"]
  if token != "":
    users = User.user_list()
    user = users[users.index(User(token))]
  else:
    user = None
  return user

@app.route("/profile", methods=["GET", "POST"])
def get_profile():
  profile = {}
  user = request_user(request)
  if user is not None:
    profile["name"] = user.name
    profile["id_number"] = user.id_number
    # Add other info
    pass
  return profile

@app.route("/instances", methods=["GET", "POST"])
def all_instances():
  post_data = request.get_json()
  page_num = post_data["pageNum"]
  page_size = post_data["pageSize"]
  response_object = {}
  busy_insts = Pool.busy_instances()
  all_insts = copy.copy(PRE_CREATED_INSTANCES)
  ret_insts = []
  for inst in all_insts:
    if inst in busy_insts:
      ret_insts.append(busy_insts[busy_insts.index(inst)])
    else:
      ret_insts.append(inst)
  response_object["data"] = json.dumps(ret_insts[page_size * (page_num - 1): page_size * page_num], \
    default=dumper, indent=2)
  response_object["total"] = len(ret_insts)
  return response_object

@app.route("/applied", methods=["GET", "POST"])
def applied_instances():
  user = request_user(request)
  applied_instances = Pool.applied_instances(user)
  post_data = request.get_json()
  page_num = post_data["pageNum"]
  page_size = post_data["pageSize"]
  response_object = {}
  response_object["data"] = json.dumps(applied_instances[page_size * (page_num - 1): page_size * page_num], \
    default=dumper, indent=2)
  response_object["total"] = len(applied_instances)
  return response_object

@app.route("/apply", methods=["POST"])
def apply_instance():
  response_object = {}
  post_data = request.get_json()
  print(post_data)
  user = request_user(request)
  inst_id = post_data.get("name")
  alloc_gpu_num = post_data.get("gpu_num")
  if alloc_gpu_num >= 0:
    user_busy_insts = Pool.busy_instances(user)
    if exceed_user_quota(user_busy_insts):
      response_object['message'] = "You already applied over 3 instances or 4 GPUs"
    else:
      Pool.put_instance(user, inst_id, alloc_gpu_num)
      alloc_success = Pool.try_allocate()
      if alloc_success:
        response_object['message'] = 'GPUs applied success'
      else:
        response_object['message'] = 'Waiting for allocation'
  else:
    response_object['message'] = "Invalid GPU number, please select a configiration manually"
  # except Exception as e:
  #   response_object['message'] = str(e)
  return response_object

@app.route("/release", methods=["DELETE"])
def release_instance():
  response_object = {}
  data = request.get_json()
  # try:
  inst_name = data.get("name")
  Pool.free_instance(inst_name)
  response_object["message"] = "GPUs released sucess"
  # except Exception as e:
  #   response_object["message"] = str(e)
  return response_object

@app.route("/auth/signup", methods=["PUT", "POST"])
def register():
  response_obj = {"message": "success"}
  data = request.get_json()
  id_number = data.get("id_number")
  user_name = data.get("name")
  password = data.get("password")
  try:
    print("begin regist")
    User.add_user(id_number, user_name, password)
    print("registration finished")
  except Exception as e:
    print(e)
    response_obj["message"] = str(e)
  return response_obj

@app.route("/auth/login", methods=["POST"])
def login():
  response_obj = {"message": "success", "token": ""}
  data = request.get_json()
  id_number = data.get("id_number")
  password = data.get("password")
  user_list = User.user_list()
  if User(id_number) in user_list:
    record_password = user_list[user_list.index(User(id_number))].password
    if record_password != password:
      response_obj["message"] = "failed"
    else:
      response_obj["token"] = id_number
  else:
    response_obj["message"] = "failed"
  print("login response", response_obj)
  return response_obj

@app.after_request
def after_request(response):
  header = response.headers
  header['Access-Control-Allow-Origin'] = '*'
  header['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
  header['Access-Control-Allow-Methods'] = 'OPTIONS, HEAD, GET, POST, DELETE, PUT'
  return response

if __name__ == "__main__":
  app.run()

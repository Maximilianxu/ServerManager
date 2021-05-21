import os
from utils import *
import json
import hashlib

user_col = DB["users"]
class User:
  def __init__(self, id_number, name='', password='') -> None:
    self.id_number = id_number
    self.name = name
    self.password = password
  
  @classmethod
  def from_json(cls, json_str):
    return User(json_str["id_number"], json_str["name"], json_str["password"])

  def __hash__(self) -> int:
    return hash(self.id_number)

  def __eq__(self, o) -> bool:
    return self.id_number == o.id_number
  
  def __str__(self) -> str:
    return str({"id:": self.id_number, "name": self.name})
  
  @classmethod
  def user_list(cls):
    user_data = user_col.find()
    users = [cls.from_json(u) for u in user_data]
    return users

  @classmethod
  def add_user(cls, id_number, name, password):
    new_user = {"id_number": id_number, "name": name, "password": password}
    user_col.insert_one(new_user)
  
  @classmethod
  def update_user(cls, id_number, **kwargs):
    newvalues = { "$set": kwargs}
    user_col.update_one({"id_number": id_number}, newvalues)

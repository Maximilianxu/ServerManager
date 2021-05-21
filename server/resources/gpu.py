class GPU:
  def __init__(self, gid) -> None:
    self.gid = gid
  
  def __eq__(self, o: object) -> bool:
    return self.gid == o.gid

  def __str__(self) -> str:
    return "GPU-" + str(self.gid)
  
  @classmethod
  def from_json(cls, json_str):
    return GPU(int(json_str["gid"]))
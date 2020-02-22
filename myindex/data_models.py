from pathlib import Path
from typing import Dict, Union
from pydantic import BaseModel

from cored import CfgObj


class NodeInfo:
    pass


class DirInfo:
    name: str = ''
    path: str = ''
    nodes_cnt: int = 0
    nodes_map: Dict[str, str] = {}

    @staticmethod
    def from_path(path):
        path = Path(path)
        info = DirInfo()
        info.name = path.name
        info.path = str(path.absolute())
        info.nodes_map = {it.name: it.name for it in path.iterdir()}
        info.nodes_cnt = len(info.nodes_map)


class Wdir:

    def __init__(self, path):
        self.path = Path(path)

    def get_info(self, cfg: CfgObj):
        info = DirInfo.from_path(self.path)
        return info

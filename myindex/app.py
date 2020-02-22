from pathlib import Path
# from pydantic

import fire
import logging

from cored import CfgObj, process_dir
from pycomfy import make_cfg_bond, make_cfg_bond_dict

_me_p = Path(__file__)
_log = logging.getLogger(f"{_me_p.parent.name}.{_me_p.name}")


class CfgClass:
    env = 'base'


def start_index(cfg: CfgObj = None, start_dir=None):
    cfg.indexed.mkdir(parents=True, exist_ok=True)
    cfg.workdir.mkdir(parents=True, exist_ok=True)
    start_p = Path(start_dir)
    res = process_dir(start_p)
    cfg.write_dir_data(res, start_p)

    # Path(start_dir).iterdir()
    # cfg.indexed



def tx(cfg: CfgObj = None):
    path = Path('/Users/ivanne/wss/pers/pydocflow')
    root = path
    for x in path.iterdir():
        rel = x.relative_to(root)
        if x.name in cfg.exclude:
            continue
        if x.is_dir()
        print(rel)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    Cli = make_cfg_bond_dict(CfgObj, globals())
    fire.Fire(Cli)

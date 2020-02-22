import os
import time
from functools import cmp_to_key
from pathlib import Path


class Consts:
    indexed_dir = '_myindex_rdir'
    workdir = '_myindex_wdir'


class CfgObj:
    def __init__(self, indexed=None, workdir=None, **kw):
        self.indexed = indexed or Path.home() / Consts.indexed_dir
        self.workdir = workdir or Path.home() / Consts.workdir
        self.exclude = kw.pop("exclude", None) or [
            '.venv',
            '.git',
            '.DS_Store'
        ]

    def write_dir_data(self, data, path: Path):
        dest_sys_p = self.indexed / str(path.absolute())[1:] / '_@_sysidx'
        dest_sys_p.mkdir(parents=True, exist_ok=True)
        for k, v in data:
            dest_p = dest_sys_p / k
            dest_p.write_text(str(v))


def process_dir(path: Path):
    import os
    import datetime
    mtime_v = path.stat().st_mtime
    mtime_h = datetime.datetime.utcfromtimestamp(mtime_v).strftime('%Y-%m-%dT%H-%M-%S')
    res = [('mtime_v.txt', mtime_v),
           ('mtime_h.txt', mtime_h)]
    print(res)

    return res


# def process_dir_flat(cfg: CfgObj, path: Path, acc=None):
#     if not isinstance(path, Path):
#         path = Path(path)
#     items = path.iterdir()
#     all_cnt  = sum(1 for _ in items)
#     dirs_cnt  = sum(1 for it in items if it.is_dir())
#     for p in items:
#         if p.is_dir()
#
#
# def process_dir2(cfg: CfgObj, path: Path):
#     if not isinstance(path, Path):
#         path = Path(path)
#     items = path.iterdir()
#     for p in items:
#         if p.is_dir()
#
class Tractor:
    def on_file(self):
        pass

    def on_node(self):
        pass


def traverce_dir(path: Path, exceptions=None, dresd=None):
    exceptions = exceptions or [
        '.git',
        '.venv',
        'out',
        '.vscode',
        '.idea',
        '.egg',
        '.eggs',
        '.pytest_cache',
        '__pycache__',
        '.DS_Store'
    ]
    if path.is_file():
        dres = {}
        diff = {}
        diff['node_type'] = 'file'
        diff['name'] = path.name
        diff['file_type'] = path.suffix
        diff['size'] = path.stat().st_size
        diff['child_cnt'] = 1
        if dresd is not None:
            dresd.update(diff)
        dres.update(diff)

    elif path.is_dir():
        dres = {'data': {}}
        for it in path.iterdir():
            if it.name in exceptions:
                continue
            dres['data'][it.name] = {}
            yield from traverce_dir(it, dresd=dres['data'][it.name])
        diff = {}
        dsize = sum(v['size'] for k, v in dres['data'].items())
        diff['size'] = dsize
        diff['child_cnt'] = sum(v.get('child_cnt', 0) for v in dres['data'].values())
        diff['name'] = path.name
        diff['node_type'] = 'node'
        diff['file_type'] = '__dir'
        if all(v['node_type'] == 'file' for v in dres['data'].values()):
            diff['node_type'] = 'leaf'

        if dresd is not None:
            dresd.update(diff)
        dres.update(diff)

        def _key(x):
            return  '_' if x[1]['file_type'] == '__dir' else '__' + '_' + x[1]['name']

        dres['data'] = dict(sorted(dres['data'].items(), key=_key))
    else:
        raise ValueError()

    if 'node_type' not in dres:
        print(dres)
    yield path, dres


TEST_DIR = '/Users/ivanne/wss/pers/pydocflow'


def test__process_dir():
    the_path = Path(TEST_DIR)
    cfg = CfgObj()
    dest_p = cfg.indexed / str(the_path.absolute())[1:] / '_idx_flat'
    type_p = cfg.indexed / str(the_path.absolute())[1:] / '_idx_type'
    dest_p.mkdir(parents=True, exist_ok=True)
    type_p.mkdir(parents=True, exist_ok=True)

    from ruamel.yaml import  YAML
    yaml = YAML()
    for path, content in traverce_dir(the_path):
        # path: Path

        rel_p = path.relative_to(the_path)
        name = '@' + str(rel_p).replace("/", "@") + '@' + '.yml'
        pp = dest_p / name
        with pp.open('w') as fp:
            yaml.dump(content, fp)
            print(pp)
        if 'node_type' not in content:
            print(content)
        nn = f"{content['node_type']}@{content['file_type']}{name}"
        try:
            os.symlink(f'../_idx_flat/{name}', str(type_p / nn))
        except Exception as ex:
            print(ex)


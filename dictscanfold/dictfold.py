import datetime
import logging
import os
from functools import partial
from pathlib import Path
from pprint import pprint

from ruamel.yaml import YAML

yaml = YAML()


def traverse(doc, on_node=None, path=None):
    path = path or []
    if isinstance(path, str):
        path = [path]

    for k, v in doc.items():
        the_path = path + [k]
        if isinstance(v, dict):
            on_node(the_path, v, ntype='node')
            traverse(v, on_node=on_node, path=the_path)
        else:
            on_node(the_path, v, ntype='leaf')
    return path


def traversex(doc, on_node=None, path=None, actions=None):
    path = path or []
    actions = actions or []

    if isinstance(path, str):
        path = Path(path)
    if isinstance(path, Path):
        path = list(path.parts)

    for k, v in doc.items():
        the_path = path + [k]
        if isinstance(v, dict):
            cmd = on_node(the_path, v, ntype='node')
            actions.append(cmd)
            traversex(v, on_node=on_node, path=the_path, actions=actions)
        else:
            cmd = on_node(the_path, v, ntype='leaf')
            actions.append(cmd)
    return actions




def test__traverse_simple():
    doc = {'out': {'mf.txt': "", 'tmp': {'be.txt': '123d'}}}
    actions = []

    def register(p, v, **kw):
        ntype = kw.pop('ntype')
        path_p = Path('/'.join(p))
        if ntype == 'leaf':
            cmd = f"touch {path_p}"
        elif ntype == 'node':
            cmd = f"mkdir -p {path_p}"
        else:
            raise ValueError(ntype)
        actions.append(cmd)

    traverse(doc, on_node=register, path='.')

    pprint(actions)


def test__traverse_smart(force_content=False):
    doc = {'out': {'mf.txt': "", 'tmp': {'be.txt': '123d'}}}

    actions = []
    if force_content:
        prefix = " "
    else:
        prefix = "test -f {filepath} || "

    create_tmpl = prefix + """ cat << EOF > {filepath} 
        {content}
    """

    def register(p, v, **kw):
        ntype = kw.pop('ntype')
        path_p = Path('/'.join(p))
        if ntype == 'leaf':
            cmd = create_tmpl.format(filepath=str(path_p), content=v)
        elif ntype == 'node':
            cmd = f"mkdir -p {path_p}"
        else:
            raise ValueError(ntype)
        actions.append(cmd)

    traverse(doc, on_node=register, path='.')

    for cmd in actions:
        print(cmd)
        os.system(cmd)


def write_if_new(path=None, content=None, force_write=False):
    pp = Path(path)
    if force_write or not pp.exists():
        pp.write_text(content)
        return 1
    return 0


def ensure_dir(path=None, content=None, force_write=False):
    need_create = 0 if Path(path).exists() else 1
    Path(path).mkdir(parents=True, exist_ok=True)
    return need_create


def get_test_dir():
    me_parent: Path = Path(__file__).parent
    tid = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H-%M-%S.%f')
    test_dir = me_parent / 'out' / tid
    test_dir.mkdir(parents=True, exist_ok=True)
    return test_dir


def node_to_action(p, v, **kw):
    ntype = kw.pop('ntype')
    path_p = Path('/'.join(p))
    if ntype == 'leaf':
        cmd = partial(write_if_new, path=path_p,
                      content=v,
                      force_write=kw.get('force_write', False))
    elif ntype == 'node':
        cmd = partial(ensure_dir, path=path_p)
    else:
        raise ValueError(ntype)
    return cmd


def test__traversex_extrasmart():
    doc = {'mf.txt': "", 'tmp': {'be.txt': '123d'}}
    out_p = get_test_dir()
    on_node = partial(node_to_action, force_write=False)
    actions = traversex(doc, on_node=on_node, path=list(out_p.parts))

    for cmd in actions:
        print(cmd)
        cmd()
        # os.system(cmd)

def read_doc_from_file(path):

    with Path(path).open() as fp:
        doc = yaml.load(fp)
        return doc

def scanfold(src, dest='.', force_write=False, root='root'):
    doc_h = read_doc_from_file(src)
    doc = doc_h[root]
    actions = traversex(
        doc,
        on_node=partial(node_to_action, force_write=force_write),
        path=dest)
    for func in actions:
        nchanges = func()
        logging.info(f"Got nchanges={nchanges} from: {func}")


def test___scanfold():
    me_par: Path = Path(__file__).parent
    src_p = me_par.joinpath('data4tests/scanfold_pydocflow.yml')
    tdir = get_test_dir()
    scanfold(str(src_p), dest=str(tdir))
    print(tdir)


# if __name__ == '__main__':
#     fire.Fire()
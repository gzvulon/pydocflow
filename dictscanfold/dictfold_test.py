import datetime
import logging
from pathlib import Path
from dictscanfold import dictfold


def get_test_dir():
    me_parent: Path = Path(__file__).parent
    tid = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H-%M-%S.%f')
    test_dir = me_parent / 'out' / tid
    test_dir.mkdir(parents=True, exist_ok=True)
    return test_dir


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

    dictfold.traverse_dictdir(doc, on_node=register, path='.')
    print(actions)


def test__traversex_extrasmart():
    from functools import partial
    doc = {'mf.txt': "", 'tmp': {'be.txt': '123d'}}
    out_p = get_test_dir()
    on_node = partial(dictfold.node_to_action, force_write=False)
    actions = dictfold.traverse_dictdir(doc, on_node=on_node, path=list(out_p.parts))
    for cmd in actions:
        print(cmd)


def test___scanfold():
    import shutil
    me_par: Path = Path(__file__).parent
    src_p = me_par.joinpath('data4tests/scanfold_pydocflow.yml')
    tdir = get_test_dir()

    changes1 = dictfold.scanfold(str(src_p), dest=str(tdir))
    assert changes1
    changes2 = dictfold.scanfold(str(src_p), dest=str(tdir))
    assert changes2 == 0

    shutil.rmtree(str(tdir / 'tests'))
    changes3 = dictfold.scanfold(str(src_p), dest=str(tdir))
    assert 0 < changes3 < changes1
    logging.info(f"test changes: {[changes1, changes2, changes3]}")


def test___scanfold_dry_script():
    me_par: Path = Path(__file__).parent
    src_p = me_par.joinpath('data4tests/scanfold_pydocflow.yml')
    changes1 = dictfold.scanfold_dry(str(src_p), dest='.').make_bash_script()
    assert changes1
    assert 'test -f tests/actors/run_tests.sh' in changes1
    assert 'mkdir -p tests' in changes1


if __name__ == '__main__':
    import fire
    fire.Fire()

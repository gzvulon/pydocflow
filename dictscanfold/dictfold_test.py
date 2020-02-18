import datetime
import logging
import os
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


def test___scanfold_structure():
    doc = {'mf.txt': "", 'ver.yml': "version: '1.3'", 'tmp': {'be.txt': '123d'}}
    tdir = get_test_dir()

    changes1 = dictfold.scanfold(doc, dest=str(tdir), root=None)

    assert changes1 == 4
    assert (tdir / 'mf.txt').exists()
    assert (tdir / 'mf.txt').read_text() == ""

    assert len([it for it in (tdir / 'tmp').iterdir()]) == 1
    assert (tdir / 'tmp' / 'be.txt').read_text() == '123d'
    assert (tdir / 'ver.yml').read_text() == "version: '1.3'"

    (tdir / 'mf.txt').write_text('DIRTY')
    (tdir / 'ver.yml').unlink()

    changes2 = dictfold.scanfold(doc, dest=str(tdir), root=None)
    assert changes2 == 1
    assert (tdir / 'mf.txt').read_text() == "DIRTY"
    assert (tdir / 'ver.yml').read_text() == "version: '1.3'"


def test___scanfold_bash_shell():
    doc = {'mf.txt': "", 'ver.yml': "version: '1.3'", 'tmp': {'be.txt': '123d', 'de.txt':'1\n\2'}}
    tdir = get_test_dir()

    changes1 = dictfold.scanfold(doc, dest=str(tdir), root=None, bash_shell=True)

    # assert changes1 == 4
    assert (tdir / 'mf.txt').exists()
    assert (tdir / 'ver.yml').read_text().strip() == "version: '1.3'"

    assert len([it for it in (tdir / 'tmp').iterdir()]) == 2
    assert (tdir / 'tmp' / 'be.txt').read_text().strip() == '123d'

    (tdir / 'mf.txt').write_text('DIRTY')
    (tdir / 'ver.yml').unlink()

    changes2 = dictfold.scanfold(doc, dest=str(tdir), root=None, bash_shell=True)
    # assert changes2 == 1
    assert (tdir / 'mf.txt').read_text() == "DIRTY"
    assert (tdir / 'ver.yml').read_text().strip() == "version: '1.3'"


def test___scanfold_bash_script():
    doc = {'mf.txt': "", 'ver.yml': "version: '1.3'",
           'tmp': {'be.txt': '123d', 'de.txt':'1\n\n   2\n'}}
    tdir = get_test_dir()

    unfold_script = dictfold.scanfold(doc, dest='.', root=None, bash_script=True)
    script = "\n\n".join([
        '#!/bin/bash',
        '# --- AUTOGENERATED --',
        unfold_script
    ])
    (tdir / 'unfold.sh').write_text(script)
    old = os.getcwd()
    os.chdir(str(tdir))
    os.system("bash unfold.sh")
    os.chdir(old)

    # assert changes1 == 4
    assert (tdir / 'mf.txt').exists()
    assert (tdir / 'ver.yml').read_text().strip() == "version: '1.3'"

    assert len([it for it in (tdir / 'tmp').iterdir()]) == 2
    assert (tdir / 'tmp' / 'be.txt').read_text().strip() == '123d'

    (tdir / 'mf.txt').write_text('DIRTY')
    (tdir / 'ver.yml').unlink()

    old = os.getcwd()
    os.chdir(str(tdir))
    os.system("bash unfold.sh")
    os.chdir(old)

    # assert changes2 == 1
    assert (tdir / 'mf.txt').read_text() == "DIRTY"
    assert (tdir / 'ver.yml').read_text().strip() == "version: '1.3'"


if __name__ == '__main__':
    import fire
    fire.Fire()

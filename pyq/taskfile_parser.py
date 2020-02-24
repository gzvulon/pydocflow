import platform
from pathlib import Path
from ruamel.yaml import YAML
import datetime

yaml = YAML()

def get_prep__aggs(struct_data:dict):
    from collections import Counter
    cmds = []
    for task in struct_data['tasks'].values():
        # print(task)
        for cmd in task['cmds']:
            if isinstance(cmd, str):
                cmds.append(cmd)
            elif isinstance(cmd, dict):
                if 'task' in cmd and len(cmd) == 1:
                    cmds.append(f"task:{cmd['task']}")
                else:
                    print("ERROR:", cmd)
            else:
                print("ERROR:", cmd)
                # import ipdb; ipdb.set_trace()
    import shlex
    wc = Counter()
    for cmd in cmds:
        wc.update(shlex.split(cmd))
    words_alnum = {
        w: c for w,c in wc.items()
        if all(ch.isalnum() or ch in '._/:@-' for ch in w)
    }

    res = dict(
        task_count=len(struct_data['tasks'].keys()),
        task_names=Counter(struct_data['tasks'].keys()),
        descs_names=Counter(
            task['desc']
            for task in struct_data['tasks']
            if 'desc' in task),
        cmds_count=len(cmds),
        cmds_lines=cmds,
        words_alnum_stat=words_alnum,
        words_alnum_count=sum(words_alnum.values())
    )
    return res

def doc_from_file(filepath):
    import hashlib

    file_p = Path(filepath)
    if file_p.suffix == '.json':
        with file_p.open() as fp:
            data = json.load(fg)
    elif file_p.suffix in ['.yml', '.yaml']:
        with file_p.open() as fp:
            data = yaml.load(fp)
    else:
        raise ValueError(f"Not supported extention {file_p.suffix}")
    raw_text = file_p.read_text()
    doc = dict(
        prep__stamp=dict(
            path=str(file_p.absolute()),
            size=file_p.stat().st_size,
            user=Path.home().absolute().name,
            node=platform.node(),
            md5=hashlib.md5(raw_text.encode()).hexdigest()
        ),
        prep__data=dict(
            raw_text=raw_text,
            struct_data=data
        )
    )
    doc['prep__stamp']['path_id'] = "unps://{user}@{node}:{path}".format(
        **doc['prep__stamp'])
    doc['ids__rfs'] = "rpun://{rpath}:{node}@{user}".format(
        rpath="@".join(reversed(doc['prep__stamp']['path'].split('/'))),
        **doc['prep__stamp']
    )

    doc['prep__stamp']['content_id'] = "{size}:{md5}".format(
        **doc['prep__stamp'])
    doc['prep__stamp']['ts_id'] = datetime.datetime.utcnow()
    doc['ids__path'] =  doc['prep__stamp']['path_id']
    doc['ids__prep'] = "{rfs}:{ts_id}".format(
        rfs=doc['ids__rfs'],
        ts_id=str(doc['prep__stamp']['ts_id']).replace(' ', 'T').replace(':', '-')
    )
    doc['prep__data']['aggs'] = get_prep__aggs(doc['prep__data']['struct_data'])
    return doc

def create_task(doc:dict, name:str):
    task = dict(name=name)
    task['parent_doc'] = {}
    for k, v in doc.items():
        if k.startswith('ids__'):
            task['parent_doc'][k] = v
    task.update(doc['prep__data']['struct_data']['tasks'][name])
    return task

def tokenize_cmd(cmd_text):
    import shlex
    tokens = shlex.split(cmd_text)
    return tokens
    # import shlex
    # wc = Counter()
    # for cmd in cmds:
    #     wc.update()
    # words_alnum = {
    #     w: c for w,c in wc.items()
    #     if all(ch.isalnum() or ch in '._/:@-~' for ch in w)
    # }
def prep_task(task):
    from collections import defaultdict
    from pnm import is_pathname_valid
    task['tokens__cmds'] = []
    task['tokens__klasses'] = defaultdict(list)
    bag = task['tokens__klasses']
    for cmd_text in  task['cmds']:
        tokens = tokenize_cmd(cmd_text)
        task['tokens__cmds'].append(tokens)
        bag['aplhpanum_yes'].extend(sc for sc in tokens if sc.isalnum())
        bag['aplhpanum_no'].extend(sc for sc in tokens if not sc.isalnum())

        bag['flags'].extend(sc for sc in bag['aplhpanum_no'] if sc.startswith('-'))
        bag['urls'].extend(sc for sc in bag['aplhpanum_no']
            if sc.startswith('http') and '://' in sc)
        bag['fs_path'].extend(sc for sc in bag['aplhpanum_no']
            if Path(sc).resolve().exists() or "~" in sc)
    started = set(bag['aplhpanum_no'])
    current = set(started)
    for klass in ['flags', 'urls', 'fs_path']:
        current.difference_update(set(bag[klass]))
    bag["rest"] = list(current)






def test_task(name=None):
    name = name or 'install-zsh'
    doc = doc_from_file(Path(__file__).parent / 'sample_taskfile.yml')
    task = create_task(doc, name)
    prep_task(task)
    return task




# def create_task_():
#     dict(
#         name=
#         org__taskfile={
#             'ids__rfs':    'rpun://sample_taskfile.yml@pyq@02-Feb-17@2020_init@ivanne@Users@:Ivannes-MBP@ivanne',
#             'ids__path':   'unps://ivanne@Ivannes-MBP:/Users/ivanne/2020_init/02-Feb-17/pyq/sample_taskfile.yml',
#             'ids__prep':   'rpun://sample_taskfile.yml@pyq@02-Feb-17@2020_init@ivanne@Users@:Ivannes-MBP@ivanne:2020-02-17T05-20-52.561976',
#         }
#     )
if __name__ == "__main__":
    import fire
    fire.Fire()
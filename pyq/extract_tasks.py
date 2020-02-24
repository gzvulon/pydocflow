import fire
import json
from pathlib import Path
from ruamel.yaml import YAML

yaml = YAML()

def test__extractor():
    target_filename = 'sample_taskfile.yml'
    target_p = Path(target_filename)
    with target_p.open() as fp:
        data = yaml.load(fp)
    tasks = data['tasks']
    return tasks
    # jsdata = json.dumps(data, indent=2, sort_keys=True)

def extract_tasks_jsons():
    target_filename = 'sample_taskfile.yml'
    target_p = Path(target_filename)
    with target_p.open() as fp:
        data = yaml.load(fp)
    tasks = data['tasks']
    for task in tasks:
        the_task = dict(tasks[task])
        the_task['org_taskname'] = task
        jsrow = json.dumps(the_task, sort_keys=True)
        print(jsrow)

if __name__ == "__main__":
    fire.Fire()



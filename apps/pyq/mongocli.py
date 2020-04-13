import fire
import json

from pathlib import Path
from pymongo import MongoClient
import platform
from ruamel.yaml import YAML

yaml = YAML()

from taskfile_parser import doc_from_file, get_prep__aggs

def test_mongo_connection():
    mongo_c = MongoClient(
        'daragent:27017',
        username='root',
        password='example',
        authSource='admin',
        authMechanism='SCRAM-SHA-256')
    return mongo_c.list_database_names()

def interate_from(filepath):
    file_p = Path(filepath)
    if file_p.suffix == '.ndjson':
        with file_p.open() as fp:
            for line in fp:
                line_strip = line.strip()
                if not line_strip:
                    continue
                elif line_strip[0] in [';', '#', '/']:
                    continue
                else:
                    drow = json.loads(line)
                    yield drow
    else:
        raise ValueError(f"Not supported extention {file_p.suffix}")



class MongoCli:

    def __init__(self, **kw):
        self.dev_mode = kw.pop('dev_mode', False)
        import types
        self.funcs = {}
        if self.dev_mode:
            # print("-dev")
            for _n, _o in globals().items():
                # print("stam", _n)
                if isinstance(_o, types.FunctionType):
                    # print("good", _o.__module__)
                    # setattr(_oself, _o.name, _o)
                    self.funcs[_n] = _o
            print(f"Available methods: {self.funcs}")
        self._mongo_c: MongoClient = None

    def _init_mongo_client(self):
        mongo_c = MongoClient(
            'daragent:27017',
            username='root',
            password='example',
            authSource='admin',
            authMechanism='SCRAM-SHA-256')
        return mongo_c

    def mongo_c(self) -> MongoClient:
        if self._mongo_c is None:
            self._mongo_c = self._init_mongo_client()
        return self._mongo_c

    def db_tasks(self):
        return self.mongo_c().get_database('play').get_collection('tasks')

    def db_tasksfiles(self):
        return self.mongo_c().get_database('play').get_collection('tasksfiles')

    def insert_task(self, drow:dict):
        print(json.dumps({
            'log':'info',
            'target': drow
        }))
        res = self.db_tasks().insert_one(drow)
        return res.inserted_id

    def insert_taskfile(self, drow:dict):
        print(json.dumps({
            'log':'info',
            'target': drow
        }))
        res = self.db_tasksfiles().insert_one(drow)
        return res.inserted_id

    def col(self, name):
        return self.mongo_c().get_database('play').get_collection(name)

    def import_from(self, filepath):
        for drow in interate_from(filepath):
            did = self.insert_task(drow)
            print(did)

    def import_doc(self, filepath, colname):
        import datetime
        col = self.col(colname)
        col_ready = self.col(f'{colname}_ready')
        doc = doc_from_file(filepath)
        doc['pydate_modified'] = datetime.datetime.utcnow()
        res = col.update_one(
            {'_id': doc['ids__prep']},
            {
                "$set": doc,
                "$setOnInsert": {
                    "pydate_created": doc['pydate_modified']
                },
                "$currentDate": {
                    "last_modified": True,
                    "modified": { "$type": "timestamp" }
                }
            }, upsert=True)


        res2 = col_ready.update_one(
            {'_id': doc['ids__rfs']},
            {
                "$set": doc,
                "$setOnInsert": {
                    "pydate_created": doc['pydate_modified']
                },
                "$currentDate": {
                    "last_modified": True,
                    "modified": { "$type": "timestamp" }
                }
            }, upsert=True)

        return doc['ids__rfs'], doc['ids__prep']


if __name__ == "__main__":
    me = Path(__file__)
    # print (
    #     MongoCli().import_doc(me.parent / 'sample_taskfile.yml', 'files').matched_count
    # )

    import sys
    if '--db' in sys.argv:
        fire.Fire()
    else:
        fire.Fire(MongoCli)
import os
import fire
from typing import List, Dict


def resolve_http(uri: str):
    pass


def resolve_s3(uri: str):
    pass


def resolve_fs(uri: str):
    pass


def resolve_rclone(uri: str):
    pass


class ParamsCfg:
    pass


class ResolversCfg:
    pass


class SimpleReplacer:
    def __init__(self, replace_expr: str):
        self.replace_expr: str = replace_expr
        self.pfrom, self.pto = self.replace_expr.split('-=>')

    def process_it(self, it: str) -> str:
        if self.pfrom in it:
            res = it.replace(self.pfrom, self.pto)
        else:
            res = it
        return res


class ResolverCfg:
    replacers: List[SimpleReplacer] = []


class ResolverCli:
    def __init__(self, cfg=None, META_RC__REPLACE=None):
        META_RC__REPLACE = os.environ.get('META_RC__REPLACE', META_RC__REPLACE)
        self.replacers: List[SimpleReplacer] = []
        if META_RC__REPLACE:
            self.replacers.append(SimpleReplacer(META_RC__REPLACE))

    def process_it(self, it: str):
        it_now = it
        for replacer in self.replacers:
            it_now = replacer.process_it(it_now)
        return it_now

    def uri_type(self, uri: str):
        changes = {}
        if uri.startswith("http://") or uri.startswith("https://"):
            changes["uri-type"] = "http"
        return changes

    def uri_http(self, uri: str):
        changes = {}
        if uri.startswith("http://") or uri.startswith("https://"):
            changes["uri-http"] = uri
        return changes

    def uri_any(self, uri: str):
        changes = {}
        # if uri.startswith("http://") or uri.startswith("https://"):
        changes["uri-fs"] = self.process_it(uri)
        return changes


# def resolve_uri(uri: str):
#     method = resolve_method()

if __name__ == "__main__":
    fire.Fire(ResolverCli)
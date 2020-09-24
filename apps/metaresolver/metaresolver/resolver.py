import fire


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


class ResolverCli:
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


# def resolve_uri(uri: str):
#     method = resolve_method()

if __name__ == "__main__":
    fire.Fire(ResolverCli)
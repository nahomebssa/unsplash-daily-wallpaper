import localStorage
localStorage = localStorage.localStorage

import json

def parse_filename_from_url(url, **options):
    file_ext = options['file_ext'] if 'file_ext' in options else ''
    filename = url[url.rindex('/'):][1:]
    filename = filename[:filename.index('?')]+file_ext
    return filename

def load_json(path):
    json_str = None
    with open(path, 'r') as jsonfile:
        json_str = jsonfile.read()
    return json.loads(json_str)
def dump_json(path, dest):
    json_str = json.dumps(dest)
    with open(path, 'w') as jsonfile:
        jsonfile.write(json_str)
    return True
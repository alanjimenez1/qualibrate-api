import json
import subprocess

class ApiRequest:

    def get(self, url):
        return json.loads(subprocess.getoutput("http GET %s" % url))

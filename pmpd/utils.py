import subprocess

class Utils():

    def clear_merge_conflict(self):
        print self.git(['reset', 'HEAD'])
        print self.git(['checkout', '.'])

    def get_tickets(self, location):
        f = open(location,'r')
        result = list()
        while True:
            x = f.readline().rstrip()
            if not x:
                return result
            else:
                result.append(x)

    def git(self, args):
        args = ['git'] + args
        git = subprocess.Popen(args, stdout=subprocess.PIPE)
        details = git.stdout.read()
        details = details.strip()
        return details

    def msg(self, msg):
        return """\
#################################################################
##
## %s
##
#################################################################\
        """ % (msg)

    def run_bash(self, cmd):
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        out = p.stdout.read().strip()
        return out

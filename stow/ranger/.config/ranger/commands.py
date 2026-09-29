from ranger.api.commands import *
from datetime import date
from datetime import datetime



class newcmd(Command):
    def execute(self):
        today = datetime.now()
        d1 = today.strftime("%Y-%m-%d-%H-%M-%S")
        filename = str(d1) + '.md'
        self.fm.run(['touch', filename ])
        with open(filename, "a") as text_file:
            text_file.write("# %s" % str(d1))

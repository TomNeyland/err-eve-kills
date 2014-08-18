from errbot import BotPlugin, botcmd
from errbot.builtins.webserver import webhook
from datetime import datetime
import ago


class Xup(BotPlugin):
    min_err_version = '1.6.0' # Optional, but recommended
    #max_err_version = '2.0.0' # Optional, but recommended

    def activate(self):
        super(Xup, self).activate()

        if not hasattr(self.shelf, 'users'):
            self.shelf.users = {}

    @botcmd(split_args_with=None)
    def xup(self, mess, args):
        """A command which simply returns 'Example'"""

        user = mess.getFrom()
        xup_args = {'user': user,'args': args, 'time': datetime.utcnow()}

        self.shelf.users[user] = xup_args

        return "Added: %s" % (self.shelf.users[user],)

    @botcmd(template="xup_list"):
    def xup_list(self, mess, args):

        now = datetime.utcnow()

        members = self.shelf.users.values()

        members = sorted(members, key=lambda member: member['time'])

        for member in members:
            member['time_ago'] = ago.human(member['time'] - now)

        return {'members': members}


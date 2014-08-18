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
        """Add yourself to the ready list, you can include an optional message."""

        user = str(mess.getFrom().getNode())
        xup_args = {'user': user,'args': args, 'message': mess.getBody(),'time': datetime.utcnow()}

        self.shelf.users[user] = xup_args

        return "Added: %s" % (self.shelf.users[user],)

    @botcmd(template="xup_list")
    def xup_list(self, mess, args):
        """Show everyone who is on the ready list."""
        now = datetime.utcnow()

        members = self.shelf.users.values()

        members = sorted(members, key=lambda member: member['time'])

        for member in members:
            member['message'] = ",".join(member['args'])
            member['time_ago'] = ago.human(now - member['time'])

        return {'members': members}

    @botcmd(split_args_with=None)
    def xup_ping(self, mess, args):
        """Ping everyone who has xed-up"""
        return ",".join(sorted(self.shelf.users.keys()))

    @botcmd(split_args_with=None)
    def xup_remove(self, mess, args):
        """Remove yourself from the ready list"""
        user = str(mess.getFrom().getNode())

        del self.shelf.users[user]

        return "Done."
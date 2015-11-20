from clint.textui import puts, colored
from elex.cli.utils import parse_date
from functools import wraps


def require_date(fn):
    @wraps(fn)
    def decorated(self):
        name = fn.__name__.replace('_', '-')
        if not self.app.pargs.data_file and len(self.app.pargs.date) and self.app.pargs.date[0]:
            try:
                self.app.election.electiondate = parse_date(self.app.pargs.date[0])
                return fn(self)
            except ValueError:
                puts(colored.yellow('Whoa there, friend! There was an error:\n'))
                puts('{0} could not be recognized as a date.\n'.format(colored.green(self.app.pargs.date[0])))
            except KeyError:
                puts(colored.yellow('Whoa there, friend! There was an error:\n'))
                puts('You have not exported %s as an environment variable.\n'.format(colored.green("AP_API_KEY")))
        elif self.app.pargs.data_file:
            self.app.election.electiondate = 'data file: {0}'.format(self.app.pargs.data_file)
            return fn(self)
        else:
            puts(colored.yellow('Please specify an election date (e.g. `elex {0} 2015-11-03`) or data file (e.g. `elex {0} --data-file path/to/file.json`). \n\nRun `elex` for help.\n'.format(name)))


    return decorated

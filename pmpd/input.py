from argparse import ArgumentParser

class Parser(ArgumentParser):
    """Adds additional logic to `argparse.ArgumentParser`.

    Handles all input (CLI args, file args, stdin), applies defaults,
    and performs extra validation.

    """
    def __init__(self, *args, **kwargs):
        kwargs['add_help'] = False
        super(Parser, self).__init__(*args, **kwargs)

    #noinspection PyMethodOverriding
    def parse_args(self, env, args=None, namespace=None):

        self.env = env
        self.args, no_options = super(Parser, self)\
            .parse_known_args(args, namespace)

        # Arguments processing and environment setup.
        self._apply_no_options(no_options)
        self._apply_config()
        self._process_auth()

        return self.args

    def _apply_config(self):
        if (not self.args.json
                and self.env.config.implicit_content_type == 'form'):
            self.args.form = True

    def _apply_no_options(self, no_options):
        """For every `--no-OPTION` in `no_options`, set `args.OPTION` to
        its default value. This allows for un-setting of options, e.g.,
        specified in config.

        """
        invalid = []

        for option in no_options:
            if not option.startswith('--no-'):
                invalid.append(option)
                continue

            # --no-option => --option
            inverted = '--' + option[5:]
            for action in self._actions:
                if inverted in action.option_strings:
                    setattr(self.args, action.dest, action.default)
                    break
            else:
                invalid.append(option)

        if invalid:
            msg = 'unrecognized arguments: %s'
            self.error(msg % ' '.join(invalid))

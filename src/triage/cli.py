#!/usr/bin/env python

from argcmdr import RootCommand, Command, main
from triage.experiments import CONFIG_VERSION
from triage.component.results_schema import upgrade_db, stamp_db, REVISION_MAPPING


class Triage(RootCommand):
    """manage Triage database and experiments"""

    def __init__(self, parser):
        parser.add_argument(
            '-d', '--dbfile',
            default='database.yaml',
            help="database connection file",
        )


@Triage.register
class Experiment(Command):
    """Validate and run experiments, manage experiment database"""
    class UpgradeDb(Command):
        """Upgrade triage results database"""
        def __call__(self, args):
            upgrade_db(args.dbfile)

    class StampDb(Command):
        """Instruct the triage results database to mark itself as updated to a known version without doing any upgrading.
        
        Use this if the database was created without an 'alembic_version' table. Uses the config version of your experiment to infer what database version is suitable.
        """
        def __init__(self, parser):
            parser.add_argument(
                'configversion',
                choices=REVISION_MAPPING.keys(),
                help='config version of last experiment you ran',
            )

        def __call__(self, args):
            revision = REVISION_MAPPING[args.configversion]
            print(f"Based on config version {args.configversion} " +
                  f"we think your results schema is version {revision} and are upgrading to it")
            stamp_db(revision, args.dbfile)

    class ConfigVersion(Command):
        """Return the experiment config version compatible with this installation of Triage"""
        def __call__(self, args):
            print(CONFIG_VERSION)


def execute():
    main(Triage)


if __name__ == '__main__':
    main(Triage)

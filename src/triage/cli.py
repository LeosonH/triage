#!/usr/bin/env python

from argcmdr import RootCommand, Command, main
from triage.experiments import CONFIG_VERSION
from sqlalchemy import create_engine
from triage.component.architect.feature_generators import FeatureGenerator
from triage.util.db import dburl_from_filename
import yaml


class Triage(RootCommand):
    """manage Triage database and experiments"""

    def __init__(self, parser):
        parser.add_argument(
            '-d', '--dbfile',
            default='database.yaml',
            help="database connection file",
        )


@Triage.register
class ConfigVersion(Command):
    """Return the experiment config version compatible with this installation of Triage"""
    def __call__(self, args):
        print(CONFIG_VERSION)


@Triage.register
class FeatureTest(Command):
    """Run a feature aggregation for an as-of-date"""
    def __init__(self, parser):
        parser.add_argument(
            'feature_config_file',
            help='Feature config YAML file, containing a list of feature_aggregation objects'
        )
        parser.add_argument(
            'as_of_date',
            help='The date at which to run features'
        )

    def __call__(self, args):
        db_engine = create_engine(dburl_from_filename(args.dbfile))
        with open(args.feature_config_file) as f:
            feature_config = yaml.load(f)

        FeatureGenerator(db_engine, 'features').create_preimputed_features(
            feature_aggregation_config=feature_config,
            feature_dates=[args.as_of_date]
        )


def execute():
    main(Triage)


if __name__ == '__main__':
    main(Triage)

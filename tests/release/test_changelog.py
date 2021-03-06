import os
import unittest
import shutil
import filecmp
from datetime import date

import mock
from semantic_version import Version

from maintain.release.changelog import ChangelogReleaser
from ..utils import temp_directory, touch


class FakeDate(date):
    """Hackery to be able to patch date"""

    def __new__(cls, *args, **kwargs):
        return date.__new__(date, *args, **kwargs)


class ChangelogReleaserTestCase(unittest.TestCase):
    def test_detects_version_file(self):
        with temp_directory() as directory:
            touch('CHANGELOG.md')
            self.assertTrue(ChangelogReleaser().detect())

    def test_determine_current_version(self):
        fixture_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'fixtures')
        changelog = os.path.join(fixture_path, 'CHANGELOG.md')

        with temp_directory() as directory:
            shutil.copyfile(changelog, 'CHANGELOG.md')
            version = ChangelogReleaser().determine_current_version()
            self.assertEqual(version, Version('1.0.0'))

    @mock.patch('maintain.release.changelog.date', FakeDate)
    def test_bumps_master(self):
        from datetime import date
        FakeDate.today = classmethod(lambda cls: date(2016, 1, 1))

        fixture_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'fixtures')
        changelog = os.path.join(fixture_path, 'CHANGELOG.md')
        bumped_changelog = os.path.join(fixture_path, 'BUMPED_CHANGELOG.md')

        with temp_directory() as directory:
            shutil.copyfile(changelog, 'CHANGELOG.md')
            version = ChangelogReleaser().bump('1.0.1')
            self.assertTrue(filecmp.cmp('CHANGELOG.md', bumped_changelog))

# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import unittest
import logging
from unittest import mock
from unittest import SkipTest

from app import main
from test import utils

NUM_LINES_TO_CHECK = 50

CONFIGS = {
    # The GitHub params belong to the public Data Commons gmail account.
    # Auth tokens, user name and other details can be found in the inbox
    # and in the inbox of teammates.
    'github_repo_owner_username': os.getenv('_GITHUB_REPO_OWNER_USERNAME', ''),
    'github_repo_name': 'data-demo',
    'github_auth_username': os.getenv('_GITHUB_AUTH_USERNAME', ''),
    'github_auth_access_token': os.getenv('_GITHUB_AUTH_ACCESS_TOKEN', '')
}


class GCSFileUploaderMock:
    _REVERSE = False

    def __init__(self, **kwargs):
        # Unused
        del kwargs

    def upload_file(self, src: str, dest: str):
        logging.warning(f'Uploading {src} to {dest}')
        with open(src) as file:
            logging.warning(f'Generated {src}: {file.readline().strip()}')
        assert utils.compare_lines(
            os.path.join('test/data', os.path.basename(src)), src,
            NUM_LINES_TO_CHECK, GCSFileUploaderMock._REVERSE)

    def upload_string(self, string: str, dest: str):
        assert dest.endswith('/latest_version.txt')
        assert string == '2020_07_15T12_07_17_365264_07_00'


# Note: Integration tests here are skipped because it is linked to a personal directory
# TODO: change CONFIGs to main repo and fix integration test.
@SkipTest
@mock.patch('app.service.email_notifier.EmailNotifier', mock.MagicMock())
@mock.patch('app.service.file_uploader.GCSFileUploader', GCSFileUploaderMock)
@mock.patch('app.utils.pacific_time',
            lambda: '2020-07-15T12:07:17.365264-07:00')
class StandaloneUpdateTest(unittest.TestCase):
    """Tests for updating imports in standalone mode.

    To add a test case:
    1) Add a manifest.json to the import directory in the master branch of
       datacommonsorg/data.
    2) Copy the CSVs and MCFs that will be generated by the scripts to
       test/data. Only keep the first or last NUM_LINES_TO_CHECK
       (defined at the top) lines and a newline at the end.
    3) Add a test function below. Use
       @mock.patch('test.integration_test.GCSFileUploaderMock._REVERSE', True)
       to compare the last NUM_LINES_TO_CHECK lines.
    """

    def setUp(self):
        self.app = main.FLASK_APP.test_client()

    def test_treasury_update(self):
        response = self.app.post(
            '/update',
            json={
                'absolute_import_name':
                    'scripts/us_fed/treasury_constant_maturity_rates:all',
                'configs':
                    CONFIGS
            })
        self.assertEqual(200, response.status_code)
        expected_result = {
            'status': 'succeeded',
            'imports_executed': [
                'scripts/us_fed/treasury_constant_maturity_rates'
                ':us_treasury_constant_maturity_rates'
            ],
            'message': 'No issues'
        }
        self.assertEqual(expected_result, response.json)

    @mock.patch('test.integration_test.GCSFileUploaderMock._REVERSE', True)
    def test_covid_state_update(self):
        response = self.app.post(
            '/update',
            json={
                'absolute_import_name':
                    'scripts/covid_tracking_project/historic_state_data:all',
                'configs':
                    CONFIGS
            })
        self.assertEqual(200, response.status_code)
        expected_result = {
            'status': 'succeeded',
            'imports_executed': [
                'scripts/covid_tracking_project/historic_state_data'
                ':historic_state_data'
            ],
            'message': 'No issues'
        }
        self.assertEqual(expected_result, response.json)


@SkipTest
@mock.patch('app.service.import_service.ImportServiceClient', mock.MagicMock())
@mock.patch('app.service.email_notifier.EmailNotifier', mock.MagicMock())
@mock.patch('app.utils.pacific_time',
            lambda: '2020-07-15T12:07:17.365264-07:00')
@mock.patch('app.service.file_uploader.GCSFileUploader', GCSFileUploaderMock)
class CommitTest(unittest.TestCase):

    def setUp(self):
        self.app = main.FLASK_APP.test_client()

    def test_treasury(self):
        response = self.app.post(
            '/',
            json={
                'COMMIT_SHA': '9804f2fd2c5422a9f6b896e9c6862db61f9a8a08',
                'configs': CONFIGS
            })
        self.assertEqual(200, response.status_code)
        expected_result = {
            'status': 'succeeded',
            'imports_executed': [
                'scripts/us_fed/treasury_constant_maturity_rates'
                ':us_treasury_constant_maturity_rates'
            ],
            'message': 'No issues'
        }
        self.assertEqual(expected_result, response.json)

    def test_jolts(self):
        response = self.app.post(
            '/',
            json={
                'COMMIT_SHA': 'cded751aaf369af27430d5f80da61b04b5dea9b4',
                'configs': CONFIGS
            })
        self.assertEqual(200, response.status_code)
        expected_result = {
            'status': 'succeeded',
            'imports_executed': ['scripts/us_bls/jolts:JOLTS'],
            'message': 'No issues'
        }
        self.assertEqual(expected_result, response.json)


@SkipTest
@mock.patch('app.utils.utctime', lambda: '2020-07-24T16:27:22.609304+00:00')
@mock.patch('app.service.email_notifier.EmailNotifier', mock.MagicMock())
@mock.patch('google.cloud.scheduler.CloudSchedulerClient',
            utils.SchedulerClientMock)
@mock.patch('google.protobuf.json_format.MessageToDict',
            lambda job, preserving_proto_field_name=False: dict(job))
class ScheduleTest(unittest.TestCase):
    """Tests for scheduling import updates."""

    def setUp(self):
        self.app = main.FLASK_APP.test_client()

    def test_treasury_absolute(self):
        """The target is specified using absolute import name."""
        response = self.app.post(
            '/schedule',
            json={
                'COMMIT_SHA': '0df53ec282b1dd030165c7dc309d53964562b211',
                'configs': CONFIGS
            })
        self.assertEqual(200, response.status_code)
        scheduled_imports = response.json['imports_executed']
        self.assertEqual(1, len(scheduled_imports))
        scheduled = scheduled_imports[0]
        expected_name = ('projects/google.com:datcom-data/'
                         'locations/us-central1/jobs/'
                         'scripts_us_fed_treasury_constant_maturity_'
                         'rates_us_treasury_constant_maturity_rates')
        self.assertEqual(expected_name, scheduled['name'])
        expected_desc = ('scripts/us_fed/treasury_constant_maturity_'
                         'rates:us_treasury_constant_maturity_rates')
        self.assertEqual(expected_desc, scheduled['description'])
        self.assertEqual('* * * * *', scheduled['schedule'])

    def test_treasury_relative(self):
        """The target is specified using relative import name."""
        response = self.app.post(
            '/schedule',
            json={
                'COMMIT_SHA': '50195689a407af9ab60d5ead0dd733b0cfbe4cb0',
                'configs': CONFIGS
            })
        self.assertEqual(200, response.status_code)
        scheduled_imports = response.json['imports_executed']
        self.assertEqual(1, len(scheduled_imports))
        scheduled = scheduled_imports[0]
        expected_name = ('projects/google.com:datcom-data/'
                         'locations/us-central1/jobs/'
                         'scripts_us_fed_treasury_constant_maturity_'
                         'rates_us_treasury_constant_maturity_rates')
        self.assertEqual(expected_name, scheduled['name'])
        expected_desc = ('scripts/us_fed/treasury_constant_maturity_'
                         'rates:us_treasury_constant_maturity_rates')
        self.assertEqual(expected_desc, scheduled['description'])
        self.assertEqual('* * * * *', scheduled['schedule'])

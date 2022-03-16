# settings_mocked.py
from django_mock_queries.mocks import monkey_patch_test_db

from api_poc.settings import *

monkey_patch_test_db()

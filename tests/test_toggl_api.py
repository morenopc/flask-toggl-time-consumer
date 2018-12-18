import os
from toggl.TogglPy import Toggl
from app.toggl_api import REPORTS_URL, PARAMET_URL

toggl = Toggl()
TOGGL_API_KEY = os.environ.get('TOGGL_API_KEY')
toggl.setAPIKey(TOGGL_API_KEY)


def test_detailed_report(client):
    # test toggl api detailed report time entries
    response = toggl.request(''.join([REPORTS_URL, 'details?', PARAMET_URL]))
    assert response.get('data') is not None

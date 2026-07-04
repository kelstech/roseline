from datetime import datetime, timedelta, timezone
from uuid import uuid4

import pytest

from backend.ehis.workforce.services import ScheduleWindow, WorkforcePolicyService, WorkforceRuleError


def test_schedule_cannot_exceed_maximum_working_hours():
    service = WorkforcePolicyService()
    start = datetime(2026, 1, 1, 8, tzinfo=timezone.utc)
    with pytest.raises(WorkforceRuleError):
        service.validate_schedule_window(ScheduleWindow(uuid4(), start, start + timedelta(hours=18)), max_hours=16)


def test_rest_period_is_mandatory_between_shifts():
    service = WorkforcePolicyService()
    previous_end = datetime(2026, 1, 1, 22, tzinfo=timezone.utc)
    next_start = previous_end + timedelta(hours=8)
    with pytest.raises(WorkforceRuleError):
        service.validate_rest_period(previous_end, next_start, minimum_rest_hours=10)


def test_verified_license_is_required_for_clinical_privilege():
    service = WorkforcePolicyService()
    with pytest.raises(WorkforceRuleError):
        service.validate_verified_license_for_privilege("pending", expires_on=datetime(2027, 1, 1).date(), starts_on=datetime(2026, 1, 1).date())

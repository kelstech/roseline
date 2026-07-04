"""Service-layer business rules for EHIS Module 05."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
from uuid import UUID


class WorkforceRuleError(ValueError):
    """Raised when a workforce business rule is violated."""


@dataclass(frozen=True)
class ScheduleWindow:
    employee_id: UUID
    starts_at: datetime
    ends_at: datetime


class WorkforcePolicyService:
    """Validates credential, assignment, hierarchy, and scheduling rules."""

    def validate_employee_number(self, employee_number: str) -> None:
        if not employee_number or len(employee_number.strip()) < 4:
            raise WorkforceRuleError("Employee number must be present and enterprise-unique.")

    def validate_verified_license_for_privilege(self, verification_status: str, expires_on, starts_on) -> None:
        if verification_status != "verified":
            raise WorkforceRuleError("Clinical privileges require a verified professional license.")
        if expires_on < starts_on:
            raise WorkforceRuleError("Clinical privilege cannot start after the supporting license expires.")

    def validate_schedule_window(self, window: ScheduleWindow, max_hours: int = 16) -> None:
        if window.ends_at <= window.starts_at:
            raise WorkforceRuleError("Schedule end must be after start.")
        hours = (window.ends_at - window.starts_at).total_seconds() / 3600
        if hours > max_hours:
            raise WorkforceRuleError("Schedule exceeds maximum working hours.")

    def validate_rest_period(self, previous_end: datetime, next_start: datetime, minimum_rest_hours: int = 10) -> None:
        if next_start - previous_end < timedelta(hours=minimum_rest_hours):
            raise WorkforceRuleError("Mandatory rest period has not elapsed.")

    def validate_reporting_hierarchy(self, employee_id: UUID, manager_chain: list[UUID]) -> None:
        if employee_id in manager_chain:
            raise WorkforceRuleError("Reporting hierarchy cannot contain cycles.")

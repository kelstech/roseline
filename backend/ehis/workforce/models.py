"""Domain-oriented Django model sketch for EHIS Module 05 workforce management."""

from __future__ import annotations

import uuid
from django.db import models
from django.utils import timezone


class AuditedModel(models.Model):
    """Common UUID, audit, soft-delete, and optimistic-version columns for workforce tables."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant_id = models.UUIDField(db_index=True)
    created_at = models.DateTimeField(default=timezone.now, db_index=True)
    created_by_id = models.UUIDField(null=True, blank=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by_id = models.UUIDField(null=True, blank=True, db_index=True)
    deleted_at = models.DateTimeField(null=True, blank=True, db_index=True)
    deleted_by_id = models.UUIDField(null=True, blank=True)
    version = models.PositiveIntegerField(default=1)
    metadata = models.JSONField(default=dict, blank=True)

    class Meta:
        abstract = True


class Employee(AuditedModel):
    """Single enterprise master record for a worker."""

    class Category(models.TextChoices):
        EMPLOYEE = "employee", "Employee"
        CONSULTANT = "consultant", "Consultant"
        VISITING_SPECIALIST = "visiting_specialist", "Visiting Specialist"
        RESIDENT_DOCTOR = "resident_doctor", "Resident Doctor"
        MEDICAL_OFFICER = "medical_officer", "Medical Officer"
        INTERN_DOCTOR = "intern_doctor", "Intern Doctor"
        NURSE = "nurse", "Nurse"
        PHARMACIST = "pharmacist", "Pharmacist"
        LAB_SCIENTIST = "laboratory_scientist", "Laboratory Scientist"
        RADIOGRAPHER = "radiographer", "Radiographer"
        BIOMEDICAL_ENGINEER = "biomedical_engineer", "Biomedical Engineer"
        PHYSIOTHERAPIST = "physiotherapist", "Physiotherapist"
        DIETITIAN = "dietitian", "Dietitian"
        CLINICAL_RESEARCHER = "clinical_researcher", "Clinical Researcher"
        ADMINISTRATIVE = "administrative_staff", "Administrative Staff"
        FINANCE = "finance_staff", "Finance Staff"
        PROCUREMENT = "procurement_staff", "Procurement Staff"
        HR = "hr_staff", "HR Staff"
        ICT = "ict_staff", "ICT Staff"
        SECURITY = "security_personnel", "Security Personnel"
        HOUSEKEEPING = "housekeeping", "Housekeeping"
        DRIVER = "driver", "Driver"
        VOLUNTEER = "volunteer", "Volunteer"
        STUDENT = "student", "Student"
        CONTRACTOR = "contractor", "Contractor"
        TEMPORARY = "temporary_staff", "Temporary Staff"
        AGENCY = "agency_staff", "Agency Staff"

    class Status(models.TextChoices):
        APPLICANT = "applicant", "Applicant"
        PROBATION = "probation", "Probation"
        ACTIVE = "active", "Active"
        SUSPENDED = "suspended", "Suspended"
        LEAVE = "leave_of_absence", "Leave of Absence"
        INACTIVE = "inactive", "Inactive"
        TERMINATED = "terminated", "Terminated"
        RETIRED = "retired", "Retired"

    employee_number = models.CharField(max_length=32, unique=True)
    identity_user_id = models.UUIDField(null=True, blank=True, db_index=True)
    authorization_role_ids = models.JSONField(default=list, blank=True)
    category = models.CharField(max_length=64, choices=Category.choices, db_index=True)
    status = models.CharField(max_length=32, choices=Status.choices, default=Status.APPLICANT, db_index=True)
    first_name = models.CharField(max_length=120)
    middle_name = models.CharField(max_length=120, blank=True)
    last_name = models.CharField(max_length=120)
    date_of_birth = models.DateField(null=True, blank=True)
    national_id_encrypted = models.TextField(blank=True)
    passport_number_encrypted = models.TextField(blank=True)
    nationality = models.CharField(max_length=120, blank=True)
    languages = models.JSONField(default=list, blank=True)
    photograph_uri = models.TextField(blank=True)
    professional_license_numbers = models.JSONField(default=list, blank=True)
    primary_department_id = models.UUIDField(null=True, blank=True, db_index=True)
    reporting_manager = models.ForeignKey("self", null=True, blank=True, on_delete=models.PROTECT)
    clinical_specialty = models.CharField(max_length=160, blank=True, db_index=True)
    clinical_subspecialty = models.CharField(max_length=160, blank=True)
    research_interests = models.JSONField(default=list, blank=True)
    salary_grade_ref = models.CharField(max_length=80, blank=True)
    leave_balance_ref = models.CharField(max_length=80, blank=True)
    bank_information_ref = models.CharField(max_length=120, blank=True)
    tax_information_ref = models.CharField(max_length=120, blank=True)
    uniform_sizes = models.JSONField(default=dict, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=["tenant_id", "employee_number"]),
            models.Index(fields=["tenant_id", "last_name", "first_name"]),
            models.Index(fields=["tenant_id", "category", "status"]),
        ]


class ProfessionalLicense(AuditedModel):
    employee = models.ForeignKey(Employee, related_name="licenses", on_delete=models.PROTECT)
    issuing_body = models.CharField(max_length=160)
    license_number = models.CharField(max_length=120)
    license_type = models.CharField(max_length=80)
    issued_on = models.DateField(null=True, blank=True)
    expires_on = models.DateField(db_index=True)
    verified_at = models.DateTimeField(null=True, blank=True)
    verification_status = models.CharField(max_length=32, default="pending", db_index=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["tenant_id", "issuing_body", "license_number"], name="uniq_license_per_issuer")]
        indexes = [models.Index(fields=["tenant_id", "expires_on", "verification_status"])]


class ClinicalPrivilege(AuditedModel):
    employee = models.ForeignKey(Employee, related_name="clinical_privileges", on_delete=models.PROTECT)
    license = models.ForeignKey(ProfessionalLicense, null=True, blank=True, on_delete=models.PROTECT)
    privilege_type = models.CharField(max_length=80, db_index=True)
    scope_of_practice = models.TextField()
    procedure_authorizations = models.JSONField(default=list, blank=True)
    starts_on = models.DateField()
    ends_on = models.DateField(db_index=True)
    status = models.CharField(max_length=32, default="pending", db_index=True)
    approved_by_id = models.UUIDField(null=True, blank=True)

    class Meta:
        indexes = [models.Index(fields=["tenant_id", "employee", "status"]), models.Index(fields=["tenant_id", "ends_on"])]


class DepartmentAssignment(AuditedModel):
    employee = models.ForeignKey(Employee, related_name="department_assignments", on_delete=models.PROTECT)
    organization_unit_id = models.UUIDField(db_index=True)
    assignment_type = models.CharField(max_length=32, db_index=True)
    is_primary = models.BooleanField(default=False, db_index=True)
    starts_at = models.DateTimeField(db_index=True)
    ends_at = models.DateTimeField(null=True, blank=True, db_index=True)
    manager_id = models.UUIDField(null=True, blank=True, db_index=True)
    cost_centre_id = models.UUIDField(null=True, blank=True, db_index=True)
    revenue_centre_id = models.UUIDField(null=True, blank=True, db_index=True)


class WorkforceSchedule(AuditedModel):
    employee = models.ForeignKey(Employee, related_name="schedules", on_delete=models.PROTECT)
    unit_id = models.UUIDField(db_index=True)
    schedule_type = models.CharField(max_length=64, db_index=True)
    starts_at = models.DateTimeField(db_index=True)
    ends_at = models.DateTimeField(db_index=True)
    status = models.CharField(max_length=32, default="draft", db_index=True)
    requires_privilege = models.BooleanField(default=False)
    overtime_eligible = models.BooleanField(default=False)


class LifecycleEvent(AuditedModel):
    employee = models.ForeignKey(Employee, related_name="lifecycle_events", on_delete=models.PROTECT)
    event_type = models.CharField(max_length=64, db_index=True)
    effective_at = models.DateTimeField(db_index=True)
    previous_status = models.CharField(max_length=32, blank=True)
    new_status = models.CharField(max_length=32, blank=True)
    reason = models.TextField(blank=True)
    approved_by_id = models.UUIDField(null=True, blank=True, db_index=True)
    electronic_signature_id = models.UUIDField(null=True, blank=True)

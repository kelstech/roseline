# Module 05 Technical Design

## Architecture
Module 05 follows Clean Architecture and DDD. The domain layer owns workforce aggregates and validation rules. The service layer orchestrates lifecycle events, credential verification, schedule validation, notifications, and integrations. Repository interfaces isolate Django ORM persistence from application use cases.

## Integrations
- Module 02 Authentication: `identity_user_id` links an employee to a login identity and enables access lifecycle workflows.
- Module 03 RBAC: `authorization_role_ids` and assignment events drive role provisioning and revocation.
- Module 04 Organization: organization unit references bind workforce assignments to hospitals, branches, departments, wards, theatres, ICUs, clinics, laboratories, pharmacies, cost centres, and projects.
- Notifications: Celery tasks publish expiry, onboarding, training, shift, vaccination, and employment-status alerts through the enterprise notification service.

## Employee master profile
The employee aggregate stores employee number, identity references, demographic information, sensitive identifiers, photograph reference, biometric reference, digital signature reference, professional identifiers, specialty, subspecialty, research interests, uniform sizes, salary grade reference, leave balance reference, payroll bank and tax references, and authorization references. Sensitive fields are encrypted and protected by field-level permission policies.

## Employment lifecycle events
Supported event types are recruitment reference, offer accepted, onboarding, probation, confirmation, promotion, transfer, department change, role change, secondment, suspension, leave of absence, return from leave, termination, retirement, resignation, exit clearance, and rehire. Events are append-only and update the current employee status through the service layer.

## Credentialing and privileges
Professional licenses, board certifications, specialist certifications, research certifications, mandatory training, clinical privileges, procedure authorizations, surgical privileges, radiation authorization, and chemotherapy authorization are modeled independently. Privilege activation requires verified credentials and valid dates. Expiry jobs suspend privileges and notify the worker, manager, credentialing office, and clinical leadership.

## Scheduling and availability
Schedules represent shifts, on-call rotations, clinic sessions, operating theatre lists, ward coverage, emergency coverage, research time, training days, conferences, vacation, and holidays. The scheduler checks overlapping assignments, maximum work hours, mandatory rest, inactive status, credential requirements, and overtime eligibility before publication.

## Security and audit
Every model has UUID primary key, audit fields, soft delete, optimistic version, and indexes. Audit logs capture before/after changes, actor identity, source IP, reason, electronic signature reference, and request correlation ID. Confidential fields use encrypted storage and serializers redact data unless the caller has explicit RBAC permissions.

## Notifications
Notification policies emit alerts for license expiry, certification expiry, failed credential verification, onboarding, assignment change, shift change, performance review due, training due, vaccination overdue, and employment status changes.

## Reports
Read models support employee directory, headcount by department and branch, credential and license expiry, clinical privileges, vacancy analysis, shift coverage, training compliance, performance reviews, research participation, turnover, employment history, workforce demographics, and occupational health compliance.

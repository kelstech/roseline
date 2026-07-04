# Module 05 — Enterprise User, Staff & Workforce Management Business Requirements

## Purpose
Module 05 is the authoritative enterprise workforce master for employees, contractors, trainees, volunteers, consultants, and external clinicians. It is not payroll, but it publishes workforce facts required by payroll, scheduling, clinical operations, security, compliance, and reporting.

## Business objectives
- Maintain one versioned master record for every human resource across hospitals, branches, and legal entities.
- Track recruitment, onboarding, employment changes, credentialing, scheduling, performance, and separation.
- Integrate each worker with authentication identities, authorization roles, and organization units from Modules 02, 03, and 04.
- Preserve complete audit history, document history, approval signatures, and security controls for sensitive HR data.
- Support cardiovascular, oncology, research, administrative, facilities, security, and support workforce operations.

## Workforce categories
| Category | Purpose | Lifecycle | Statuses | Supervision | Required credentials | Clinical privileges |
|---|---|---|---|---|---|---|
| Employees | Permanent workforce | Recruit, onboard, employ, change, separate, rehire | applicant, active, probation, suspended, inactive, terminated, retired | line manager and department head | identity, contract, background check, role training | role-dependent |
| Consultants | Specialist advisory or clinical service | contract, credential, assign, renew, exit | contracted, active, suspended, expired | medical director or sponsor | license, council registration, malpractice/insurance where applicable | explicit privileges only |
| Visiting Specialists | Time-bound specialist care | invite, verify, privilege, schedule, complete | visiting, active, expired | host consultant and clinical director | current specialist license and verification | limited by visit scope |
| Resident Doctors | Postgraduate trainees | appoint, rotate, evaluate, graduate | trainee, active, rotated, completed | program director and supervising consultant | medical registration, training enrollment | supervised privileges |
| Medical Officers | General medical providers | appoint, credential, roster, review | active, probation, suspended | department consultant/head | medical council registration | approved scope of practice |
| Intern Doctors | Internship providers | onboard, rotate, assess, complete | intern, active, completed | internship coordinator | provisional registration | supervised only |
| Nurses | Nursing care workforce | hire, credential, roster, renew | active, suspended, inactive | nurse manager/matron | nursing council registration, BLS/ACLS where required | nursing procedures by grade |
| Pharmacists | Medication management | hire, license, assign, renew | active, suspended | chief pharmacist | pharmacy council registration | medication-related authorizations |
| Laboratory Scientists | Diagnostic laboratory workforce | hire, credential, assign, renew | active, suspended | lab manager/pathologist | lab council/license where applicable | lab procedure authorizations |
| Radiographers | Imaging workforce | hire, radiation certify, schedule | active, suspended | radiology manager | radiography license, radiation safety | modality and radiation privileges |
| Biomedical Engineers | Clinical equipment support | hire, train, assign assets | active, inactive | engineering manager | technical certifications | none unless equipment authorization |
| Physiotherapists | Rehabilitation care | hire, credential, schedule | active, suspended | rehab manager | professional license | therapy scope privileges |
| Dietitians | Nutrition care | hire, credential, clinic schedule | active, suspended | clinical nutrition lead | dietetics certification/license | nutrition consultation scope |
| Clinical Researchers | Research workforce | appoint, certify, assign study | active, suspended, completed | principal investigator | GCP, ethics training | research procedures only |
| Administrative Staff | Enterprise administration | hire, assign, review | active, inactive | unit manager | background check, role training | none |
| Finance Staff | Finance operations | hire, authorize, segregate duties | active, suspended | finance manager | background check, finance controls training | none |
| Procurement Staff | Supply chain operations | hire, authorize, train | active, suspended | procurement manager | procurement compliance training | none |
| HR Staff | Workforce operations | hire, authorize, audit | active, suspended | HR manager | privacy and HR compliance training | none |
| ICT Staff | Technology operations | hire, grant access, train | active, suspended | ICT manager | security training, privileged access approval | none |
| Security Personnel | Physical security | hire, background check, roster | active, suspended | security supervisor | security license/checks where required | none |
| Housekeeping | Environmental services | hire, train, roster | active, inactive | facilities supervisor | infection prevention training | none |
| Drivers | Transport services | hire, license, roster | active, suspended | transport supervisor | driver license, defensive driving | none |
| Volunteers | Unpaid support | approve, onboard, supervise, exit | active, inactive | volunteer coordinator | identity check, safeguarding training | none |
| Students | Learners and placements | approve, rotate, assess, complete | student, active, completed | academic coordinator/preceptor | school letter, immunization, training | supervised only if permitted |
| Contractors | External service workforce | contract, onboard, monitor, offboard | contracted, active, expired | contract owner | identity, background, contract compliance | none unless credentialed clinician |
| Temporary Staff | Time-limited employees | appoint, roster, end assignment | temporary, active, expired | hiring manager | identity, contract, required training | role-dependent |
| Agency Staff | Third-party supplied staff | verify, roster, review, release | agency-active, suspended, released | agency coordinator and unit manager | agency attestation plus role credentials | explicit temporary privileges |

## Core business rules
- Employee numbers are unique across the enterprise and immutable after issue.
- A worker cannot hold an active clinical privilege unless all mandatory licenses and verifications are current.
- Expired professional licenses suspend dependent privileges automatically.
- Primary department assignment is required for active employees and must have non-overlapping effective dates.
- Secondary and temporary assignments cannot exceed configured concurrent assignment limits without approval.
- Reporting lines cannot be cyclic and must resolve to an active manager.
- Inactive, terminated, suspended, or expired workers cannot receive new schedules, privileges, assets, or access grants without exception approval.
- Maximum working hours, rest periods, and overtime eligibility are validated before schedule publication.
- Every material workforce change creates a lifecycle event and immutable audit entry.

# Module 01 Permissions

| Permission | Purpose | Suggested roles |
| --- | --- | --- |
| `patient.register` | Create standard, temporary, newborn, anonymous emergency, deceased, and foreign patient records. | Registrar, ED Registrar |
| `patient.view` | Search and view MPI records and duplicate candidates. | Registrar, Clinician, HIM |
| `patient.update` | Maintain demographics, identifiers, insurance, contacts, language, religion, occupation, addresses, phones, alerts, and allergies. | Registrar, HIM |
| `patient.biometrics.capture` | Capture fingerprint, face recognition, and photograph references after consent. | Registrar Supervisor, Security Enrollment |
| `patient.consents.manage` | Create, sign, revoke, and expire consent forms. | Registrar, HIM, Privacy Officer |
| `patient.deceased.mark` | Mark and verify deceased patients. | HIM, Clinician Supervisor |
| `patient.merge` | Complete patient merging after duplicate review. | MPI Analyst, HIM Supervisor |
| `patient.reports.view` | View registration, duplicate, merge, deceased, and data quality reports. | Registration Manager, HIM Manager |

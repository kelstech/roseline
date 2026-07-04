# Module 01 — Patient Registration and Master Patient Index

## Purpose
Module 01 creates and maintains the enterprise patient record in an Epic-style registration workspace. It is the source of truth for demographics, identifiers, coverage, contacts, biometric identity, consent, medical identity flags, and longitudinal Master Patient Index (MPI) reconciliation.

## Core capabilities
- **Demographics:** legal name, preferred name, sex at birth, gender identity, date and time of birth, estimated DOB flag, marital status, language, religion, nationality, occupation, employer, blood group, RH factor, photograph, barcode, and QR Code.
- **Identifiers:** MRN, National ID, Passport, foreign IDs, temporary IDs, insurance member IDs, barcode values, and QR payloads with issuing country and verification state.
- **Insurance:** multiple payer policies with priority, coverage dates, subscriber details, plan, group, member, and verification timestamps.
- **Biometrics:** consent-linked fingerprint templates, face recognition templates, and photograph references. Raw biometric data must remain in an encrypted biometric vault; the MPI stores only hashes and secure URIs.
- **Contacts:** emergency contacts, next of kin, family members, legal guardians, multiple addresses, and multiple phone numbers.
- **Clinical safety flags:** medical alerts and allergies presented during registration and patient lookup.
- **Provider context:** referring physician references for externally referred patients.
- **Consent forms:** draft, signed, revoked, and expired forms linked to identity-sensitive workflows including biometrics.

## Patient scenarios
| Scenario | Behavior |
| --- | --- |
| Standard patient | Full demographic, identifier, insurance, address, phone, and consent capture. |
| Duplicate detection | Search uses exact identifier matches, normalized names, DOB, and phone numbers; candidates scoring 50+ are shown for review. |
| Patient merging | Authorized HIM/MPI staff merge a source patient into a target patient, keep an audit snapshot, and mark the source as merged. |
| Deceased patient | Status requires a death timestamp and verification workflow before scheduling or billing rules treat the patient as deceased. |
| Newborn registration | Supports mother link, birth order, date/time of birth, temporary newborn naming, guardians, and later identity completion. |
| Temporary patient | Allows registration with limited demographics while preserving a temporary identifier for later reconciliation. |
| Anonymous emergency patient | Creates UNKNOWN/EMERGENCY identities for immediate care with emergency reason and later conversion to a known patient. |
| Foreign patient | Captures passport, foreign IDs, nationality, country of birth, foreign addresses, and international phone formats. |

## Workflow
1. Registrar opens the MPI workspace and searches before creating a patient.
2. The duplicate engine scores candidates by National ID, Passport, insurance member ID, DOB, phone, and normalized names.
3. Registrar captures demographics, multiple addresses, multiple phone numbers, insurance, contacts, family members, language, religion, occupation, and referring physician.
4. Consent forms are collected before fingerprint or face recognition capture.
5. Barcode and QR Code payloads are generated from the enterprise MRN and patient UUID.
6. Medical alerts and allergies are surfaced on the registration summary.
7. Exceptions route to MPI review queues for duplicate resolution, merge approval, anonymous emergency conversion, newborn completion, and deceased verification.

## Data protection requirements
- Encrypt National ID, Passport, insurance identifiers, biometric storage, and consent documents at rest.
- Mask sensitive identifiers by default in the frontend and reports.
- Audit every create, update, duplicate decision, merge, deceased marking, consent change, and biometric capture.
- Require role-based permissions for merge, deceased marking, biometric capture, and reports.

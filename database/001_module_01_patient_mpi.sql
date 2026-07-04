-- Roseline Module 01: Patient Registration and Master Patient Index
-- PostgreSQL schema designed for Epic-like enterprise patient identity management.

CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE TYPE patient_status AS ENUM ('active', 'temporary', 'anonymous_emergency', 'newborn', 'deceased', 'merged', 'inactive');
CREATE TYPE sex_at_birth AS ENUM ('female', 'male', 'intersex', 'unknown');
CREATE TYPE address_type AS ENUM ('home', 'mailing', 'work', 'temporary', 'foreign', 'billing');
CREATE TYPE phone_type AS ENUM ('mobile', 'home', 'work', 'emergency', 'fax', 'other');
CREATE TYPE identifier_type AS ENUM ('mrn', 'national_id', 'passport', 'insurance_member_id', 'barcode', 'qr_code', 'temporary_id', 'foreign_id');
CREATE TYPE biometric_type AS ENUM ('fingerprint', 'face_template', 'photograph');
CREATE TYPE relationship_type AS ENUM ('mother', 'father', 'spouse', 'child', 'sibling', 'guardian', 'next_of_kin', 'emergency_contact', 'other');
CREATE TYPE consent_status AS ENUM ('draft', 'signed', 'revoked', 'expired');
CREATE TYPE merge_status AS ENUM ('proposed', 'approved', 'rejected', 'completed', 'reversed');

CREATE TABLE patients (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  mrn TEXT NOT NULL UNIQUE,
  status patient_status NOT NULL DEFAULT 'active',
  legal_family_name TEXT,
  legal_given_name TEXT,
  legal_middle_name TEXT,
  preferred_name TEXT,
  sex_at_birth sex_at_birth NOT NULL DEFAULT 'unknown',
  gender_identity TEXT,
  date_of_birth DATE,
  birth_time TIME,
  is_estimated_dob BOOLEAN NOT NULL DEFAULT false,
  blood_group TEXT CHECK (blood_group IN ('A', 'B', 'AB', 'O') OR blood_group IS NULL),
  rh_factor TEXT CHECK (rh_factor IN ('positive', 'negative', 'unknown') OR rh_factor IS NULL),
  primary_language TEXT,
  religion TEXT,
  nationality TEXT,
  country_of_birth TEXT,
  marital_status TEXT,
  occupation TEXT,
  employer_name TEXT,
  referring_physician_id UUID,
  deceased_at TIMESTAMPTZ,
  death_verified_by UUID,
  newborn_mother_patient_id UUID REFERENCES patients(id),
  newborn_birth_order INTEGER,
  anonymous_reason TEXT,
  foreign_patient BOOLEAN NOT NULL DEFAULT false,
  photograph_uri TEXT,
  barcode_value TEXT UNIQUE,
  qr_code_value TEXT UNIQUE,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  created_by UUID,
  updated_by UUID,
  CONSTRAINT deceased_status_requires_date CHECK (status <> 'deceased' OR deceased_at IS NOT NULL),
  CONSTRAINT newborn_requires_birth_link CHECK (status <> 'newborn' OR date_of_birth IS NOT NULL)
);

CREATE TABLE patient_identifiers (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  patient_id UUID NOT NULL REFERENCES patients(id),
  type identifier_type NOT NULL,
  value TEXT NOT NULL,
  issuing_country TEXT,
  issued_at DATE,
  expires_at DATE,
  verified BOOLEAN NOT NULL DEFAULT false,
  active BOOLEAN NOT NULL DEFAULT true,
  UNIQUE(type, value, issuing_country)
);

CREATE TABLE patient_addresses (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  patient_id UUID NOT NULL REFERENCES patients(id),
  type address_type NOT NULL,
  line1 TEXT NOT NULL,
  line2 TEXT,
  city TEXT,
  state_region TEXT,
  postal_code TEXT,
  country TEXT NOT NULL,
  valid_from DATE DEFAULT CURRENT_DATE,
  valid_to DATE,
  preferred BOOLEAN NOT NULL DEFAULT false
);

CREATE TABLE patient_phones (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  patient_id UUID NOT NULL REFERENCES patients(id),
  type phone_type NOT NULL,
  country_code TEXT,
  number TEXT NOT NULL,
  extension TEXT,
  sms_allowed BOOLEAN NOT NULL DEFAULT false,
  preferred BOOLEAN NOT NULL DEFAULT false,
  verified BOOLEAN NOT NULL DEFAULT false
);

CREATE TABLE patient_insurances (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  patient_id UUID NOT NULL REFERENCES patients(id),
  payer_name TEXT NOT NULL,
  plan_name TEXT,
  policy_number TEXT NOT NULL,
  group_number TEXT,
  member_id TEXT NOT NULL,
  subscriber_name TEXT,
  subscriber_relationship TEXT,
  coverage_start DATE,
  coverage_end DATE,
  priority INTEGER NOT NULL DEFAULT 1,
  verified_at TIMESTAMPTZ
);

CREATE TABLE patient_biometrics (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  patient_id UUID NOT NULL REFERENCES patients(id),
  type biometric_type NOT NULL,
  template_hash TEXT NOT NULL,
  storage_uri TEXT NOT NULL,
  capture_device TEXT,
  captured_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  consent_id UUID,
  active BOOLEAN NOT NULL DEFAULT true
);

CREATE TABLE patient_contacts (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  patient_id UUID NOT NULL REFERENCES patients(id),
  relationship relationship_type NOT NULL,
  family_name TEXT NOT NULL,
  given_name TEXT NOT NULL,
  phone TEXT,
  email TEXT,
  address TEXT,
  legal_guardian BOOLEAN NOT NULL DEFAULT false,
  emergency_priority INTEGER,
  next_of_kin BOOLEAN NOT NULL DEFAULT false
);

CREATE TABLE patient_family_members (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  patient_id UUID NOT NULL REFERENCES patients(id),
  related_patient_id UUID REFERENCES patients(id),
  relationship relationship_type NOT NULL,
  display_name TEXT,
  hereditary_relevance TEXT
);

CREATE TABLE patient_consents (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  patient_id UUID NOT NULL REFERENCES patients(id),
  form_code TEXT NOT NULL,
  form_title TEXT NOT NULL,
  status consent_status NOT NULL DEFAULT 'draft',
  signed_at TIMESTAMPTZ,
  revoked_at TIMESTAMPTZ,
  document_uri TEXT,
  signer_name TEXT,
  witness_name TEXT
);

ALTER TABLE patient_biometrics ADD CONSTRAINT fk_biometrics_consent FOREIGN KEY (consent_id) REFERENCES patient_consents(id);

CREATE TABLE patient_medical_alerts (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  patient_id UUID NOT NULL REFERENCES patients(id),
  alert_type TEXT NOT NULL,
  severity TEXT NOT NULL CHECK (severity IN ('info', 'warning', 'critical')),
  description TEXT NOT NULL,
  active BOOLEAN NOT NULL DEFAULT true,
  starts_at TIMESTAMPTZ DEFAULT now(),
  ends_at TIMESTAMPTZ
);

CREATE TABLE patient_allergies (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  patient_id UUID NOT NULL REFERENCES patients(id),
  allergen TEXT NOT NULL,
  reaction TEXT,
  severity TEXT CHECK (severity IN ('mild', 'moderate', 'severe', 'life_threatening') OR severity IS NULL),
  verified BOOLEAN NOT NULL DEFAULT false,
  active BOOLEAN NOT NULL DEFAULT true
);

CREATE TABLE duplicate_candidates (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  left_patient_id UUID NOT NULL REFERENCES patients(id),
  right_patient_id UUID NOT NULL REFERENCES patients(id),
  score NUMERIC(5,2) NOT NULL,
  reasons JSONB NOT NULL DEFAULT '[]',
  status TEXT NOT NULL DEFAULT 'open' CHECK (status IN ('open', 'not_duplicate', 'merge_requested', 'resolved')),
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  UNIQUE(left_patient_id, right_patient_id),
  CHECK (left_patient_id <> right_patient_id)
);

CREATE TABLE patient_merges (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  source_patient_id UUID NOT NULL REFERENCES patients(id),
  target_patient_id UUID NOT NULL REFERENCES patients(id),
  status merge_status NOT NULL DEFAULT 'proposed',
  rationale TEXT NOT NULL,
  approved_by UUID,
  completed_by UUID,
  completed_at TIMESTAMPTZ,
  audit_snapshot JSONB NOT NULL DEFAULT '{}',
  CHECK (source_patient_id <> target_patient_id)
);

CREATE INDEX idx_patients_name_dob ON patients (legal_family_name, legal_given_name, date_of_birth);
CREATE INDEX idx_patients_status ON patients (status);
CREATE INDEX idx_patient_identifiers_value ON patient_identifiers (value);
CREATE INDEX idx_patient_phones_number ON patient_phones (number);
CREATE INDEX idx_duplicate_candidates_score ON duplicate_candidates (score DESC);

import crypto from 'node:crypto';

export const PERMISSIONS = Object.freeze({
  REGISTER_PATIENT: 'patient.register',
  VIEW_PATIENT: 'patient.view',
  UPDATE_PATIENT: 'patient.update',
  CAPTURE_BIOMETRICS: 'patient.biometrics.capture',
  MANAGE_CONSENTS: 'patient.consents.manage',
  MARK_DECEASED: 'patient.deceased.mark',
  MERGE_PATIENTS: 'patient.merge',
  VIEW_REPORTS: 'patient.reports.view'
});

export const REQUIRED_FIELDS = ['legalFamilyName', 'legalGivenName'];

export function createMrn(sequence, prefix = 'MRN') {
  return `${prefix}${String(sequence).padStart(10, '0')}`;
}

export function normalizePatient(input) {
  const status = input.status ?? (input.temporary ? 'temporary' : 'active');
  return {
    ...input,
    status,
    legalFamilyName: input.legalFamilyName?.trim() || (status === 'anonymous_emergency' ? 'UNKNOWN' : undefined),
    legalGivenName: input.legalGivenName?.trim() || (status === 'anonymous_emergency' ? 'EMERGENCY' : undefined),
    phones: input.phones ?? [],
    addresses: input.addresses ?? [],
    identifiers: input.identifiers ?? [],
    insurances: input.insurances ?? [],
    contacts: input.contacts ?? [],
    familyMembers: input.familyMembers ?? [],
    consents: input.consents ?? [],
    alerts: input.alerts ?? [],
    allergies: input.allergies ?? []
  };
}

export function validatePatient(input) {
  const patient = normalizePatient(input);
  const errors = [];
  if (!patient.dateOfBirth && !['anonymous_emergency', 'temporary'].includes(patient.status)) {
    errors.push('dateOfBirth is required unless the patient is temporary or anonymous emergency');
  }
  for (const field of REQUIRED_FIELDS) {
    if (!patient[field]) errors.push(`${field} is required`);
  }
  if (patient.status === 'deceased' && !patient.deceasedAt) errors.push('deceasedAt is required for deceased patients');
  if (patient.status === 'newborn' && !patient.newborn?.motherPatientId) errors.push('newborn.motherPatientId is required for newborn registration');
  return { ok: errors.length === 0, errors, patient };
}

function clean(value) {
  return String(value ?? '').toLowerCase().replace(/[^a-z0-9]/g, '');
}

export function duplicateScore(a, b) {
  const reasons = [];
  let score = 0;
  const aIds = new Set((a.identifiers ?? []).map((id) => `${id.type}:${clean(id.value)}:${id.issuingCountry ?? ''}`));
  for (const id of b.identifiers ?? []) {
    if (aIds.has(`${id.type}:${clean(id.value)}:${id.issuingCountry ?? ''}`)) {
      score += id.type === 'national_id' || id.type === 'passport' ? 55 : 35;
      reasons.push(`matching ${id.type}`);
    }
  }
  if (clean(a.legalFamilyName) && clean(a.legalFamilyName) === clean(b.legalFamilyName)) { score += 15; reasons.push('matching family name'); }
  if (clean(a.legalGivenName) && clean(a.legalGivenName) === clean(b.legalGivenName)) { score += 10; reasons.push('matching given name'); }
  if (a.dateOfBirth && a.dateOfBirth === b.dateOfBirth) { score += 20; reasons.push('matching date of birth'); }
  const aPhones = new Set((a.phones ?? []).map((p) => clean(p.number)));
  if ((b.phones ?? []).some((p) => aPhones.has(clean(p.number)))) { score += 10; reasons.push('matching phone'); }
  return { score: Math.min(score, 100), reasons, duplicate: score >= 75 };
}

export function findDuplicateCandidates(candidate, existingPatients) {
  return existingPatients
    .map((patient) => ({ patientId: patient.id, ...duplicateScore(candidate, patient) }))
    .filter((match) => match.score >= 50)
    .sort((a, b) => b.score - a.score);
}

export function createBarcodePayload(patient) {
  return `ROSELINE|MRN|${patient.mrn}|${patient.id}`;
}

export function createQrPayload(patient) {
  return JSON.stringify({ system: 'roseline', module: 'MPI', mrn: patient.mrn, patientId: patient.id });
}

export function hashBiometricTemplate(template) {
  return crypto.createHash('sha256').update(String(template)).digest('hex');
}

export function mergePatients(source, target, userId, rationale) {
  if (source.id === target.id) throw new Error('source and target patients must be different');
  return {
    sourcePatient: { ...source, status: 'merged', mergedIntoPatientId: target.id },
    targetPatient: {
      ...target,
      identifiers: [...(target.identifiers ?? []), ...(source.identifiers ?? [])],
      phones: [...(target.phones ?? []), ...(source.phones ?? [])],
      addresses: [...(target.addresses ?? []), ...(source.addresses ?? [])],
      alerts: [...(target.alerts ?? []), ...(source.alerts ?? [])],
      allergies: [...(target.allergies ?? []), ...(source.allergies ?? [])]
    },
    mergeRecord: {
      sourcePatientId: source.id,
      targetPatientId: target.id,
      status: 'completed',
      rationale,
      completedBy: userId,
      completedAt: new Date().toISOString()
    }
  };
}

export function buildRegistrationReport(patients) {
  return patients.reduce((report, patient) => {
    report.total += 1;
    report.byStatus[patient.status] = (report.byStatus[patient.status] ?? 0) + 1;
    if (patient.foreignPatient) report.foreignPatients += 1;
    if (patient.deceasedAt) report.deceasedPatients += 1;
    return report;
  }, { total: 0, foreignPatients: 0, deceasedPatients: 0, byStatus: {} });
}

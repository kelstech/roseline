import test from 'node:test';
import assert from 'node:assert/strict';
import { buildRegistrationReport, createMrn, duplicateScore, hashBiometricTemplate, mergePatients, validatePatient } from '../backend/src/patient-mpi.js';

test('validates required registration fields and deceased status', () => {
  assert.equal(validatePatient({ legalFamilyName: 'Doe', legalGivenName: 'Jane', dateOfBirth: '1990-01-01' }).ok, true);
  const invalid = validatePatient({ legalFamilyName: 'Doe', legalGivenName: 'Jane', dateOfBirth: '1990-01-01', status: 'deceased' });
  assert.equal(invalid.ok, false);
  assert.match(invalid.errors.join(','), /deceasedAt/);
});

test('detects high confidence duplicates using identifiers and DOB', () => {
  const a = { legalFamilyName: 'Doe', legalGivenName: 'Jane', dateOfBirth: '1990-01-01', identifiers: [{ type: 'national_id', value: 'A-123' }] };
  const b = { legalFamilyName: 'DOE', legalGivenName: 'Jane', dateOfBirth: '1990-01-01', identifiers: [{ type: 'national_id', value: 'A123' }] };
  const result = duplicateScore(a, b);
  assert.equal(result.duplicate, true);
  assert.equal(result.score, 100);
});

test('merges source identity data into target patient', () => {
  const source = { id: 'source', identifiers: [{ type: 'passport', value: 'P1' }], phones: [{ number: '555' }] };
  const target = { id: 'target', identifiers: [], phones: [], addresses: [], alerts: [], allergies: [] };
  const result = mergePatients(source, target, 'registrar', 'same patient');
  assert.equal(result.sourcePatient.status, 'merged');
  assert.equal(result.targetPatient.identifiers.length, 1);
  assert.equal(result.mergeRecord.status, 'completed');
});

test('generates reports, MRNs, and biometric hashes', () => {
  assert.equal(createMrn(42), 'MRN0000000042');
  assert.equal(hashBiometricTemplate('finger').length, 64);
  assert.deepEqual(buildRegistrationReport([{ status: 'active' }, { status: 'deceased', deceasedAt: '2026-01-01', foreignPatient: true }]), {
    total: 2,
    foreignPatients: 1,
    deceasedPatients: 1,
    byStatus: { active: 1, deceased: 1 }
  });
});

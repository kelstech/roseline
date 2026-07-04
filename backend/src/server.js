import express from 'express';
import { randomUUID } from 'node:crypto';
import { buildRegistrationReport, createBarcodePayload, createMrn, createQrPayload, findDuplicateCandidates, mergePatients, normalizePatient, PERMISSIONS, validatePatient } from './patient-mpi.js';

const app = express();
app.use(express.json({ limit: '10mb' }));
const patients = [];
let sequence = 1;

function requirePermission(permission) {
  return (req, res, next) => {
    const permissions = String(req.header('x-permissions') ?? '').split(',').map((p) => p.trim());
    if (!permissions.includes(permission)) return res.status(403).json({ error: 'forbidden', permission });
    next();
  };
}

app.get('/api/module-01/permissions', (_req, res) => res.json(PERMISSIONS));

app.post('/api/module-01/patients', requirePermission(PERMISSIONS.REGISTER_PATIENT), (req, res) => {
  const validation = validatePatient(req.body);
  if (!validation.ok) return res.status(422).json({ errors: validation.errors });
  const patient = normalizePatient({ ...validation.patient, id: randomUUID(), mrn: createMrn(sequence++) });
  patient.barcodeValue = createBarcodePayload(patient);
  patient.qrCodeValue = createQrPayload(patient);
  const duplicates = findDuplicateCandidates(patient, patients);
  patients.push(patient);
  res.status(201).json({ patient, duplicates });
});

app.get('/api/module-01/patients', requirePermission(PERMISSIONS.VIEW_PATIENT), (req, res) => {
  const q = String(req.query.q ?? '').toLowerCase();
  res.json(patients.filter((p) => !q || `${p.mrn} ${p.legalFamilyName} ${p.legalGivenName}`.toLowerCase().includes(q)));
});

app.post('/api/module-01/patients/duplicate-search', requirePermission(PERMISSIONS.VIEW_PATIENT), (req, res) => {
  res.json(findDuplicateCandidates(normalizePatient(req.body), patients));
});

app.post('/api/module-01/patients/:id/mark-deceased', requirePermission(PERMISSIONS.MARK_DECEASED), (req, res) => {
  const patient = patients.find((p) => p.id === req.params.id);
  if (!patient) return res.status(404).json({ error: 'not_found' });
  patient.status = 'deceased';
  patient.deceasedAt = req.body.deceasedAt ?? new Date().toISOString();
  res.json(patient);
});

app.post('/api/module-01/patient-merges', requirePermission(PERMISSIONS.MERGE_PATIENTS), (req, res) => {
  const source = patients.find((p) => p.id === req.body.sourcePatientId);
  const target = patients.find((p) => p.id === req.body.targetPatientId);
  if (!source || !target) return res.status(404).json({ error: 'not_found' });
  const result = mergePatients(source, target, req.header('x-user-id') ?? 'system', req.body.rationale);
  Object.assign(source, result.sourcePatient);
  Object.assign(target, result.targetPatient);
  res.json(result);
});

app.get('/api/module-01/reports/registration-summary', requirePermission(PERMISSIONS.VIEW_REPORTS), (_req, res) => {
  res.json(buildRegistrationReport(patients));
});

export default app;

if (process.env.NODE_ENV !== 'test') {
  app.listen(process.env.PORT ?? 3001, () => console.log('Module 01 MPI API listening'));
}

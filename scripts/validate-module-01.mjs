import fs from 'node:fs';

const requiredFiles = [
  'database/001_module_01_patient_mpi.sql',
  'backend/src/patient-mpi.js',
  'backend/src/server.js',
  'frontend/src/Module01PatientRegistration.jsx',
  'docs/module-01-patient-registration-mpi.md',
  'docs/api/module-01-openapi.yaml',
  'docs/security/module-01-permissions.md',
  'docs/reports/module-01-reports.md',
  'tests/patient-mpi.test.js'
];
const requiredTerms = ['Demographics', 'National ID', 'Passport', 'Insurance', 'Biometrics', 'Fingerprint', 'Face recognition', 'Emergency contacts', 'duplicate', 'merge', 'deceased', 'newborn', 'temporary', 'anonymous', 'foreign', 'Barcode', 'QR Code'];
for (const file of requiredFiles) {
  if (!fs.existsSync(file)) throw new Error(`Missing ${file}`);
}
const docs = fs.readFileSync('docs/module-01-patient-registration-mpi.md', 'utf8');
for (const term of requiredTerms) {
  if (!docs.toLowerCase().includes(term.toLowerCase())) throw new Error(`Documentation missing ${term}`);
}
console.log('Module 01 artifact validation passed');

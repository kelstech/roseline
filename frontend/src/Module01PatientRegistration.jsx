import React, { useMemo, useState } from 'react';
import { createBarcodePayload, createQrPayload, duplicateScore } from '../../backend/src/patient-mpi.js';
import './module01.css';

const emptyPatient = {
  legalFamilyName: '', legalGivenName: '', dateOfBirth: '', sexAtBirth: 'unknown', status: 'active',
  nationalId: '', passport: '', primaryLanguage: '', religion: '', bloodGroup: '', rhFactor: '', occupation: '',
  referringPhysician: '', photographUri: '', medicalAlert: '', allergy: '', phone: '', address: '', emergencyContact: '', nextOfKin: ''
};

export default function Module01PatientRegistration({ existingPatients = [], onRegister = () => {} }) {
  const [patient, setPatient] = useState(emptyPatient);
  const [savedPatient, setSavedPatient] = useState(null);
  const duplicateCandidates = useMemo(() => existingPatients
    .map((existing) => ({ ...duplicateScore(toApiPatient(patient), existing), patient: existing }))
    .filter((match) => match.score >= 50), [patient, existingPatients]);

  function update(field, value) { setPatient((current) => ({ ...current, [field]: value })); }
  function submit(event) {
    event.preventDefault();
    const registered = { ...toApiPatient(patient), id: crypto.randomUUID(), mrn: `MRN${Date.now()}` };
    registered.barcodeValue = createBarcodePayload(registered);
    registered.qrCodeValue = createQrPayload(registered);
    setSavedPatient(registered);
    onRegister(registered);
  }

  return <main className="mpi-shell">
    <header><p className="eyebrow">Module 01</p><h1>Patient Registration & Master Patient Index</h1><p>Epic-style identity workspace for complete longitudinal patient records.</p></header>
    <form className="mpi-grid" onSubmit={submit}>
      <section className="card"><h2>Demographics</h2>
        <Field label="Family name" value={patient.legalFamilyName} onChange={(v) => update('legalFamilyName', v)} />
        <Field label="Given name" value={patient.legalGivenName} onChange={(v) => update('legalGivenName', v)} />
        <Field label="Date of birth" type="date" value={patient.dateOfBirth} onChange={(v) => update('dateOfBirth', v)} />
        <Select label="Patient status" value={patient.status} onChange={(v) => update('status', v)} options={['active','temporary','anonymous_emergency','newborn','deceased']} />
        <Select label="Sex at birth" value={patient.sexAtBirth} onChange={(v) => update('sexAtBirth', v)} options={['female','male','intersex','unknown']} />
        <Field label="Language" value={patient.primaryLanguage} onChange={(v) => update('primaryLanguage', v)} />
        <Field label="Religion" value={patient.religion} onChange={(v) => update('religion', v)} />
      </section>
      <section className="card"><h2>Identity & coverage</h2>
        <Field label="National ID" value={patient.nationalId} onChange={(v) => update('nationalId', v)} />
        <Field label="Passport" value={patient.passport} onChange={(v) => update('passport', v)} />
        <Field label="Insurance member ID" value={patient.insuranceMemberId} onChange={(v) => update('insuranceMemberId', v)} />
        <Field label="Occupation" value={patient.occupation} onChange={(v) => update('occupation', v)} />
        <Field label="Referring physician" value={patient.referringPhysician} onChange={(v) => update('referringPhysician', v)} />
      </section>
      <section className="card"><h2>Clinical identity</h2>
        <Select label="Blood group" value={patient.bloodGroup} onChange={(v) => update('bloodGroup', v)} options={['','A','B','AB','O']} />
        <Select label="RH factor" value={patient.rhFactor} onChange={(v) => update('rhFactor', v)} options={['','positive','negative','unknown']} />
        <Field label="Medical alerts" value={patient.medicalAlert} onChange={(v) => update('medicalAlert', v)} />
        <Field label="Allergies" value={patient.allergy} onChange={(v) => update('allergy', v)} />
        <Field label="Photograph URI" value={patient.photographUri} onChange={(v) => update('photographUri', v)} />
      </section>
      <section className="card"><h2>Contacts</h2>
        <Field label="Phone number" value={patient.phone} onChange={(v) => update('phone', v)} />
        <Field label="Address" value={patient.address} onChange={(v) => update('address', v)} />
        <Field label="Emergency contact" value={patient.emergencyContact} onChange={(v) => update('emergencyContact', v)} />
        <Field label="Next of kin" value={patient.nextOfKin} onChange={(v) => update('nextOfKin', v)} />
      </section>
      <section className="card wide"><h2>Biometrics, consent, duplicates</h2>
        <div className="pill-row"><span>Fingerprint ready</span><span>Face recognition ready</span><span>Consent required</span></div>
        {duplicateCandidates.length ? <div className="warning">Potential duplicates: {duplicateCandidates.map((d) => `${d.patient.mrn} (${d.score})`).join(', ')}</div> : <div className="ok">No duplicate candidates above threshold.</div>}
        <button type="submit">Register patient</button>
      </section>
    </form>
    {savedPatient && <aside className="card result"><h2>Generated identifiers</h2><code>{savedPatient.barcodeValue}</code><code>{savedPatient.qrCodeValue}</code></aside>}
  </main>;
}

function toApiPatient(patient) {
  return {
    ...patient,
    identifiers: [patient.nationalId && { type: 'national_id', value: patient.nationalId }, patient.passport && { type: 'passport', value: patient.passport }, patient.insuranceMemberId && { type: 'insurance_member_id', value: patient.insuranceMemberId }].filter(Boolean),
    phones: patient.phone ? [{ type: 'mobile', number: patient.phone }] : [],
    addresses: patient.address ? [{ type: 'home', line1: patient.address, country: 'Unknown' }] : [],
    alerts: patient.medicalAlert ? [{ alertType: 'registration', severity: 'warning', description: patient.medicalAlert }] : [],
    allergies: patient.allergy ? [{ allergen: patient.allergy }] : []
  };
}

function Field({ label, value, onChange, type = 'text' }) { return <label>{label}<input type={type} value={value ?? ''} onChange={(e) => onChange(e.target.value)} /></label>; }
function Select({ label, value, onChange, options }) { return <label>{label}<select value={value} onChange={(e) => onChange(e.target.value)}>{options.map((o) => <option key={o} value={o}>{o || 'Select'}</option>)}</select></label>; }

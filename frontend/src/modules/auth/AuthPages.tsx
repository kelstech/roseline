import React from 'react';
import { Box, Button, Card, CardContent, Container, Grid, List, ListItem, ListItemText, TextField, Typography } from '@mui/material';

export type AuthPageName =
  | 'login'
  | 'forgotPassword'
  | 'resetPassword'
  | 'changePassword'
  | 'mfaEnrollment'
  | 'mfaVerification'
  | 'trustedDevices'
  | 'sessions'
  | 'profileSecurity'
  | 'deviceManagement'
  | 'emergencyAccess'
  | 'apiKeyManagement'
  | 'oauthClientManagement'
  | 'identityProviderManagement';

const pageTitles: Record<AuthPageName, string> = {
  login: 'Secure Login',
  forgotPassword: 'Forgot Password',
  resetPassword: 'Reset Password',
  changePassword: 'Change Password',
  mfaEnrollment: 'MFA Enrollment',
  mfaVerification: 'MFA Verification',
  trustedDevices: 'Trusted Devices',
  sessions: 'Active Sessions',
  profileSecurity: 'Profile Security',
  deviceManagement: 'Device Management',
  emergencyAccess: 'Emergency Access',
  apiKeyManagement: 'API Key Management',
  oauthClientManagement: 'OAuth Client Management',
  identityProviderManagement: 'Identity Provider Management',
};

function AuthShell({ page, children }: { page: AuthPageName; children: React.ReactNode }) {
  return (
    <Container maxWidth="md" sx={{ py: { xs: 3, md: 8 } }}>
      <Card component="main" aria-labelledby="auth-page-title" sx={{ borderRadius: 3 }}>
        <CardContent sx={{ p: { xs: 3, md: 5 } }}>
          <Typography id="auth-page-title" variant="h4" component="h1" gutterBottom>
            {pageTitles[page]}
          </Typography>
          <Box aria-live="polite">{children}</Box>
        </CardContent>
      </Card>
    </Container>
  );
}

export function LoginPage() {
  return (
    <AuthShell page="login">
      <Box component="form" noValidate display="grid" gap={2}>
        <TextField label="Email, username, or staff ID" name="username" autoComplete="username" required fullWidth />
        <TextField label="Password" name="password" type="password" autoComplete="current-password" required fullWidth />
        <Button type="submit" variant="contained" size="large">Continue securely</Button>
        <Button variant="text">Use single sign-on</Button>
      </Box>
    </AuthShell>
  );
}

export function PasswordRecoveryPage({ mode }: { mode: 'forgot' | 'reset' | 'change' }) {
  const page = mode === 'forgot' ? 'forgotPassword' : mode === 'reset' ? 'resetPassword' : 'changePassword';
  return (
    <AuthShell page={page}>
      <Box component="form" noValidate display="grid" gap={2}>
        {mode === 'forgot' && <TextField label="Verified email or phone" name="identifier" required fullWidth />}
        {mode !== 'forgot' && <TextField label="New password" name="newPassword" type="password" required fullWidth />}
        {mode === 'change' && <TextField label="Current password" name="currentPassword" type="password" required fullWidth />}
        <Button type="submit" variant="contained">Submit</Button>
      </Box>
    </AuthShell>
  );
}

export function MFAPage({ enrollment }: { enrollment: boolean }) {
  return (
    <AuthShell page={enrollment ? 'mfaEnrollment' : 'mfaVerification'}>
      <Box component="form" noValidate display="grid" gap={2}>
        <Typography>{enrollment ? 'Choose and verify an authenticator, passkey, SMS, email, or push factor.' : 'Enter the verification code or approve the push request.'}</Typography>
        <TextField label={enrollment ? 'Device label' : 'Verification code'} name="mfaInput" required fullWidth />
        <Button type="submit" variant="contained">{enrollment ? 'Enroll MFA' : 'Verify'}</Button>
      </Box>
    </AuthShell>
  );
}

export function SecurityListPage({ page, items }: { page: Extract<AuthPageName, 'trustedDevices' | 'sessions' | 'profileSecurity' | 'deviceManagement' | 'apiKeyManagement' | 'oauthClientManagement' | 'identityProviderManagement'>; items: string[] }) {
  return (
    <AuthShell page={page}>
      <Grid container spacing={2}>
        <Grid item xs={12}>
          <List aria-label={pageTitles[page]}>
            {items.map((item) => (
              <ListItem key={item} secondaryAction={<Button>Manage</Button>}>
                <ListItemText primary={item} secondary="Review status, last activity, expiry, and revocation controls." />
              </ListItem>
            ))}
          </List>
        </Grid>
      </Grid>
    </AuthShell>
  );
}

export function EmergencyAccessPage() {
  return (
    <AuthShell page="emergencyAccess">
      <Box component="form" noValidate display="grid" gap={2}>
        <Typography color="error">Emergency access is audited in real time and requires a clinical safety reason.</Typography>
        <TextField label="Emergency credential" name="credential" type="password" required fullWidth />
        <TextField label="Reason for access" name="reason" multiline minRows={3} required fullWidth />
        <Button type="submit" color="error" variant="contained">Request break-glass session</Button>
      </Box>
    </AuthShell>
  );
}

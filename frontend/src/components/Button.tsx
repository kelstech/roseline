import React from 'react';
import { tokens } from '../design/tokens';

type ButtonProps = React.ButtonHTMLAttributes<HTMLButtonElement> & { variant?: 'primary' | 'critical' };

export function Button({ variant = 'primary', style, ...props }: ButtonProps) {
  return <button {...props} style={{ background: tokens.colors[variant], color: 'white', border: 0, borderRadius: tokens.radius.md, padding: `${tokens.spacing.sm} ${tokens.spacing.md}`, fontFamily: tokens.typography.fontFamily, ...style }} />;
}

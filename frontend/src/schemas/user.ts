
// Based on backend/app/schemas/organization.py
export interface Organization {
  id: number;
  name: string;
  level: number;
  parent_id: number | null;
}

export type UserRole = 'employee' | 'team_lead' | 'dept_head' | 'admin';

// Based on backend/app/schemas/user.py
export interface User {
  id: number;
  username: string;
  email: string;
  full_name: string | null;
  role: UserRole;
  organization_id: number | null;
  organization?: Organization | null; // Optional, as it might not always be fetched
}

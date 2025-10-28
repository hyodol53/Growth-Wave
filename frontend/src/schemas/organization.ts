
// Based on backend/app/schemas/organization.py
export interface Organization {
  id: number;
  name: string;
  level: number;
  parent_id: number | null;
  department_grade: string | null;
}

export type OrganizationCreate = Omit<Organization, 'id'>;
export type OrganizationUpdate = Partial<OrganizationCreate>;

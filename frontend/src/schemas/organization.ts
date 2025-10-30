import { DepartmentGrade } from "./evaluation";

export interface Organization {
  id: number;
  name: string;
  level: number; // Renamed from organization_level
  parent_id: number | null;
  department_grade?: DepartmentGrade;
}

export interface OrganizationCreate {
    name: string;
    level: number; // Renamed from organization_level
    parent_id?: number | null;
}

export type OrganizationUpdate = Partial<OrganizationCreate>;
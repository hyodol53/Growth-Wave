import type { FinalEvaluation } from './evaluation';

// Based on backend/app/schemas/organization.py
export interface Organization {
  id: number;
  name: string;
  level: number;
  parent_id: number | null;
}

export enum UserRole {
  EMPLOYEE = 'employee',
  TEAM_LEAD = 'team_lead',
  DEPT_HEAD = 'dept_head',
  CENTER_HEAD = 'center_head',
  ADMIN = 'admin',
}

export type User = {
  id: number;
  username: string;
  email: string;
  full_name: string | null;
  role: UserRole;
  organization_id: number | null;
  title: string | null;
};

export interface UserCreate {
    email: string;
    full_name?: string;
    username: string;
    role: UserRole;
    organization_id?: number;
    password?: string;
}

export interface UserUpdate extends Partial<UserCreate> {}



// Based on backend GET /api/v1/users/me/history response

export interface ProjectHistoryItem {

    project_id: number;

    project_name: string;

    participation_weight: number;

    is_pm: boolean;

}



export interface UserHistoryEntry {

    evaluation_period: string;

    final_evaluation: FinalEvaluation | null;

    projects: ProjectHistoryItem[];

}



export type UserHistoryResponse = {

    history: Record<string, UserHistoryEntry>;

};

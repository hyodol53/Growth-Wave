
import type { User } from './user';
import type { Organization } from './organization';

// Based on backend/app/schemas/project.py
export interface Project {
    id: number;
    name: string;
    description: string | null;
    start_date: string; // ISO date string
    end_date: string;   // ISO date string
    pm_id: number;
    owner_org_id: number;
    pm?: User;
    owner_org?: Organization;
}

export type ProjectCreate = Omit<Project, 'id' | 'pm' | 'owner_org'>;
export type ProjectUpdate = Partial<ProjectCreate>;

// Based on backend/app/schemas/project_member.py
export interface ProjectMember {
    user_id: number;
    project_id: number;
    participation_weight: number;
}

// Based on backend GET /api/v1/projects/{project_id}/members response
export interface ProjectMemberDetails {
    user_id: number;
    full_name: string;
    is_pm: boolean;
    participation_weight: number;
}

export interface UserProjectWeight {
    project_id: number;
    project_name: string;
    participation_weight: number;
}

export interface UserProjectWeightsUpdate {
    weights: UserProjectWeight[];
}

export interface UserProjectWeight {
    project_id: number;
    project_name: string;
    participation_weight: number;
}

export interface UserProjectWeightsUpdate {
    weights: UserProjectWeight[];
}

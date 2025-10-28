
import { User } from './user';
import { Organization } from './organization';

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

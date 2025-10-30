
export interface Project {
    id: number;
    name: string;
    description?: string;
    pm_id: number;
    evaluation_period_id: number;
    start_date?: string;
    end_date?: string;
    created_at: string;
    updated_at: string;
}

export interface ProjectCreate {
    name: string;
    description?: string;
    pm_id: number;
    evaluation_period_id: number;
    start_date?: string;
    end_date?: string;
}

export interface ProjectUpdate {
    name?: string;
    description?: string;
    pm_id?: number;
    evaluation_period_id?: number;
    start_date?: string;
    end_date?: string;
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

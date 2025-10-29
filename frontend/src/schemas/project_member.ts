// frontend/src/schemas/project_member.ts

export interface ProjectMemberBase {
    user_id: number;
    project_id: number;
    is_pm: boolean;
    participation_weight: number;
  }
  
  export interface ProjectMemberCreate extends ProjectMemberBase {}
  
  export interface ProjectMemberUpdate {
    participation_weight?: number;
  }
  
  export interface ProjectMemberInDB extends ProjectMemberBase {
    id: number;
  }  
  export interface ProjectMember extends ProjectMemberInDB {}
  
  export interface ProjectMemberDetail {
    user_id: number;
    full_name: string;
    is_pm: boolean;
    participation_weight: number;
  }
  
  export interface ProjectMemberAdd {
    user_id: number;
    is_pm: boolean;
  }
  
  export interface ProjectWeight {
    project_id: number;
    participation_weight: number;
  }
  
  export interface UserProjectWeights {
    weights: ProjectWeight[];
  }
  
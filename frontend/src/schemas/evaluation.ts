export interface EvaluationPeriod {
    id: number;
    name: string;
    start_date: string;
    end_date: string;
    is_active: boolean;
  }
  
  export interface EvaluationPeriodCreate {
      name: string;
      start_date: string;
      end_date: string;
  }
  
  export type EvaluationPeriodUpdate = Partial<EvaluationPeriodCreate>;
  
  
  export enum DepartmentGrade {
      S = "S",
      A = "A",
      B = "B",
  }
  
  export interface DepartmentGradeRatio {
      id: number;
      department_grade: DepartmentGrade;
      s_ratio: number;
      a_ratio: number;
      b_ratio: number;
  }
  
  export interface DepartmentGradeRatioCreate {
      department_grade: DepartmentGrade;
      s_ratio: number;
      a_ratio: number;
      b_ratio: number;
  }
  
  export type DepartmentGradeRatioUpdate = Partial<DepartmentGradeRatioCreate>;
  
  
  export enum UserRole {
      EMPLOYEE = "employee",
      TEAM_LEAD = "team_lead",
      DEPT_HEAD = "dept_head",
      ADMIN = "admin",
  }
  
  export enum EvaluationItem {
      PEER_REVIEW = "peer_review",
      PM_REVIEW = "pm_review",
      QUALITATIVE_REVIEW = "qualitative_review",
  }
  
  export interface EvaluationWeight {
      id: number;
      user_role: UserRole;
      item: EvaluationItem;
      weight: number;
  }
  
  export interface EvaluationWeightCreate {
      user_role: UserRole;
      item: EvaluationItem;
      weight: number;
  }
  
  export type EvaluationWeightUpdate = Partial<EvaluationWeightCreate>;

export interface FinalEvaluation {
    id: number;
    evaluatee_id: number;
    evaluation_period: string;
    peer_score: number;
    pm_score: number;
    qualitative_score: number;
    final_score: number;
    grade: string | null;
}

export interface PeerFeedback {
    id: number;
    evaluator_id: number;
    evaluatee_id: number;
    project_id: number;
    evaluation_period: string;
    score: number;
    feedback: string;
}

export interface ManagerEvaluationView {
    final_evaluation: FinalEvaluation | null;
    peer_feedback: PeerFeedback[];
}

export interface GradeAdjustment {
    user_id: number;
    grade: string;
}

export interface GradeAdjustmentRequest {
    adjustments: GradeAdjustment[];
}

export interface PeerEvaluationCreate {
    evaluations: {
        project_id: number;
        evaluatee_id: number;
        score: number;
        feedback: string;
    }[];
}

export interface PmEvaluationCreate {
    evaluations: {
        project_id: number;
        evaluatee_id: number;
        score: number;
    }[];
}

export interface QualitativeEvaluationCreate {
    evaluations: {
        evaluatee_id: number;
        score: number;
    }[];
}
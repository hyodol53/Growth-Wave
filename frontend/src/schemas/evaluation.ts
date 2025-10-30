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

export interface Evaluation {
    id: number;
    name: string;
}

export interface MyEvaluationResult {
    evaluation_period: string;
    grade: string | null;
    pm_scores: {
        project_name: string;
        pm_name: string;
        score: number;
    }[];
}

export interface PeerEvaluation {
    id: number;
    project_id: number;
    evaluator_id: number;
    evaluatee_id: number;
    scores: number[];
    comment: string | null;
}

export interface PmEvaluation {
    id: number;
    project_id: number;
    evaluator_id: number;
    evaluatee_id: number;
    score: number;
    comment: string | null;
}

export interface QualitativeEvaluation {
    id: number;
    evaluator_id: number;
    evaluatee_id: number;
    score: number;
    comment: string | null;
}

export interface Evaluation {
    id: number;
    name: string;
}

export interface MyEvaluationResult {
    evaluation_period: string;
    grade: string | null;
    pm_scores: {
        project_name: string;
        pm_name: string;
        score: number;
    }[];
}

export interface PeerEvaluation {
    id: number;
    project_id: number;
    evaluator_id: number;
    evaluatee_id: number;
    scores: number[];
    comment: string | null;
}

export interface PmEvaluation {
    id: number;
    project_id: number;
    evaluator_id: number;
    evaluatee_id: number;
    score: number;
    comment: string | null;
}

export interface QualitativeEvaluation {
    id: number;
    evaluator_id: number;
    evaluatee_id: number;
    score: number;
    comment: string | null;
}

export interface PeerEvaluationCreate {
    project_id: number;
    evaluatee_id: number;
    scores: number[];
    comment?: string | null;
}
export interface PeerEvaluationUpdate extends PeerEvaluationCreate {}

export interface PmEvaluationCreate {
    project_id: number;
    evaluatee_id: number;
    score: number;
    comment?: string | null;
}
export interface PmEvaluationUpdate extends PmEvaluationCreate {}

export interface QualitativeEvaluationUpdate {
    evaluatee_id: number;
    score: number;
    comment?: string | null;
}

export interface FinalEvaluation {
  evaluatee_id: number;
  evaluation_period: string;
  peer_score: number;
  pm_score: number;
  qualitative_score: number;
  final_score: number;
  grade: string | null;
  id: number;
}

export type FinalEvaluationHistory = FinalEvaluation;

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
  adjusted_grade: string;
}



export interface EvaluationPeriod {

  id: number;

  name: string;

  start_date: string;

  end_date: string;

}



export interface EvaluatedUser {

  user_id: number;

  full_name: string;

  title: string;

  organization_name: string;

}



export interface DetailedProjectEvaluation {

  project_id: number;

  project_name: string;

  participation_weight: number;

  peer_evaluation_score: number | null;

  pm_evaluation_score: number | null;

  peer_feedback: string[];

}



export interface DetailedQualitativeEvaluation {

  score: number | null;

  comment: string | null;

}



export interface DetailedEvaluationResult {

  status: 'COMPLETED' | 'IN_PROGRESS';

  user_info: {

    user_id: number;

    full_name: string;

    title: string;

    organization_name: string;

  };

  final_evaluation: {

    grade: string | null;

    final_score: number | null;

  } | null;

  project_evaluations: DetailedProjectEvaluation[];

  qualitative_evaluation: DetailedQualitativeEvaluation | null;

}





// For submitting evaluations (POST)
export interface PeerEvaluationSubmit {
    evaluations: {
        project_id: number;
        evaluatee_id: number;
        scores: number[];
        comment?: string;
    }[];
}

export interface PmEvaluationSubmit {
    evaluations: {
        project_id: number;
        evaluatee_id: number;
        score: number;
        comment?: string;
    }[];
}

export interface QualitativeEvaluationCreate {
    evaluations: {
        evaluatee_id: number;
        score: number;
    }[];
}

// For fetching evaluation data (GET)
interface PeerToEvaluate {
    evaluatee_id: number;
    evaluatee_name: string;
    scores: (number | null)[];
    comment: string | null;
}



export interface PeerEvaluationData {

    project_id: number;

    project_name: string;

    status: 'NOT_STARTED' | 'IN_PROGRESS' | 'COMPLETED';

    peers_to_evaluate: PeerToEvaluate[];

}







// Assuming PM evaluation data has a similar structure



export interface PmEvaluationData {



    project_id: number;



    project_name: string;



    status: 'NOT_STARTED' | 'IN_PROGRESS' | 'COMPLETED';



    members_to_evaluate: MemberToEvaluate[];



}







interface MemberToEvaluate {



    evaluatee_id: number;



    evaluatee_name: string;



    score: number | null;



    comment: string | null;



}







export interface MyEvaluationTask {



    project_id: number;



    project_name: string;



    user_role_in_project: 'PM' | 'MEMBER';



}





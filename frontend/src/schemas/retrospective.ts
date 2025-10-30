// frontend/src/schemas/retrospective.ts

export interface Retrospective {
  id: number;
  user_id: number;
  title: string;
  content: string;
  evaluation_period_id?: number | null;
  created_at: string;
  updated_at?: string | null;
}

export interface RetrospectiveCreate {
  title: string;
  content: string;
  evaluation_period_id?: number;
}

export interface RetrospectiveUpdate {
  title?: string;
  content?: string;
}

export interface GeneratedRetrospective {
  content: string;
}

export interface GenerateRetrospectivePayload {
  start_date: string;
  end_date: string;
}
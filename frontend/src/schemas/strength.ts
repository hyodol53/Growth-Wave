export interface Strength {
    id: number;
    hashtag: string;
}

export interface StrengthStat {
    hashtag: string;
    count: number;
}

export interface StrengthProfile {
    user_id: number;
    full_name: string;
    total_praises: number;
    strengths: StrengthStat[];
}
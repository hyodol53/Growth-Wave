import type { StrengthProfile } from './strength';

export interface GrowthAndCultureReport {
  strength_profile: StrengthProfile;
  collaboration_summary: {
    message: string;
  };
}

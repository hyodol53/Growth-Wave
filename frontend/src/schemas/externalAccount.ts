// frontend/src/schemas/externalAccount.ts

export interface ExternalAccount {
  id: number;
  provider: 'jira' | 'bitbucket';
  account_id: string;
}

export interface ExternalAccountCreate {
  provider: 'jira' | 'bitbucket';
  account_id: string;
  credentials: string;
}

// API response types matching backend schemas

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
}

export interface Organization {
  id: string;
  name: string;
  slug: string;
  industry: string | null;
  company_size: string | null;
  cloud_providers: Record<string, unknown> | null;
  tech_stack: Record<string, unknown> | null;
  settings: Record<string, unknown> | null;
  created_at: string;
  updated_at: string;
}

export interface User {
  id: string;
  org_id: string;
  keycloak_id: string;
  email: string;
  full_name: string;
  role: string;
  department: string | null;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface Framework {
  id: string;
  name: string;
  version: string;
  category: string | null;
  description: string | null;
  is_active: boolean;
  domains?: FrameworkDomain[];
  created_at: string;
  updated_at: string;
}

export interface FrameworkDomain {
  id: string;
  framework_id: string;
  code: string;
  name: string;
  description: string | null;
  sort_order: number;
  requirements?: FrameworkRequirement[];
  created_at: string;
}

export interface FrameworkRequirement {
  id: string;
  domain_id: string;
  code: string;
  title: string;
  description: string | null;
  sort_order: number;
  objectives?: ControlObjective[];
  created_at: string;
}

export interface ControlObjective {
  id: string;
  requirement_id: string;
  code: string;
  title: string;
  description: string | null;
  sort_order: number;
  created_at: string;
}

export interface ControlTemplate {
  id: string;
  template_code: string;
  title: string;
  domain: string;
  description: string | null;
  implementation_guidance: string | null;
  test_procedure: string | null;
  automation_level: string;
  variables: Record<string, unknown> | null;
  created_at: string;
  updated_at: string;
}

export interface Control {
  id: string;
  org_id: string;
  template_id: string | null;
  title: string;
  description: string | null;
  implementation_details: string | null;
  owner_id: string | null;
  status: ControlStatus;
  effectiveness: string | null;
  automation_level: string;
  test_procedure: string | null;
  last_test_date: string | null;
  last_test_result: string | null;
  agent_run_id: string | null;
  framework_mappings?: ControlFrameworkMapping[];
  created_at: string;
  updated_at: string;
}

export type ControlStatus =
  | "draft"
  | "implemented"
  | "partially_implemented"
  | "not_implemented"
  | "not_applicable";

export interface ControlStats {
  total: number;
  draft: number;
  implemented: number;
  partially_implemented: number;
  not_implemented: number;
  not_applicable: number;
}

export interface Evidence {
  id: string;
  org_id: string;
  control_id: string;
  template_id: string | null;
  title: string;
  status: string;
  collected_at: string | null;
  expires_at: string | null;
  artifact_url: string | null;
  artifact_hash: string | null;
  data: Record<string, unknown> | null;
  collection_method: string;
  collector: string | null;
  created_at: string;
  updated_at: string;
}

export interface EvidenceTemplate {
  id: string;
  template_code: string;
  title: string;
  description: string | null;
  evidence_type: string;
  format: string | null;
  collection_method: string;
  refresh_frequency: string | null;
  retention_period: string | null;
  fields: Record<string, unknown> | null;
  pass_criteria: Record<string, unknown> | null;
  integrations: Record<string, unknown> | null;
  created_at: string;
  updated_at: string;
}

export interface AgentRun {
  id: string;
  org_id: string;
  agent_type: string;
  trigger: string;
  status: AgentRunStatus;
  input_data: Record<string, unknown> | null;
  output_data: Record<string, unknown> | null;
  error_message: string | null;
  started_at: string | null;
  completed_at: string | null;
  tokens_used: number | null;
  created_at: string;
  updated_at: string;
}

export type AgentRunStatus = "pending" | "running" | "completed" | "failed";

export interface AgentRunTrigger {
  framework_id: string;
  company_context?: Record<string, unknown>;
}

export interface UserInfo {
  keycloak_id: string;
  email: string;
  full_name: string;
  role: string;
  org_id: string | null;
}

// Policies

export type PolicyStatus =
  | "draft"
  | "in_review"
  | "approved"
  | "published"
  | "archived";

export interface Policy {
  id: string;
  org_id: string;
  template_id: string | null;
  title: string;
  content: string | null;
  version: string;
  status: PolicyStatus;
  owner_id: string | null;
  approved_by_id: string | null;
  approved_at: string | null;
  published_at: string | null;
  next_review_date: string | null;
  framework_ids: string[] | null;
  control_ids: string[] | null;
  agent_run_id: string | null;
  created_at: string;
  updated_at: string;
}

export interface PolicyStats {
  total: number;
  draft: number;
  in_review: number;
  approved: number;
  published: number;
  archived: number;
}

export interface PolicyTemplate {
  id: string;
  template_code: string;
  title: string;
  description: string | null;
  category: string;
  sections: string[] | null;
  variables: string[] | null;
  content_template: string | null;
  required_by_frameworks: string[] | null;
  review_frequency: string | null;
  created_at: string;
  updated_at: string;
}

// Control Framework Mapping (for control detail page)

export interface ControlFrameworkMapping {
  id: string;
  control_id: string;
  framework_id: string;
  requirement_id: string | null;
  objective_id: string | null;
  framework_name: string | null;
  requirement_code: string | null;
  requirement_title: string | null;
}

// Risk Register

export type RiskCategory = "operational" | "security" | "compliance" | "financial";
export type RiskLevel = "critical" | "high" | "medium" | "low";
export type RiskStatus = "identified" | "assessed" | "treating" | "accepted" | "closed";

export interface Risk {
  id: string;
  org_id: string;
  title: string;
  description: string | null;
  category: RiskCategory;
  likelihood: number;
  impact: number;
  risk_score: number;
  risk_level: RiskLevel;
  status: RiskStatus;
  treatment_plan: string | null;
  treatment_type: string | null;
  treatment_status: string | null;
  treatment_due_date: string | null;
  residual_likelihood: number | null;
  residual_impact: number | null;
  residual_score: number | null;
  owner_id: string | null;
  reviewer_id: string | null;
  last_review_date: string | null;
  next_review_date: string | null;
  control_mappings?: RiskControlMapping[];
  created_at: string;
  updated_at: string;
}

export interface RiskControlMapping {
  id: string;
  risk_id: string;
  control_id: string;
  effectiveness: string;
  notes: string | null;
}

export interface RiskStats {
  total: number;
  by_status: Record<string, number>;
  by_risk_level: Record<string, number>;
  average_score: number;
}

export interface RiskMatrixCell {
  likelihood: number;
  impact: number;
  count: number;
  risk_ids: string[];
}

export interface RiskMatrixResponse {
  cells: RiskMatrixCell[];
}

// Integrations

export interface Integration {
  id: string;
  org_id: string;
  provider: string;
  name: string;
  status: string;
  config: Record<string, unknown> | null;
  credentials_ref: string | null;
  last_sync_at: string | null;
  created_at: string;
  updated_at: string;
}

export interface CollectionJob {
  id: string;
  org_id: string;
  integration_id: string;
  evidence_template_id: string | null;
  control_id: string | null;
  status: string;
  collector_type: string;
  result_data: Record<string, unknown> | null;
  evidence_id: string | null;
  error_message: string | null;
  created_at: string;
  updated_at: string;
}

export interface ProviderInfo {
  provider: string;
  name: string;
  description: string;
  collector_types: string[];
}

// Audits

export type AuditStatus = "planning" | "preparation" | "fieldwork" | "reporting" | "completed" | "closed";

export interface Audit {
  id: string;
  org_id: string;
  title: string;
  framework_id: string | null;
  audit_type: string;
  status: AuditStatus;
  auditor_firm: string | null;
  lead_auditor_name: string | null;
  scheduled_start: string | null;
  scheduled_end: string | null;
  readiness_score: number | null;
  created_at: string;
  updated_at: string;
}

export interface AuditFinding {
  id: string;
  audit_id: string;
  org_id: string;
  control_id: string | null;
  title: string;
  description: string | null;
  severity: string;
  status: string;
  remediation_plan: string | null;
  remediation_due_date: string | null;
  remediation_owner_id: string | null;
  created_at: string;
  updated_at: string;
}

export interface AuditorAccessToken {
  id: string;
  audit_id: string;
  auditor_email: string;
  auditor_name: string | null;
  permissions: Record<string, unknown> | null;
  is_active: boolean;
  expires_at: string;
  token?: string;
  created_at: string;
  updated_at: string;
}

export interface ReadinessScore {
  overall_score: number;
  controls_score: number;
  evidence_score: number;
  policies_score: number;
  risks_score: number;
  controls_implemented: number;
  controls_total: number;
  evidence_collected: number;
  evidence_total: number;
  policies_published: number;
  policies_total: number;
  risks_treated: number;
  risks_total: number;
}

// Onboarding

export interface OnboardingWizardInput {
  company_name: string;
  industry: string;
  company_size: string;
  cloud_providers: string[];
  tech_stack: string[];
  departments: string[];
  target_framework_ids: string[];
  compliance_timeline?: string;
  special_requirements?: string;
}

export interface OnboardingSession {
  id: string;
  org_id: string;
  status: string;
  input_data: Record<string, unknown> | null;
  progress: Record<string, unknown> | null;
  results: Record<string, unknown> | null;
  agent_run_ids: Record<string, unknown> | null;
  created_at: string;
  updated_at: string;
}

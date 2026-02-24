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

// Incidents

export type IncidentSeverity = "P1" | "P2" | "P3" | "P4";
export type IncidentStatus = "open" | "investigating" | "resolved" | "closed";

export interface Incident {
  id: string;
  org_id: string;
  title: string;
  description: string | null;
  severity: IncidentSeverity;
  status: IncidentStatus;
  category: string | null;
  assigned_to_id: string | null;
  detected_at: string | null;
  resolved_at: string | null;
  post_mortem_notes: string | null;
  related_control_ids: string[] | null;
  timeline_events?: IncidentTimelineEvent[];
  created_at: string;
  updated_at: string;
}

export interface IncidentTimelineEvent {
  id: string;
  incident_id: string;
  actor_id: string | null;
  event_type: string;
  description: string;
  occurred_at: string;
  created_at: string;
}

export interface IncidentStats {
  total: number;
  by_status: Record<string, number>;
  by_severity: Record<string, number>;
  open_p1_count: number;
  avg_resolution_hours: number;
}

// Vendors

export type VendorRiskTier = "critical" | "high" | "medium" | "low";
export type VendorStatus = "active" | "under_review" | "terminated";

export interface Vendor {
  id: string;
  org_id: string;
  name: string;
  category: string | null;
  website: string | null;
  risk_tier: VendorRiskTier;
  status: VendorStatus;
  contact_name: string | null;
  contact_email: string | null;
  contract_start_date: string | null;
  contract_end_date: string | null;
  last_assessment_date: string | null;
  next_assessment_date: string | null;
  assessment_score: number | null;
  notes: string | null;
  tags: string[] | null;
  assessments?: VendorAssessment[];
  created_at: string;
  updated_at: string;
}

export interface VendorAssessment {
  id: string;
  vendor_id: string;
  org_id: string;
  assessed_by_id: string | null;
  assessment_date: string | null;
  score: number | null;
  risk_tier_assigned: string | null;
  notes: string | null;
  questionnaire_data: Record<string, unknown> | null;
  created_at: string;
  updated_at: string;
}

export interface VendorStats {
  total: number;
  by_risk_tier: Record<string, number>;
  by_status: Record<string, number>;
  expiring_contracts_count: number;
}

// Training

export interface TrainingCourse {
  id: string;
  org_id: string;
  title: string;
  description: string | null;
  content_url: string | null;
  course_type: string;
  required_roles: string[] | null;
  duration_minutes: number | null;
  is_required: boolean;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface TrainingAssignment {
  id: string;
  org_id: string;
  course_id: string;
  user_id: string;
  status: string;
  due_date: string | null;
  completed_at: string | null;
  score: number | null;
  attempts: number;
  assigned_by_id: string | null;
  created_at: string;
  updated_at: string;
}

export interface TrainingStats {
  total_courses: number;
  assigned: number;
  completed: number;
  overdue: number;
  completion_rate_pct: number;
}

// Access Reviews

export interface AccessReviewCampaign {
  id: string;
  org_id: string;
  title: string;
  description: string | null;
  reviewer_id: string | null;
  status: string;
  due_date: string | null;
  completed_at: string | null;
  entry_count: number;
  pending_count: number;
  created_at: string;
  updated_at: string;
}

export interface AccessReviewEntry {
  id: string;
  campaign_id: string;
  org_id: string;
  user_name: string;
  user_email: string;
  system_name: string;
  resource: string | null;
  current_access: string | null;
  decision: string | null;
  decided_by_id: string | null;
  decided_at: string | null;
  notes: string | null;
  created_at: string;
  updated_at: string;
}

export interface AccessReviewStats {
  total_campaigns: number;
  active_campaigns: number;
  total_entries: number;
  pending_decisions: number;
  approved: number;
  revoked: number;
}

// Monitoring

export interface MonitorRule {
  id: string;
  org_id: string;
  control_id: string | null;
  title: string;
  description: string | null;
  check_type: string;
  schedule: string;
  is_active: boolean;
  config: Record<string, unknown> | null;
  last_checked_at: string | null;
  last_result: string | null;
  created_at: string;
  updated_at: string;
}

export interface MonitorAlert {
  id: string;
  org_id: string;
  rule_id: string;
  severity: string;
  status: string;
  title: string;
  details: Record<string, unknown> | null;
  triggered_at: string | null;
  resolved_at: string | null;
  acknowledged_by_id: string | null;
  created_at: string;
  updated_at: string;
}

export interface MonitoringStats {
  total_rules: number;
  active_rules: number;
  open_alerts: number;
  by_severity: Record<string, number>;
}

// Questionnaires

export interface Questionnaire {
  id: string;
  org_id: string;
  title: string;
  source: string | null;
  status: string;
  questions: Record<string, unknown>[] | null;
  total_questions: number;
  answered_count: number;
  responses?: QuestionnaireResponseItem[];
  created_at: string;
  updated_at: string;
}

export interface QuestionnaireResponseItem {
  id: string;
  questionnaire_id: string;
  org_id: string;
  question_id: string;
  question_text: string;
  answer: string | null;
  confidence: number | null;
  source_type: string | null;
  source_id: string | null;
  is_approved: boolean;
  approved_by_id: string | null;
  created_at: string;
  updated_at: string;
}

export interface QuestionnaireStats {
  total: number;
  draft: number;
  in_progress: number;
  completed: number;
  submitted: number;
}

// Trust Center

export interface TrustCenterConfig {
  id: string;
  org_id: string;
  is_published: boolean;
  slug: string;
  headline: string | null;
  description: string | null;
  contact_email: string | null;
  logo_url: string | null;
  certifications: string[] | null;
  branding: Record<string, unknown> | null;
  created_at: string;
  updated_at: string;
}

export interface TrustCenterDocument {
  id: string;
  org_id: string;
  title: string;
  document_type: string | null;
  is_public: boolean;
  requires_nda: boolean;
  file_url: string | null;
  description: string | null;
  valid_until: string | null;
  sort_order: number;
  created_at: string;
  updated_at: string;
}

// Reports

export interface Report {
  id: string;
  org_id: string;
  title: string;
  report_type: string;
  format: string;
  status: string;
  parameters: Record<string, unknown> | null;
  generated_at: string | null;
  file_url: string | null;
  requested_by_id: string | null;
  error_message: string | null;
  created_at: string;
  updated_at: string;
}

export interface ReportStats {
  total: number;
  by_type: Record<string, number>;
  by_status: Record<string, number>;
}

// Role constants
export const ROLES = {
  SUPER_ADMIN: "super_admin",
  ADMIN: "admin",
  COMPLIANCE_MANAGER: "compliance_manager",
  CONTROL_OWNER: "control_owner",
  EMPLOYEE: "employee",
  EXECUTIVE: "executive",
  AUDITOR_INTERNAL: "auditor_internal",
  AUDITOR_EXTERNAL: "auditor_external",
} as const;

export type Role = (typeof ROLES)[keyof typeof ROLES];

// Agent trigger types for new agents
export interface AgentRunTriggerGeneric {
  framework_id?: string;
  company_context?: Record<string, unknown>;
  vendor_id?: string;
  audit_id?: string;
  control_ids?: string[];
}

// Framework builder types
export interface FrameworkCreate {
  name: string;
  version: string;
  category?: string;
  description?: string;
}

export interface DomainCreate {
  code: string;
  name: string;
  description?: string;
}

export interface RequirementCreate {
  code: string;
  title: string;
  description?: string;
}

// Notifications

export interface Notification {
  id: string;
  org_id: string;
  user_id: string | null;
  channel: string;
  category: string;
  title: string;
  message: string;
  severity: string;
  entity_type: string | null;
  entity_id: string | null;
  is_read: boolean;
  read_at: string | null;
  sent_at: string | null;
  metadata: Record<string, unknown> | null;
  created_at: string;
  updated_at: string;
}

export interface NotificationStats {
  total: number;
  unread: number;
  by_category: Record<string, number>;
  by_severity: Record<string, number>;
}

// Audit Logs

export interface AuditLogEntry {
  id: string;
  org_id: string;
  actor_type: string;
  actor_id: string;
  action: string;
  entity_type: string;
  entity_id: string;
  changes: Record<string, unknown> | null;
  ip_address: string | null;
  timestamp: string;
}

export interface AuditLogStats {
  total: number;
  by_action: Record<string, number>;
  by_entity_type: Record<string, number>;
}

// Auditor Marketplace

export interface AuditorProfile {
  id: string;
  user_id: string;
  firm_name: string | null;
  bio: string | null;
  credentials: string[] | null;
  specializations: string[] | null;
  years_experience: number | null;
  location: string | null;
  hourly_rate: number | null;
  is_verified: boolean;
  verified_at: string | null;
  is_public: boolean;
  rating: number | null;
  total_audits: number;
  website_url: string | null;
  linkedin_url: string | null;
  user_name: string | null;
  user_email: string | null;
  created_at: string;
  updated_at: string;
}

// Gap Analysis

export interface GapAnalysis {
  framework_id: string;
  total_requirements: number;
  covered_count: number;
  partial_count: number;
  gap_count: number;
  coverage_percentage: number;
  covered: GapAnalysisEntry[];
  partial: GapAnalysisEntry[];
  gaps: GapAnalysisEntry[];
}

export interface GapAnalysisEntry {
  requirement_id: string;
  code: string;
  title: string;
  controls: { id: string; title: string; status: string }[];
}

export interface CrossFrameworkMatrix {
  total_controls: number;
  multi_framework_controls: number;
  deduplication_opportunity: number;
  frameworks: FrameworkSummary[];
  matrix: MatrixRow[];
}

export interface FrameworkSummary {
  framework_id: string;
  framework_name: string;
  total_requirements: number;
  mapped_controls: number;
  implemented_controls: number;
  coverage_pct: number;
}

export interface MatrixRow {
  control_id: string;
  control_title: string;
  status: string;
  framework_ids: string[];
  framework_count: number;
}

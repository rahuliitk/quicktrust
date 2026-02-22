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

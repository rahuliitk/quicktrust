"use client";

import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import api from "@/lib/api";
import type {
  Framework,
  FrameworkCreate,
  DomainCreate,
  RequirementCreate,
  Control,
  ControlStats,
  ControlTemplate,
  EvidenceTemplate,
  Evidence,
  AgentRun,
  AgentRunTrigger,
  AgentRunTriggerGeneric,
  Organization,
  Policy,
  PolicyStats,
  PolicyTemplate,
  PaginatedResponse,
  Risk,
  RiskStats,
  RiskMatrixResponse,
  Integration,
  CollectionJob,
  ProviderInfo,
  Audit,
  AuditFinding,
  AuditorAccessToken,
  ReadinessScore,
  OnboardingSession,
  OnboardingWizardInput,
  Incident,
  IncidentStats,
  IncidentTimelineEvent,
  Vendor,
  VendorStats,
  VendorAssessment,
  TrainingCourse,
  TrainingAssignment,
  TrainingStats,
  AccessReviewCampaign,
  AccessReviewEntry,
  AccessReviewStats,
  MonitorRule,
  MonitorAlert,
  MonitoringStats,
  Questionnaire,
  QuestionnaireStats,
  TrustCenterConfig,
  TrustCenterDocument,
  Report,
  ReportStats,
} from "@/lib/types";

// Frameworks
export function useFrameworks() {
  return useQuery({
    queryKey: ["frameworks"],
    queryFn: () => api.get<Framework[]>("/frameworks"),
  });
}

export function useFramework(id: string) {
  return useQuery({
    queryKey: ["frameworks", id],
    queryFn: () => api.get<Framework>(`/frameworks/${id}`),
    enabled: !!id,
  });
}

// Controls
export function useControls(orgId: string, params?: { status?: string; page?: number }) {
  const searchParams = new URLSearchParams();
  if (params?.status) searchParams.set("status", params.status);
  if (params?.page) searchParams.set("page", String(params.page));
  const qs = searchParams.toString();

  return useQuery({
    queryKey: ["controls", orgId, params],
    queryFn: () =>
      api.get<PaginatedResponse<Control>>(
        `/organizations/${orgId}/controls${qs ? `?${qs}` : ""}`
      ),
    enabled: !!orgId,
  });
}

export function useControl(orgId: string, controlId: string) {
  return useQuery({
    queryKey: ["controls", orgId, controlId],
    queryFn: () =>
      api.get<Control>(`/organizations/${orgId}/controls/${controlId}`),
    enabled: !!orgId && !!controlId,
  });
}

export function useControlStats(orgId: string) {
  return useQuery({
    queryKey: ["control-stats", orgId],
    queryFn: () =>
      api.get<ControlStats>(`/organizations/${orgId}/controls/stats`),
    enabled: !!orgId,
  });
}

export function useBulkApprove(orgId: string) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (data: { control_ids: string[]; status?: string }) =>
      api.post(`/organizations/${orgId}/controls/bulk-approve`, data),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["controls", orgId] });
      qc.invalidateQueries({ queryKey: ["control-stats", orgId] });
    },
  });
}

// Control Templates
export function useControlTemplates(params?: { domain?: string; page?: number }) {
  const searchParams = new URLSearchParams();
  if (params?.domain) searchParams.set("domain", params.domain);
  if (params?.page) searchParams.set("page", String(params.page));
  const qs = searchParams.toString();

  return useQuery({
    queryKey: ["control-templates", params],
    queryFn: () =>
      api.get<PaginatedResponse<ControlTemplate>>(
        `/control-templates${qs ? `?${qs}` : ""}`
      ),
  });
}

export function useControlTemplate(id: string) {
  return useQuery({
    queryKey: ["control-templates", id],
    queryFn: () => api.get<ControlTemplate>(`/control-templates/${id}`),
    enabled: !!id,
  });
}

// Evidence Templates
export function useEvidenceTemplates(params?: { page?: number }) {
  const searchParams = new URLSearchParams();
  if (params?.page) searchParams.set("page", String(params.page));
  const qs = searchParams.toString();

  return useQuery({
    queryKey: ["evidence-templates", params],
    queryFn: () =>
      api.get<PaginatedResponse<EvidenceTemplate>>(
        `/evidence-templates${qs ? `?${qs}` : ""}`
      ),
  });
}

// Evidence
export function useEvidence(orgId: string, params?: { control_id?: string; page?: number }) {
  const searchParams = new URLSearchParams();
  if (params?.control_id) searchParams.set("control_id", params.control_id);
  if (params?.page) searchParams.set("page", String(params.page));
  const qs = searchParams.toString();

  return useQuery({
    queryKey: ["evidence", orgId, params],
    queryFn: () =>
      api.get<PaginatedResponse<Evidence>>(
        `/organizations/${orgId}/evidence${qs ? `?${qs}` : ""}`
      ),
    enabled: !!orgId,
  });
}

// Agent Runs
export function useAgentRuns(orgId: string) {
  return useQuery({
    queryKey: ["agent-runs", orgId],
    queryFn: () =>
      api.get<PaginatedResponse<AgentRun>>(
        `/organizations/${orgId}/agents/runs`
      ),
    enabled: !!orgId,
  });
}

export function useAgentRun(orgId: string, runId: string) {
  return useQuery({
    queryKey: ["agent-runs", orgId, runId],
    queryFn: () =>
      api.get<AgentRun>(`/organizations/${orgId}/agents/runs/${runId}`),
    enabled: !!orgId && !!runId,
  });
}

export function useTriggerAgent(orgId: string) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (data: AgentRunTrigger) =>
      api.post<AgentRun>(
        `/organizations/${orgId}/agents/controls-generation/run`,
        data
      ),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["agent-runs", orgId] });
    },
  });
}

// Policies
export function usePolicies(orgId: string, params?: { status?: string; page?: number }) {
  const searchParams = new URLSearchParams();
  if (params?.status) searchParams.set("status", params.status);
  if (params?.page) searchParams.set("page", String(params.page));
  const qs = searchParams.toString();

  return useQuery({
    queryKey: ["policies", orgId, params],
    queryFn: () =>
      api.get<PaginatedResponse<Policy>>(
        `/organizations/${orgId}/policies${qs ? `?${qs}` : ""}`
      ),
    enabled: !!orgId,
  });
}

export function usePolicy(orgId: string, policyId: string) {
  return useQuery({
    queryKey: ["policies", orgId, policyId],
    queryFn: () =>
      api.get<Policy>(`/organizations/${orgId}/policies/${policyId}`),
    enabled: !!orgId && !!policyId,
  });
}

export function usePolicyStats(orgId: string) {
  return useQuery({
    queryKey: ["policy-stats", orgId],
    queryFn: () =>
      api.get<PolicyStats>(`/organizations/${orgId}/policies/stats`),
    enabled: !!orgId,
  });
}

export function useCreatePolicy(orgId: string) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (data: { title: string; content?: string; template_id?: string; status?: string }) =>
      api.post<Policy>(`/organizations/${orgId}/policies`, data),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["policies", orgId] });
      qc.invalidateQueries({ queryKey: ["policy-stats", orgId] });
    },
  });
}

export function useUpdatePolicy(orgId: string) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: ({ policyId, ...data }: { policyId: string; title?: string; content?: string; status?: string }) =>
      api.patch<Policy>(`/organizations/${orgId}/policies/${policyId}`, data),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["policies", orgId] });
      qc.invalidateQueries({ queryKey: ["policy-stats", orgId] });
    },
  });
}

export function usePolicyTemplates(params?: { category?: string; page?: number }) {
  const searchParams = new URLSearchParams();
  if (params?.category) searchParams.set("category", params.category);
  if (params?.page) searchParams.set("page", String(params.page));
  const qs = searchParams.toString();

  return useQuery({
    queryKey: ["policy-templates", params],
    queryFn: () =>
      api.get<PaginatedResponse<PolicyTemplate>>(
        `/policy-templates${qs ? `?${qs}` : ""}`
      ),
  });
}

export function useTriggerPolicyAgent(orgId: string) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (data: AgentRunTrigger) =>
      api.post<AgentRun>(
        `/organizations/${orgId}/agents/policy-generation/run`,
        data
      ),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["agent-runs", orgId] });
      qc.invalidateQueries({ queryKey: ["policies", orgId] });
      qc.invalidateQueries({ queryKey: ["policy-stats", orgId] });
    },
  });
}

// Organization
export function useOrganization(orgId: string) {
  return useQuery({
    queryKey: ["organizations", orgId],
    queryFn: () => api.get<Organization>(`/organizations/${orgId}`),
    enabled: !!orgId,
  });
}

// ===== Risk Register =====

export function useRisks(orgId: string, params?: { status?: string; risk_level?: string; category?: string; page?: number }) {
  const searchParams = new URLSearchParams();
  if (params?.status) searchParams.set("status", params.status);
  if (params?.risk_level) searchParams.set("risk_level", params.risk_level);
  if (params?.category) searchParams.set("category", params.category);
  if (params?.page) searchParams.set("page", String(params.page));
  const qs = searchParams.toString();

  return useQuery({
    queryKey: ["risks", orgId, params],
    queryFn: () =>
      api.get<PaginatedResponse<Risk>>(
        `/organizations/${orgId}/risks${qs ? `?${qs}` : ""}`
      ),
    enabled: !!orgId,
  });
}

export function useRisk(orgId: string, riskId: string) {
  return useQuery({
    queryKey: ["risks", orgId, riskId],
    queryFn: () => api.get<Risk>(`/organizations/${orgId}/risks/${riskId}`),
    enabled: !!orgId && !!riskId,
  });
}

export function useRiskStats(orgId: string) {
  return useQuery({
    queryKey: ["risk-stats", orgId],
    queryFn: () => api.get<RiskStats>(`/organizations/${orgId}/risks/stats`),
    enabled: !!orgId,
  });
}

export function useRiskMatrix(orgId: string) {
  return useQuery({
    queryKey: ["risk-matrix", orgId],
    queryFn: () => api.get<RiskMatrixResponse>(`/organizations/${orgId}/risks/matrix`),
    enabled: !!orgId,
  });
}

export function useCreateRisk(orgId: string) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (data: Partial<Risk>) =>
      api.post<Risk>(`/organizations/${orgId}/risks`, data),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["risks", orgId] });
      qc.invalidateQueries({ queryKey: ["risk-stats", orgId] });
      qc.invalidateQueries({ queryKey: ["risk-matrix", orgId] });
    },
  });
}

export function useUpdateRisk(orgId: string) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: ({ riskId, ...data }: { riskId: string } & Partial<Risk>) =>
      api.patch<Risk>(`/organizations/${orgId}/risks/${riskId}`, data),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["risks", orgId] });
      qc.invalidateQueries({ queryKey: ["risk-stats", orgId] });
      qc.invalidateQueries({ queryKey: ["risk-matrix", orgId] });
    },
  });
}

export function useDeleteRisk(orgId: string) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (riskId: string) =>
      api.delete(`/organizations/${orgId}/risks/${riskId}`),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["risks", orgId] });
      qc.invalidateQueries({ queryKey: ["risk-stats", orgId] });
      qc.invalidateQueries({ queryKey: ["risk-matrix", orgId] });
    },
  });
}

// ===== Integrations =====

export function useIntegrations(orgId: string, params?: { page?: number }) {
  const searchParams = new URLSearchParams();
  if (params?.page) searchParams.set("page", String(params.page));
  const qs = searchParams.toString();

  return useQuery({
    queryKey: ["integrations", orgId, params],
    queryFn: () =>
      api.get<PaginatedResponse<Integration>>(
        `/organizations/${orgId}/integrations${qs ? `?${qs}` : ""}`
      ),
    enabled: !!orgId,
  });
}

export function useIntegration(orgId: string, integrationId: string) {
  return useQuery({
    queryKey: ["integrations", orgId, integrationId],
    queryFn: () =>
      api.get<Integration>(`/organizations/${orgId}/integrations/${integrationId}`),
    enabled: !!orgId && !!integrationId,
  });
}

export function useProviders(orgId: string) {
  return useQuery({
    queryKey: ["providers", orgId],
    queryFn: () =>
      api.get<ProviderInfo[]>(`/organizations/${orgId}/integrations/providers`),
    enabled: !!orgId,
  });
}

export function useCreateIntegration(orgId: string) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (data: { provider: string; name: string; config?: Record<string, unknown> }) =>
      api.post<Integration>(`/organizations/${orgId}/integrations`, data),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["integrations", orgId] });
    },
  });
}

export function useTriggerCollection(orgId: string, integrationId: string) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (data: { collector_type: string; evidence_template_id?: string; control_id?: string }) =>
      api.post<CollectionJob>(
        `/organizations/${orgId}/integrations/${integrationId}/collect`,
        data
      ),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["collection-jobs", orgId, integrationId] });
      qc.invalidateQueries({ queryKey: ["evidence", orgId] });
    },
  });
}

export function useCollectionJobs(orgId: string, integrationId: string) {
  return useQuery({
    queryKey: ["collection-jobs", orgId, integrationId],
    queryFn: () =>
      api.get<PaginatedResponse<CollectionJob>>(
        `/organizations/${orgId}/integrations/${integrationId}/jobs`
      ),
    enabled: !!orgId && !!integrationId,
  });
}

// ===== Audits =====

export function useAudits(orgId: string, params?: { page?: number }) {
  const searchParams = new URLSearchParams();
  if (params?.page) searchParams.set("page", String(params.page));
  const qs = searchParams.toString();

  return useQuery({
    queryKey: ["audits", orgId, params],
    queryFn: () =>
      api.get<PaginatedResponse<Audit>>(
        `/organizations/${orgId}/audits${qs ? `?${qs}` : ""}`
      ),
    enabled: !!orgId,
  });
}

export function useAudit(orgId: string, auditId: string) {
  return useQuery({
    queryKey: ["audits", orgId, auditId],
    queryFn: () => api.get<Audit>(`/organizations/${orgId}/audits/${auditId}`),
    enabled: !!orgId && !!auditId,
  });
}

export function useReadinessScore(orgId: string) {
  return useQuery({
    queryKey: ["readiness", orgId],
    queryFn: () => api.get<ReadinessScore>(`/organizations/${orgId}/audits/readiness`),
    enabled: !!orgId,
  });
}

export function useCreateAudit(orgId: string) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (data: { title: string; framework_id?: string; audit_type?: string; auditor_firm?: string }) =>
      api.post<Audit>(`/organizations/${orgId}/audits`, data),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["audits", orgId] });
    },
  });
}

export function useAuditFindings(orgId: string, auditId: string) {
  return useQuery({
    queryKey: ["audit-findings", orgId, auditId],
    queryFn: () =>
      api.get<AuditFinding[]>(`/organizations/${orgId}/audits/${auditId}/findings`),
    enabled: !!orgId && !!auditId,
  });
}

export function useAuditTokens(orgId: string, auditId: string) {
  return useQuery({
    queryKey: ["audit-tokens", orgId, auditId],
    queryFn: () =>
      api.get<AuditorAccessToken[]>(`/organizations/${orgId}/audits/${auditId}/tokens`),
    enabled: !!orgId && !!auditId,
  });
}

export function useUpdateAudit(orgId: string) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: ({ auditId, ...data }: { auditId: string; title?: string; status?: string; auditor_firm?: string; lead_auditor_name?: string }) =>
      api.patch<Audit>(`/organizations/${orgId}/audits/${auditId}`, data),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["audits", orgId] });
    },
  });
}

export function useCreateFinding(orgId: string, auditId: string) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (data: { title: string; description?: string; severity?: string; control_id?: string }) =>
      api.post<AuditFinding>(`/organizations/${orgId}/audits/${auditId}/findings`, data),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["audit-findings", orgId, auditId] });
    },
  });
}

export function useCreateToken(orgId: string, auditId: string) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (data: { auditor_email: string; auditor_name?: string; expires_in_days?: number }) =>
      api.post<AuditorAccessToken>(`/organizations/${orgId}/audits/${auditId}/tokens`, data),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["audit-tokens", orgId, auditId] });
    },
  });
}

export function useRevokeToken(orgId: string, auditId: string) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (tokenId: string) =>
      api.delete(`/organizations/${orgId}/audits/${auditId}/tokens/${tokenId}`),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["audit-tokens", orgId, auditId] });
    },
  });
}

// ===== Onboarding =====

export function useStartOnboarding(orgId: string) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (data: OnboardingWizardInput) =>
      api.post<OnboardingSession>(`/organizations/${orgId}/onboarding/start`, data),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["onboarding", orgId] });
    },
  });
}

export function useOnboardingStatus(orgId: string, sessionId: string) {
  return useQuery({
    queryKey: ["onboarding", orgId, sessionId],
    queryFn: () =>
      api.get<OnboardingSession>(
        `/organizations/${orgId}/onboarding/status/${sessionId}`
      ),
    enabled: !!orgId && !!sessionId,
    refetchInterval: (query) => {
      const data = query.state.data;
      if (data && (data.status === "completed" || data.status === "failed")) return false;
      return 3000;
    },
  });
}

export function useLatestOnboarding(orgId: string) {
  return useQuery({
    queryKey: ["onboarding-latest", orgId],
    queryFn: () =>
      api.get<OnboardingSession | null>(`/organizations/${orgId}/onboarding/latest`),
    enabled: !!orgId,
  });
}

// ===== Update Organization =====

export function useUpdateOrganization(orgId: string) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (data: Partial<Organization>) =>
      api.patch<Organization>(`/organizations/${orgId}`, data),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["organizations", orgId] });
    },
  });
}

// ===== Incidents =====

export function useIncidents(orgId: string, params?: { status?: string; severity?: string; page?: number }) {
  const searchParams = new URLSearchParams();
  if (params?.status) searchParams.set("status", params.status);
  if (params?.severity) searchParams.set("severity", params.severity);
  if (params?.page) searchParams.set("page", String(params.page));
  const qs = searchParams.toString();

  return useQuery({
    queryKey: ["incidents", orgId, params],
    queryFn: () =>
      api.get<PaginatedResponse<Incident>>(
        `/organizations/${orgId}/incidents${qs ? `?${qs}` : ""}`
      ),
    enabled: !!orgId,
  });
}

export function useIncident(orgId: string, incidentId: string) {
  return useQuery({
    queryKey: ["incidents", orgId, incidentId],
    queryFn: () => api.get<Incident>(`/organizations/${orgId}/incidents/${incidentId}`),
    enabled: !!orgId && !!incidentId,
  });
}

export function useIncidentStats(orgId: string) {
  return useQuery({
    queryKey: ["incident-stats", orgId],
    queryFn: () => api.get<IncidentStats>(`/organizations/${orgId}/incidents/stats`),
    enabled: !!orgId,
  });
}

export function useCreateIncident(orgId: string) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (data: Partial<Incident>) =>
      api.post<Incident>(`/organizations/${orgId}/incidents`, data),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["incidents", orgId] });
      qc.invalidateQueries({ queryKey: ["incident-stats", orgId] });
    },
  });
}

export function useUpdateIncident(orgId: string) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: ({ incidentId, ...data }: { incidentId: string } & Partial<Incident>) =>
      api.patch<Incident>(`/organizations/${orgId}/incidents/${incidentId}`, data),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["incidents", orgId] });
      qc.invalidateQueries({ queryKey: ["incident-stats", orgId] });
    },
  });
}

export function useDeleteIncident(orgId: string) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (incidentId: string) =>
      api.delete(`/organizations/${orgId}/incidents/${incidentId}`),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["incidents", orgId] });
      qc.invalidateQueries({ queryKey: ["incident-stats", orgId] });
    },
  });
}

export function useIncidentTimeline(orgId: string, incidentId: string) {
  return useQuery({
    queryKey: ["incident-timeline", orgId, incidentId],
    queryFn: () =>
      api.get<IncidentTimelineEvent[]>(`/organizations/${orgId}/incidents/${incidentId}/timeline`),
    enabled: !!orgId && !!incidentId,
  });
}

export function useAddTimelineEvent(orgId: string, incidentId: string) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (data: { event_type: string; description: string }) =>
      api.post<IncidentTimelineEvent>(`/organizations/${orgId}/incidents/${incidentId}/timeline`, data),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["incident-timeline", orgId, incidentId] });
    },
  });
}

// ===== Vendors =====

export function useVendors(orgId: string, params?: { risk_tier?: string; status?: string; page?: number }) {
  const searchParams = new URLSearchParams();
  if (params?.risk_tier) searchParams.set("risk_tier", params.risk_tier);
  if (params?.status) searchParams.set("status", params.status);
  if (params?.page) searchParams.set("page", String(params.page));
  const qs = searchParams.toString();

  return useQuery({
    queryKey: ["vendors", orgId, params],
    queryFn: () =>
      api.get<PaginatedResponse<Vendor>>(
        `/organizations/${orgId}/vendors${qs ? `?${qs}` : ""}`
      ),
    enabled: !!orgId,
  });
}

export function useVendor(orgId: string, vendorId: string) {
  return useQuery({
    queryKey: ["vendors", orgId, vendorId],
    queryFn: () => api.get<Vendor>(`/organizations/${orgId}/vendors/${vendorId}`),
    enabled: !!orgId && !!vendorId,
  });
}

export function useVendorStats(orgId: string) {
  return useQuery({
    queryKey: ["vendor-stats", orgId],
    queryFn: () => api.get<VendorStats>(`/organizations/${orgId}/vendors/stats`),
    enabled: !!orgId,
  });
}

export function useCreateVendor(orgId: string) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (data: Partial<Vendor>) =>
      api.post<Vendor>(`/organizations/${orgId}/vendors`, data),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["vendors", orgId] });
      qc.invalidateQueries({ queryKey: ["vendor-stats", orgId] });
    },
  });
}

export function useUpdateVendor(orgId: string) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: ({ vendorId, ...data }: { vendorId: string } & Partial<Vendor>) =>
      api.patch<Vendor>(`/organizations/${orgId}/vendors/${vendorId}`, data),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["vendors", orgId] });
      qc.invalidateQueries({ queryKey: ["vendor-stats", orgId] });
    },
  });
}

export function useDeleteVendor(orgId: string) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (vendorId: string) =>
      api.delete(`/organizations/${orgId}/vendors/${vendorId}`),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["vendors", orgId] });
      qc.invalidateQueries({ queryKey: ["vendor-stats", orgId] });
    },
  });
}

export function useVendorAssessments(orgId: string, vendorId: string) {
  return useQuery({
    queryKey: ["vendor-assessments", orgId, vendorId],
    queryFn: () =>
      api.get<VendorAssessment[]>(`/organizations/${orgId}/vendors/${vendorId}/assessments`),
    enabled: !!orgId && !!vendorId,
  });
}

export function useCreateVendorAssessment(orgId: string, vendorId: string) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (data: { score: number; risk_tier_assigned: string; notes?: string }) =>
      api.post<VendorAssessment>(`/organizations/${orgId}/vendors/${vendorId}/assessments`, data),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["vendor-assessments", orgId, vendorId] });
      qc.invalidateQueries({ queryKey: ["vendors", orgId] });
    },
  });
}

// ===== Training =====

export function useTrainingCourses(orgId: string, params?: { page?: number }) {
  const searchParams = new URLSearchParams();
  if (params?.page) searchParams.set("page", String(params.page));
  const qs = searchParams.toString();

  return useQuery({
    queryKey: ["training-courses", orgId, params],
    queryFn: () =>
      api.get<PaginatedResponse<TrainingCourse>>(
        `/organizations/${orgId}/training/courses${qs ? `?${qs}` : ""}`
      ),
    enabled: !!orgId,
  });
}

export function useTrainingCourse(orgId: string, courseId: string) {
  return useQuery({
    queryKey: ["training-courses", orgId, courseId],
    queryFn: () =>
      api.get<TrainingCourse>(`/organizations/${orgId}/training/courses/${courseId}`),
    enabled: !!orgId && !!courseId,
  });
}

export function useCreateTrainingCourse(orgId: string) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (data: Partial<TrainingCourse>) =>
      api.post<TrainingCourse>(`/organizations/${orgId}/training/courses`, data),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["training-courses", orgId] });
      qc.invalidateQueries({ queryKey: ["training-stats", orgId] });
    },
  });
}

export function useUpdateTrainingCourse(orgId: string) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: ({ courseId, ...data }: { courseId: string } & Partial<TrainingCourse>) =>
      api.patch<TrainingCourse>(`/organizations/${orgId}/training/courses/${courseId}`, data),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["training-courses", orgId] });
      qc.invalidateQueries({ queryKey: ["training-stats", orgId] });
    },
  });
}

export function useDeleteTrainingCourse(orgId: string) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (courseId: string) =>
      api.delete(`/organizations/${orgId}/training/courses/${courseId}`),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["training-courses", orgId] });
      qc.invalidateQueries({ queryKey: ["training-stats", orgId] });
    },
  });
}

export function useTrainingAssignments(orgId: string, params?: { status?: string; course_id?: string; page?: number }) {
  const searchParams = new URLSearchParams();
  if (params?.status) searchParams.set("status", params.status);
  if (params?.course_id) searchParams.set("course_id", params.course_id);
  if (params?.page) searchParams.set("page", String(params.page));
  const qs = searchParams.toString();

  return useQuery({
    queryKey: ["training-assignments", orgId, params],
    queryFn: () =>
      api.get<PaginatedResponse<TrainingAssignment>>(
        `/organizations/${orgId}/training/assignments${qs ? `?${qs}` : ""}`
      ),
    enabled: !!orgId,
  });
}

export function useTrainingStats(orgId: string) {
  return useQuery({
    queryKey: ["training-stats", orgId],
    queryFn: () => api.get<TrainingStats>(`/organizations/${orgId}/training/stats`),
    enabled: !!orgId,
  });
}

// ===== Access Reviews =====

export function useAccessReviewCampaigns(orgId: string, params?: { status?: string; page?: number }) {
  const searchParams = new URLSearchParams();
  if (params?.status) searchParams.set("status", params.status);
  if (params?.page) searchParams.set("page", String(params.page));
  const qs = searchParams.toString();

  return useQuery({
    queryKey: ["access-review-campaigns", orgId, params],
    queryFn: () =>
      api.get<PaginatedResponse<AccessReviewCampaign>>(
        `/organizations/${orgId}/access-reviews${qs ? `?${qs}` : ""}`
      ),
    enabled: !!orgId,
  });
}

export function useAccessReviewCampaign(orgId: string, campaignId: string) {
  return useQuery({
    queryKey: ["access-review-campaigns", orgId, campaignId],
    queryFn: () =>
      api.get<AccessReviewCampaign>(`/organizations/${orgId}/access-reviews/${campaignId}`),
    enabled: !!orgId && !!campaignId,
  });
}

export function useAccessReviewStats(orgId: string) {
  return useQuery({
    queryKey: ["access-review-stats", orgId],
    queryFn: () => api.get<AccessReviewStats>(`/organizations/${orgId}/access-reviews/stats`),
    enabled: !!orgId,
  });
}

export function useCreateAccessReviewCampaign(orgId: string) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (data: { title: string; description?: string; due_date?: string }) =>
      api.post<AccessReviewCampaign>(`/organizations/${orgId}/access-reviews`, data),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["access-review-campaigns", orgId] });
      qc.invalidateQueries({ queryKey: ["access-review-stats", orgId] });
    },
  });
}

export function useUpdateAccessReviewCampaign(orgId: string) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: ({ campaignId, ...data }: { campaignId: string } & Partial<AccessReviewCampaign>) =>
      api.patch<AccessReviewCampaign>(`/organizations/${orgId}/access-reviews/${campaignId}`, data),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["access-review-campaigns", orgId] });
      qc.invalidateQueries({ queryKey: ["access-review-stats", orgId] });
    },
  });
}

export function useAccessReviewEntries(orgId: string, campaignId: string) {
  return useQuery({
    queryKey: ["access-review-entries", orgId, campaignId],
    queryFn: () =>
      api.get<AccessReviewEntry[]>(`/organizations/${orgId}/access-reviews/${campaignId}/entries`),
    enabled: !!orgId && !!campaignId,
  });
}

export function useCreateAccessReviewEntry(orgId: string, campaignId: string) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (data: { user_name: string; user_email: string; system_name: string; resource: string; current_access: string }) =>
      api.post<AccessReviewEntry>(`/organizations/${orgId}/access-reviews/${campaignId}/entries`, data),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["access-review-entries", orgId, campaignId] });
      qc.invalidateQueries({ queryKey: ["access-review-campaigns", orgId] });
    },
  });
}

export function useUpdateAccessReviewEntry(orgId: string, campaignId: string) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: ({ entryId, ...data }: { entryId: string; decision?: string; notes?: string }) =>
      api.patch<AccessReviewEntry>(`/organizations/${orgId}/access-reviews/${campaignId}/entries/${entryId}`, data),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["access-review-entries", orgId, campaignId] });
      qc.invalidateQueries({ queryKey: ["access-review-campaigns", orgId] });
    },
  });
}

// ===== Monitoring =====

export function useMonitorRules(orgId: string, params?: { check_type?: string; is_active?: string; page?: number }) {
  const searchParams = new URLSearchParams();
  if (params?.check_type) searchParams.set("check_type", params.check_type);
  if (params?.is_active) searchParams.set("is_active", params.is_active);
  if (params?.page) searchParams.set("page", String(params.page));
  const qs = searchParams.toString();

  return useQuery({
    queryKey: ["monitor-rules", orgId, params],
    queryFn: () =>
      api.get<PaginatedResponse<MonitorRule>>(
        `/organizations/${orgId}/monitoring/rules${qs ? `?${qs}` : ""}`
      ),
    enabled: !!orgId,
  });
}

export function useMonitorRule(orgId: string, ruleId: string) {
  return useQuery({
    queryKey: ["monitor-rules", orgId, ruleId],
    queryFn: () =>
      api.get<MonitorRule>(`/organizations/${orgId}/monitoring/rules/${ruleId}`),
    enabled: !!orgId && !!ruleId,
  });
}

export function useCreateMonitorRule(orgId: string) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (data: Partial<MonitorRule>) =>
      api.post<MonitorRule>(`/organizations/${orgId}/monitoring/rules`, data),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["monitor-rules", orgId] });
      qc.invalidateQueries({ queryKey: ["monitoring-stats", orgId] });
    },
  });
}

export function useUpdateMonitorRule(orgId: string) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: ({ ruleId, ...data }: { ruleId: string } & Partial<MonitorRule>) =>
      api.patch<MonitorRule>(`/organizations/${orgId}/monitoring/rules/${ruleId}`, data),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["monitor-rules", orgId] });
      qc.invalidateQueries({ queryKey: ["monitoring-stats", orgId] });
    },
  });
}

export function useDeleteMonitorRule(orgId: string) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (ruleId: string) =>
      api.delete(`/organizations/${orgId}/monitoring/rules/${ruleId}`),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["monitor-rules", orgId] });
      qc.invalidateQueries({ queryKey: ["monitoring-stats", orgId] });
    },
  });
}

export function useRunMonitorRule(orgId: string) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (ruleId: string) =>
      api.post<MonitorAlert[]>(`/organizations/${orgId}/monitoring/rules/${ruleId}/run`),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["monitor-rules", orgId] });
      qc.invalidateQueries({ queryKey: ["monitor-alerts", orgId] });
    },
  });
}

export function useMonitorAlerts(orgId: string, params?: { status?: string; severity?: string; rule_id?: string; page?: number }) {
  const searchParams = new URLSearchParams();
  if (params?.status) searchParams.set("status", params.status);
  if (params?.severity) searchParams.set("severity", params.severity);
  if (params?.rule_id) searchParams.set("rule_id", params.rule_id);
  if (params?.page) searchParams.set("page", String(params.page));
  const qs = searchParams.toString();

  return useQuery({
    queryKey: ["monitor-alerts", orgId, params],
    queryFn: () =>
      api.get<PaginatedResponse<MonitorAlert>>(
        `/organizations/${orgId}/monitoring/alerts${qs ? `?${qs}` : ""}`
      ),
    enabled: !!orgId,
  });
}

export function useUpdateMonitorAlert(orgId: string) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: ({ alertId, ...data }: { alertId: string; status?: string }) =>
      api.patch<MonitorAlert>(`/organizations/${orgId}/monitoring/alerts/${alertId}`, data),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["monitor-alerts", orgId] });
      qc.invalidateQueries({ queryKey: ["monitoring-stats", orgId] });
    },
  });
}

export function useMonitoringStats(orgId: string) {
  return useQuery({
    queryKey: ["monitoring-stats", orgId],
    queryFn: () => api.get<MonitoringStats>(`/organizations/${orgId}/monitoring/stats`),
    enabled: !!orgId,
  });
}

// ===== Questionnaires =====

export function useQuestionnaires(orgId: string, params?: { status?: string; page?: number }) {
  const searchParams = new URLSearchParams();
  if (params?.status) searchParams.set("status", params.status);
  if (params?.page) searchParams.set("page", String(params.page));
  const qs = searchParams.toString();

  return useQuery({
    queryKey: ["questionnaires", orgId, params],
    queryFn: () =>
      api.get<PaginatedResponse<Questionnaire>>(
        `/organizations/${orgId}/questionnaires${qs ? `?${qs}` : ""}`
      ),
    enabled: !!orgId,
  });
}

export function useQuestionnaire(orgId: string, questionnaireId: string) {
  return useQuery({
    queryKey: ["questionnaires", orgId, questionnaireId],
    queryFn: () =>
      api.get<Questionnaire>(`/organizations/${orgId}/questionnaires/${questionnaireId}`),
    enabled: !!orgId && !!questionnaireId,
  });
}

export function useQuestionnaireStats(orgId: string) {
  return useQuery({
    queryKey: ["questionnaire-stats", orgId],
    queryFn: () => api.get<QuestionnaireStats>(`/organizations/${orgId}/questionnaires/stats`),
    enabled: !!orgId,
  });
}

export function useCreateQuestionnaire(orgId: string) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (data: Partial<Questionnaire>) =>
      api.post<Questionnaire>(`/organizations/${orgId}/questionnaires`, data),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["questionnaires", orgId] });
      qc.invalidateQueries({ queryKey: ["questionnaire-stats", orgId] });
    },
  });
}

export function useUpdateQuestionnaire(orgId: string) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: ({ questionnaireId, ...data }: { questionnaireId: string } & Partial<Questionnaire>) =>
      api.patch<Questionnaire>(`/organizations/${orgId}/questionnaires/${questionnaireId}`, data),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["questionnaires", orgId] });
      qc.invalidateQueries({ queryKey: ["questionnaire-stats", orgId] });
    },
  });
}

export function useDeleteQuestionnaire(orgId: string) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (questionnaireId: string) =>
      api.delete(`/organizations/${orgId}/questionnaires/${questionnaireId}`),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["questionnaires", orgId] });
      qc.invalidateQueries({ queryKey: ["questionnaire-stats", orgId] });
    },
  });
}

export function useAutoFillQuestionnaire(orgId: string) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (questionnaireId: string) =>
      api.post<number>(`/organizations/${orgId}/questionnaires/${questionnaireId}/auto-fill`),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["questionnaires", orgId] });
    },
  });
}

// ===== Trust Center =====

export function useTrustCenterConfig(orgId: string) {
  return useQuery({
    queryKey: ["trust-center-config", orgId],
    queryFn: () => api.get<TrustCenterConfig>(`/organizations/${orgId}/trust-center/config`),
    enabled: !!orgId,
  });
}

export function useUpdateTrustCenterConfig(orgId: string) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (data: Partial<TrustCenterConfig>) =>
      api.patch<TrustCenterConfig>(`/organizations/${orgId}/trust-center/config`, data),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["trust-center-config", orgId] });
    },
  });
}

export function useTrustCenterDocuments(orgId: string) {
  return useQuery({
    queryKey: ["trust-center-documents", orgId],
    queryFn: () => api.get<TrustCenterDocument[]>(`/organizations/${orgId}/trust-center/documents`),
    enabled: !!orgId,
  });
}

export function useCreateTrustCenterDocument(orgId: string) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (data: Partial<TrustCenterDocument>) =>
      api.post<TrustCenterDocument>(`/organizations/${orgId}/trust-center/documents`, data),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["trust-center-documents", orgId] });
    },
  });
}

// ===== Reports =====

export function useReports(orgId: string, params?: { report_type?: string; status?: string; page?: number }) {
  const searchParams = new URLSearchParams();
  if (params?.report_type) searchParams.set("report_type", params.report_type);
  if (params?.status) searchParams.set("status", params.status);
  if (params?.page) searchParams.set("page", String(params.page));
  const qs = searchParams.toString();

  return useQuery({
    queryKey: ["reports", orgId, params],
    queryFn: () =>
      api.get<PaginatedResponse<Report>>(
        `/organizations/${orgId}/reports${qs ? `?${qs}` : ""}`
      ),
    enabled: !!orgId,
  });
}

export function useCreateReport(orgId: string) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (data: { title: string; report_type: string; format: string }) =>
      api.post<Report>(`/organizations/${orgId}/reports`, data),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["reports", orgId] });
      qc.invalidateQueries({ queryKey: ["report-stats", orgId] });
    },
  });
}

export function useReportStats(orgId: string) {
  return useQuery({
    queryKey: ["report-stats", orgId],
    queryFn: () => api.get<ReportStats>(`/organizations/${orgId}/reports/stats`),
    enabled: !!orgId,
  });
}

// ===== Policy Workflow =====

export function useSubmitPolicy(orgId: string) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (policyId: string) =>
      api.post(`/organizations/${orgId}/policies/${policyId}/submit-for-review`),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["policies", orgId] });
      qc.invalidateQueries({ queryKey: ["policy-stats", orgId] });
    },
  });
}

export function useApprovePolicy(orgId: string) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (policyId: string) =>
      api.post(`/organizations/${orgId}/policies/${policyId}/approve`),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["policies", orgId] });
      qc.invalidateQueries({ queryKey: ["policy-stats", orgId] });
    },
  });
}

export function usePublishPolicy(orgId: string) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (policyId: string) =>
      api.post(`/organizations/${orgId}/policies/${policyId}/publish`),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["policies", orgId] });
      qc.invalidateQueries({ queryKey: ["policy-stats", orgId] });
    },
  });
}

// ===== Agent Trigger Hooks (New Agents) =====

export function useTriggerEvidenceAgent(orgId: string) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (data: AgentRunTrigger) =>
      api.post<AgentRun>(
        `/organizations/${orgId}/agents/evidence-generation/run`,
        data
      ),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["agent-runs", orgId] });
      qc.invalidateQueries({ queryKey: ["evidence", orgId] });
    },
  });
}

export function useTriggerRiskAssessmentAgent(orgId: string) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (data: AgentRunTriggerGeneric) =>
      api.post<AgentRun>(
        `/organizations/${orgId}/agents/risk-assessment/run`,
        data
      ),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["agent-runs", orgId] });
      qc.invalidateQueries({ queryKey: ["risks", orgId] });
    },
  });
}

export function useTriggerRemediationAgent(orgId: string) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (data: AgentRunTriggerGeneric) =>
      api.post<AgentRun>(
        `/organizations/${orgId}/agents/remediation/run`,
        data
      ),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["agent-runs", orgId] });
      qc.invalidateQueries({ queryKey: ["controls", orgId] });
    },
  });
}

export function useTriggerAuditPrepAgent(orgId: string) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (data: AgentRunTriggerGeneric) =>
      api.post<AgentRun>(
        `/organizations/${orgId}/agents/audit-preparation/run`,
        data
      ),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["agent-runs", orgId] });
      qc.invalidateQueries({ queryKey: ["audits", orgId] });
    },
  });
}

export function useTriggerVendorRiskAgent(orgId: string) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (data: AgentRunTriggerGeneric) =>
      api.post<AgentRun>(
        `/organizations/${orgId}/agents/vendor-risk-assessment/run`,
        data
      ),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["agent-runs", orgId] });
      qc.invalidateQueries({ queryKey: ["vendors", orgId] });
    },
  });
}

export function useTriggerPentestAgent(orgId: string) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (data: AgentRunTriggerGeneric) =>
      api.post<AgentRun>(
        `/organizations/${orgId}/agents/pentest-orchestrator/run`,
        data
      ),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["agent-runs", orgId] });
    },
  });
}

export function useTriggerMonitoringDaemonAgent(orgId: string) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (data: AgentRunTriggerGeneric) =>
      api.post<AgentRun>(
        `/organizations/${orgId}/agents/monitoring-daemon/run`,
        data
      ),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["agent-runs", orgId] });
      qc.invalidateQueries({ queryKey: ["monitor-rules", orgId] });
      qc.invalidateQueries({ queryKey: ["monitor-alerts", orgId] });
    },
  });
}

// ===== Framework Builder =====

export function useCreateFramework() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (data: FrameworkCreate) =>
      api.post<Framework>(`/frameworks`, data),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["frameworks"] });
    },
  });
}

export function useUpdateFramework() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: ({ id, ...data }: { id: string } & Partial<FrameworkCreate>) =>
      api.patch<Framework>(`/frameworks/${id}`, data),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["frameworks"] });
    },
  });
}

export function useDeleteFramework() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (id: string) => api.delete(`/frameworks/${id}`),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["frameworks"] });
    },
  });
}

export function useAddFrameworkDomain() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: ({ frameworkId, ...data }: { frameworkId: string } & DomainCreate) =>
      api.post(`/frameworks/${frameworkId}/domains`, data),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["frameworks"] });
    },
  });
}

export function useAddDomainRequirement() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: ({
      frameworkId,
      domainId,
      ...data
    }: { frameworkId: string; domainId: string } & RequirementCreate) =>
      api.post(`/frameworks/${frameworkId}/domains/${domainId}/requirements`, data),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["frameworks"] });
    },
  });
}

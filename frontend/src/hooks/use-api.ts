"use client";

import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import api from "@/lib/api";
import type {
  Framework,
  Control,
  ControlStats,
  ControlTemplate,
  EvidenceTemplate,
  Evidence,
  AgentRun,
  AgentRunTrigger,
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

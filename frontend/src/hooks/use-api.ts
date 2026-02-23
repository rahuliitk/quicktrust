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

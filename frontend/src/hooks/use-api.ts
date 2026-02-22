"use client";

import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import api from "@/lib/api";
import type {
  Framework,
  Control,
  ControlStats,
  ControlTemplate,
  EvidenceTemplate,
  AgentRun,
  AgentRunTrigger,
  Organization,
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

// Organization
export function useOrganization(orgId: string) {
  return useQuery({
    queryKey: ["organizations", orgId],
    queryFn: () => api.get<Organization>(`/organizations/${orgId}`),
    enabled: !!orgId,
  });
}

"use client";

import { useState } from "react";
import Link from "next/link";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Skeleton } from "@/components/ui/skeleton";
import { Progress } from "@/components/ui/progress";
import {
  useFrameworks,
  usePolicies,
  useTriggerPolicyAgent,
} from "@/hooks/use-api";
import { useAgentStatus } from "@/hooks/use-agent-status";
import type { AgentRun } from "@/lib/types";
import { Bot, CheckCircle, Loader2, Play, XCircle, FileText } from "lucide-react";
import { useOrgId } from "@/hooks/use-org-id";

export default function AgentPolicyGenerationPage() {
  const orgId = useOrgId();
  const { data: frameworks, isLoading: fwLoading } = useFrameworks();
  const [selectedFrameworkId, setSelectedFrameworkId] = useState<string>("");
  const [currentRunId, setCurrentRunId] = useState<string | null>(null);
  const [companyContext, setCompanyContext] = useState({
    name: "My Company",
    industry: "Technology",
    company_size: "50-200",
    cloud_providers: ["AWS"],
    tech_stack: ["React", "Node.js", "PostgreSQL"],
  });

  const triggerAgent = useTriggerPolicyAgent(orgId);
  const { run, polling, elapsed, isComplete, isFailed } = useAgentStatus(
    orgId,
    currentRunId
  );

  const { data: policiesData } = usePolicies(orgId, { status: "draft" });
  const draftPolicies = policiesData?.items || [];

  function handleTrigger() {
    if (!selectedFrameworkId) return;
    triggerAgent.mutate(
      {
        framework_id: selectedFrameworkId,
        company_context: companyContext,
      },
      {
        onSuccess: (data: AgentRun) => {
          setCurrentRunId(data.id);
        },
      }
    );
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold">Policy Generation Agent</h1>
        <p className="text-muted-foreground">
          AI-powered policy document generation from templates and company context
        </p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Generate Policies</CardTitle>
          <CardDescription>
            Select a framework and provide company context to generate tailored policy documents.
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div>
            <label className="text-sm font-medium">Framework</label>
            {fwLoading ? (
              <Skeleton className="mt-1 h-10 w-full" />
            ) : (
              <select
                className="mt-1 w-full rounded-md border bg-background p-2 text-sm"
                value={selectedFrameworkId}
                onChange={(e) => setSelectedFrameworkId(e.target.value)}
              >
                <option value="">Select a framework...</option>
                {frameworks?.map((fw) => (
                  <option key={fw.id} value={fw.id}>
                    {fw.name} (v{fw.version})
                  </option>
                ))}
              </select>
            )}
          </div>

          <div className="grid gap-4 md:grid-cols-2">
            <div>
              <label className="text-sm font-medium">Company Name</label>
              <input
                className="mt-1 w-full rounded-md border bg-background p-2 text-sm"
                value={companyContext.name}
                onChange={(e) =>
                  setCompanyContext({ ...companyContext, name: e.target.value })
                }
              />
            </div>
            <div>
              <label className="text-sm font-medium">Industry</label>
              <input
                className="mt-1 w-full rounded-md border bg-background p-2 text-sm"
                value={companyContext.industry}
                onChange={(e) =>
                  setCompanyContext({ ...companyContext, industry: e.target.value })
                }
              />
            </div>
            <div>
              <label className="text-sm font-medium">Company Size</label>
              <input
                className="mt-1 w-full rounded-md border bg-background p-2 text-sm"
                value={companyContext.company_size}
                onChange={(e) =>
                  setCompanyContext({
                    ...companyContext,
                    company_size: e.target.value,
                  })
                }
              />
            </div>
            <div>
              <label className="text-sm font-medium">Cloud Providers</label>
              <input
                className="mt-1 w-full rounded-md border bg-background p-2 text-sm"
                value={companyContext.cloud_providers.join(", ")}
                onChange={(e) =>
                  setCompanyContext({
                    ...companyContext,
                    cloud_providers: e.target.value.split(",").map((s) => s.trim()),
                  })
                }
              />
            </div>
          </div>

          <Button
            onClick={handleTrigger}
            disabled={!selectedFrameworkId || triggerAgent.isPending || polling}
          >
            {triggerAgent.isPending ? (
              <Loader2 className="mr-2 h-4 w-4 animate-spin" />
            ) : (
              <Play className="mr-2 h-4 w-4" />
            )}
            Generate Policies
          </Button>
        </CardContent>
      </Card>

      {currentRunId && run && (
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Bot className="h-5 w-5" />
              Agent Run Status
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="flex items-center gap-4">
              <Badge
                variant={
                  run.status === "completed"
                    ? "success"
                    : run.status === "failed"
                    ? "destructive"
                    : "secondary"
                }
              >
                {run.status}
              </Badge>
              {polling && (
                <div className="flex items-center gap-2 text-sm text-muted-foreground">
                  <Loader2 className="h-3 w-3 animate-spin" />
                  Running... ({elapsed}s)
                </div>
              )}
              {isComplete && (
                <div className="flex items-center gap-2 text-sm text-green-600">
                  <CheckCircle className="h-3 w-3" />
                  Completed
                  {run.output_data &&
                    ` — ${(run.output_data as Record<string, unknown>).policies_count || 0} policies generated`}
                </div>
              )}
              {isFailed && (
                <div className="flex items-center gap-2 text-sm text-red-600">
                  <XCircle className="h-3 w-3" />
                  {run.error_message || "Unknown error"}
                </div>
              )}
            </div>
            {polling && <Progress value={undefined} className="mt-3" />}
          </CardContent>
        </Card>
      )}

      {isComplete && draftPolicies.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle>Generated Policies</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-2">
              {draftPolicies.map((policy) => (
                <Link
                  key={policy.id}
                  href={`/policies/${policy.id}`}
                  className="flex items-center gap-3 rounded-lg border p-3 transition-colors hover:bg-accent/50"
                >
                  <FileText className="h-5 w-5 text-muted-foreground" />
                  <div className="flex-1">
                    <div className="font-medium text-sm">{policy.title}</div>
                    <div className="text-xs text-muted-foreground">
                      Version {policy.version} &middot; {policy.status}
                    </div>
                  </div>
                  <Badge variant="secondary">{policy.status}</Badge>
                </Link>
              ))}
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
}

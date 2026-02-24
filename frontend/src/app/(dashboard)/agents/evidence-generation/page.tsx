"use client";

import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Progress } from "@/components/ui/progress";
import { Skeleton } from "@/components/ui/skeleton";
import { useFrameworks, useTriggerEvidenceAgent } from "@/hooks/use-api";
import { useAgentStatus } from "@/hooks/use-agent-status";
import type { AgentRun } from "@/lib/types";
import { Bot, CheckCircle, Loader2, Play, XCircle } from "lucide-react";
import { useOrgId } from "@/hooks/use-org-id";
import Link from "next/link";

export default function EvidenceGenerationPage() {
  const orgId = useOrgId();
  const { data: frameworks, isLoading: fwLoading } = useFrameworks();
  const [selectedFrameworkId, setSelectedFrameworkId] = useState<string>("");
  const [currentRunId, setCurrentRunId] = useState<string | null>(null);

  const triggerAgent = useTriggerEvidenceAgent(orgId);
  const { run, polling, elapsed, isComplete, isFailed } = useAgentStatus(orgId, currentRunId);

  function handleTrigger() {
    if (!selectedFrameworkId) return;
    triggerAgent.mutate(
      { framework_id: selectedFrameworkId, company_context: {} },
      { onSuccess: (data: AgentRun) => setCurrentRunId(data.id) }
    );
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold">Evidence Generation Agent</h1>
        <p className="text-muted-foreground">AI-powered evidence generation for compliance controls</p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Generate Evidence</CardTitle>
          <CardDescription>Select a framework to generate evidence artifacts for mapped controls.</CardDescription>
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
          <Button onClick={handleTrigger} disabled={!selectedFrameworkId || triggerAgent.isPending || polling}>
            {triggerAgent.isPending ? <Loader2 className="mr-2 h-4 w-4 animate-spin" /> : <Play className="mr-2 h-4 w-4" />}
            Generate Evidence
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
              <Badge variant={run.status === "completed" ? "success" : run.status === "failed" ? "destructive" : "secondary"}>
                {run.status}
              </Badge>
              {polling && (
                <div className="flex items-center gap-2 text-sm text-muted-foreground">
                  <Loader2 className="h-3 w-3 animate-spin" />Running... ({elapsed}s)
                </div>
              )}
              {isComplete && (
                <div className="flex items-center gap-2 text-sm text-green-600">
                  <CheckCircle className="h-3 w-3" />Completed
                  {run.output_data && ` — ${(run.output_data as Record<string, unknown>).evidence_count || 0} evidence items generated`}
                </div>
              )}
              {isFailed && (
                <div className="flex items-center gap-2 text-sm text-red-600">
                  <XCircle className="h-3 w-3" />{run.error_message || "Unknown error"}
                </div>
              )}
            </div>
            {polling && <Progress value={undefined} className="mt-3" />}
            {isComplete && (
              <div className="mt-4">
                <Link href="/evidence">
                  <Button variant="outline">View Evidence Library</Button>
                </Link>
              </div>
            )}
          </CardContent>
        </Card>
      )}
    </div>
  );
}

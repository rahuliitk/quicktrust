"use client";

import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Progress } from "@/components/ui/progress";
import { useTriggerRemediationAgent } from "@/hooks/use-api";
import { useAgentStatus } from "@/hooks/use-agent-status";
import type { AgentRun } from "@/lib/types";
import { Bot, CheckCircle, Loader2, Play, XCircle } from "lucide-react";
import { useOrgId } from "@/hooks/use-org-id";
import Link from "next/link";

export default function RemediationPage() {
  const orgId = useOrgId();
  const [currentRunId, setCurrentRunId] = useState<string | null>(null);

  const triggerAgent = useTriggerRemediationAgent(orgId);
  const { run, polling, elapsed, isComplete, isFailed } = useAgentStatus(orgId, currentRunId);

  function handleTrigger() {
    triggerAgent.mutate(
      {},
      { onSuccess: (data: AgentRun) => setCurrentRunId(data.id) }
    );
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold">Remediation Planner Agent</h1>
        <p className="text-muted-foreground">Generate step-by-step remediation plans for failing controls</p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Run Remediation Planner</CardTitle>
          <CardDescription>Analyze all failing controls and generate actionable remediation plans.</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <Button onClick={handleTrigger} disabled={triggerAgent.isPending || polling}>
            {triggerAgent.isPending ? <Loader2 className="mr-2 h-4 w-4 animate-spin" /> : <Play className="mr-2 h-4 w-4" />}
            Run Remediation Planner
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
                  {run.output_data && ` — ${(run.output_data as Record<string, unknown>).remediation_count || 0} plans generated`}
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
                <Link href="/controls">
                  <Button variant="outline">View Controls</Button>
                </Link>
              </div>
            )}
          </CardContent>
        </Card>
      )}
    </div>
  );
}

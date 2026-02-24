"use client";

import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Progress } from "@/components/ui/progress";
import { Skeleton } from "@/components/ui/skeleton";
import { useVendors, useTriggerVendorRiskAgent } from "@/hooks/use-api";
import { useAgentStatus } from "@/hooks/use-agent-status";
import type { AgentRun } from "@/lib/types";
import { Bot, CheckCircle, Loader2, Play, XCircle } from "lucide-react";
import { useOrgId } from "@/hooks/use-org-id";
import Link from "next/link";

export default function VendorRiskAssessmentPage() {
  const orgId = useOrgId();
  const { data: vendorsData, isLoading: vendorsLoading } = useVendors(orgId);
  const [selectedVendorId, setSelectedVendorId] = useState<string>("");
  const [currentRunId, setCurrentRunId] = useState<string | null>(null);

  const triggerAgent = useTriggerVendorRiskAgent(orgId);
  const { run, polling, elapsed, isComplete, isFailed } = useAgentStatus(orgId, currentRunId);

  function handleTrigger() {
    if (!selectedVendorId) return;
    triggerAgent.mutate(
      { vendor_id: selectedVendorId },
      { onSuccess: (data: AgentRun) => setCurrentRunId(data.id) }
    );
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold">Vendor Risk Assessment Agent</h1>
        <p className="text-muted-foreground">Assess vendor risk and generate recommendations</p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Run Vendor Risk Assessment</CardTitle>
          <CardDescription>Select a vendor to assess their risk profile and generate recommendations.</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div>
            <label className="text-sm font-medium">Vendor</label>
            {vendorsLoading ? (
              <Skeleton className="mt-1 h-10 w-full" />
            ) : (
              <select
                className="mt-1 w-full rounded-md border bg-background p-2 text-sm"
                value={selectedVendorId}
                onChange={(e) => setSelectedVendorId(e.target.value)}
              >
                <option value="">Select a vendor...</option>
                {vendorsData?.items?.map((vendor) => (
                  <option key={vendor.id} value={vendor.id}>
                    {vendor.name} ({vendor.risk_tier})
                  </option>
                ))}
              </select>
            )}
          </div>
          <Button onClick={handleTrigger} disabled={!selectedVendorId || triggerAgent.isPending || polling}>
            {triggerAgent.isPending ? <Loader2 className="mr-2 h-4 w-4 animate-spin" /> : <Play className="mr-2 h-4 w-4" />}
            Run Vendor Risk Assessment
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
                  {run.output_data && ` — Risk score: ${(run.output_data as Record<string, unknown>).risk_score || "N/A"}, Tier: ${(run.output_data as Record<string, unknown>).risk_tier || "N/A"}`}
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
                <Link href="/vendors">
                  <Button variant="outline">View Vendors</Button>
                </Link>
              </div>
            )}
          </CardContent>
        </Card>
      )}
    </div>
  );
}

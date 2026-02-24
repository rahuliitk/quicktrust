"use client";

import { useState } from "react";
import Link from "next/link";
import { useParams } from "next/navigation";
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
  CardDescription,
} from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Skeleton } from "@/components/ui/skeleton";
import {
  useIntegration,
  useCollectionJobs,
  useTriggerCollection,
} from "@/hooks/use-api";
import { ArrowLeft, Play, Plug, History } from "lucide-react";
import { useOrgId } from "@/hooks/use-org-id";

const PROVIDER_COLLECTORS: Record<string, { type: string; label: string }[]> = {
  aws: [
    { type: "aws_iam_mfa_report", label: "IAM MFA Report" },
    { type: "aws_cloudtrail_status", label: "CloudTrail Status" },
    { type: "aws_encryption_at_rest", label: "Encryption at Rest" },
  ],
  github: [
    { type: "github_branch_protection", label: "Branch Protection" },
    { type: "github_dependabot_alerts", label: "Dependabot Alerts" },
  ],
  okta: [
    { type: "okta_mfa_enrollment", label: "MFA Enrollment" },
  ],
  prowler: [
    { type: "prowler_aws_full_scan", label: "Full AWS Security Scan" },
    { type: "prowler_aws_service_scan", label: "Service-Specific Scan" },
    { type: "prowler_aws_compliance_scan", label: "Compliance Framework Scan" },
  ],
};

const statusVariant: Record<string, "success" | "secondary" | "destructive"> = {
  connected: "success",
  disconnected: "secondary",
  error: "destructive",
};

const jobStatusVariant: Record<
  string,
  "success" | "secondary" | "destructive" | "warning" | "default"
> = {
  completed: "success",
  pending: "secondary",
  running: "warning",
  failed: "destructive",
};

export default function IntegrationDetailPage() {
  const params = useParams();
  const orgId = useOrgId();
  const integrationId = params.id as string;

  const { data: integration, isLoading } = useIntegration(
    orgId,
    integrationId
  );
  const { data: jobsData, isLoading: jobsLoading } = useCollectionJobs(
    orgId,
    integrationId
  );
  const triggerCollection = useTriggerCollection(orgId, integrationId);

  const [runningType, setRunningType] = useState<string | null>(null);

  const jobs = jobsData?.items || [];

  function handleCollect(collectorType: string) {
    setRunningType(collectorType);
    triggerCollection.mutate(
      { collector_type: collectorType },
      {
        onSettled: () => setRunningType(null),
      }
    );
  }

  if (isLoading) {
    return (
      <div className="space-y-4">
        <Skeleton className="h-6 w-32" />
        <Skeleton className="h-10 w-64" />
        <Skeleton className="h-64 w-full rounded-xl" />
      </div>
    );
  }

  if (!integration) {
    return (
      <div className="space-y-4">
        <Link
          href="/integrations"
          className="inline-flex items-center gap-1 text-sm text-muted-foreground hover:text-foreground transition-colors"
        >
          <ArrowLeft className="h-4 w-4" />
          Back to Integrations
        </Link>
        <p>Integration not found.</p>
      </div>
    );
  }

  const collectors = PROVIDER_COLLECTORS[integration.provider] || [];

  return (
    <div className="space-y-6">
      {/* Back link */}
      <Link
        href="/integrations"
        className="inline-flex items-center gap-1 text-sm text-muted-foreground hover:text-foreground transition-colors"
      >
        <ArrowLeft className="h-4 w-4" />
        Back to Integrations
      </Link>

      {/* Header */}
      <div className="flex items-center gap-3">
        <h1 className="text-3xl font-bold">{integration.name}</h1>
        <Badge variant="outline" className="capitalize">
          {integration.provider}
        </Badge>
        <Badge variant={statusVariant[integration.status] || "secondary"}>
          {integration.status}
        </Badge>
      </div>

      {integration.last_sync_at && (
        <p className="text-sm text-muted-foreground">
          Last synced{" "}
          {new Date(integration.last_sync_at).toLocaleDateString()}
        </p>
      )}

      {/* Configuration */}
      <Card>
        <CardHeader>
          <CardTitle>Configuration</CardTitle>
          <CardDescription>
            Connection settings for this integration
          </CardDescription>
        </CardHeader>
        <CardContent>
          {integration.config &&
          Object.keys(integration.config).length > 0 ? (
            <pre className="rounded-md border bg-muted/50 p-4 text-sm overflow-x-auto">
              {JSON.stringify(integration.config, null, 2)}
            </pre>
          ) : (
            <p className="text-sm text-muted-foreground">
              No configuration data available.
            </p>
          )}
        </CardContent>
      </Card>

      {/* Collect Now */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Plug className="h-5 w-5" />
            Collect Now
          </CardTitle>
          <CardDescription>
            Trigger an evidence collection run for this integration
          </CardDescription>
        </CardHeader>
        <CardContent>
          {collectors.length > 0 ? (
            <div className="space-y-3">
              {collectors.map((collector) => (
                <div
                  key={collector.type}
                  className="flex items-center justify-between rounded-lg border p-3"
                >
                  <div>
                    <div className="font-medium text-sm">
                      {collector.label}
                    </div>
                    <div className="text-xs text-muted-foreground font-mono">
                      {collector.type}
                    </div>
                  </div>
                  <Button
                    size="sm"
                    onClick={() => handleCollect(collector.type)}
                    disabled={
                      triggerCollection.isPending &&
                      runningType === collector.type
                    }
                  >
                    <Play className="mr-2 h-3 w-3" />
                    {triggerCollection.isPending &&
                    runningType === collector.type
                      ? "Running..."
                      : "Run"}
                  </Button>
                </div>
              ))}
            </div>
          ) : (
            <p className="text-sm text-muted-foreground">
              No collector types are defined for the{" "}
              <span className="font-medium capitalize">
                {integration.provider}
              </span>{" "}
              provider.
            </p>
          )}
        </CardContent>
      </Card>

      {/* Collection History */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <History className="h-5 w-5" />
            Collection History
          </CardTitle>
          <CardDescription>
            Previous evidence collection runs for this integration
          </CardDescription>
        </CardHeader>
        <CardContent>
          {jobsLoading ? (
            <div className="space-y-3">
              {[1, 2, 3].map((i) => (
                <Skeleton key={i} className="h-16 w-full rounded-lg" />
              ))}
            </div>
          ) : jobs.length > 0 ? (
            <div className="space-y-3">
              {jobs.map((job) => (
                <div
                  key={job.id}
                  className="flex items-center gap-4 rounded-lg border p-3"
                >
                  <div className="flex-1 min-w-0">
                    <div className="font-medium text-sm font-mono">
                      {job.collector_type}
                    </div>
                    <div className="mt-1 text-xs text-muted-foreground">
                      {new Date(job.created_at).toLocaleString()}
                      {job.error_message && (
                        <span className="ml-2 text-destructive">
                          {job.error_message}
                        </span>
                      )}
                    </div>
                  </div>
                  {job.result_data && (
                    <span className="text-xs text-muted-foreground">
                      {Object.keys(job.result_data).length}{" "}
                      {Object.keys(job.result_data).length === 1
                        ? "field"
                        : "fields"}
                    </span>
                  )}
                  <Badge
                    variant={jobStatusVariant[job.status] || "secondary"}
                  >
                    {job.status}
                  </Badge>
                </div>
              ))}
            </div>
          ) : (
            <div className="flex flex-col items-center justify-center py-8 text-center">
              <History className="h-10 w-10 text-muted-foreground mb-3" />
              <p className="text-sm text-muted-foreground">
                No collection jobs have been run yet. Use the collectors above
                to trigger your first run.
              </p>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}

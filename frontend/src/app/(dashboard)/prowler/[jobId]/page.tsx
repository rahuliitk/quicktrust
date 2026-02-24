"use client";

import Link from "next/link";
import { useParams } from "next/navigation";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Skeleton } from "@/components/ui/skeleton";
import { useProwlerScanDetail } from "@/hooks/use-api";
import { ArrowLeft, ShieldCheck, CheckCircle, XCircle } from "lucide-react";
import { useOrgId } from "@/hooks/use-org-id";

const severityColor: Record<string, string> = {
  critical: "bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-100",
  high: "bg-orange-100 text-orange-800 dark:bg-orange-900 dark:text-orange-100",
  medium: "bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-100",
  low: "bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-100",
};

export default function ProwlerScanDetailPage() {
  const params = useParams();
  const orgId = useOrgId();
  const jobId = params.jobId as string;

  const { data: scan, isLoading } = useProwlerScanDetail(orgId, jobId);

  if (isLoading) {
    return (
      <div className="space-y-4">
        <Skeleton className="h-6 w-32" />
        <Skeleton className="h-10 w-64" />
        <Skeleton className="h-64 w-full rounded-xl" />
      </div>
    );
  }

  if (!scan) {
    return (
      <div className="space-y-4">
        <Link
          href="/prowler"
          className="inline-flex items-center gap-1 text-sm text-muted-foreground hover:text-foreground transition-colors"
        >
          <ArrowLeft className="h-4 w-4" />
          Back to Security Scanner
        </Link>
        <p>Scan not found.</p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <Link
        href="/prowler"
        className="inline-flex items-center gap-1 text-sm text-muted-foreground hover:text-foreground transition-colors"
      >
        <ArrowLeft className="h-4 w-4" />
        Back to Security Scanner
      </Link>

      {/* Header */}
      <div className="flex items-center gap-3">
        <ShieldCheck className="h-8 w-8 text-primary" />
        <h1 className="text-3xl font-bold">
          {scan.scan_type === "full"
            ? "Full AWS Scan"
            : scan.scan_type === "service"
            ? "Service Scan"
            : "Compliance Scan"}
        </h1>
        <Badge variant={scan.status === "completed" ? "success" : "secondary"}>
          {scan.status}
        </Badge>
      </div>

      {scan.created_at && (
        <p className="text-sm text-muted-foreground">
          {new Date(scan.created_at).toLocaleString()} &middot; {scan.cloud_provider?.toUpperCase()}
        </p>
      )}

      {/* Summary Stats */}
      <div className="grid grid-cols-4 gap-4">
        <Card>
          <CardContent className="p-4 text-center">
            <div className="text-2xl font-bold">{scan.total_findings}</div>
            <div className="text-xs text-muted-foreground">Total Checks</div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4 text-center">
            <div className="text-2xl font-bold text-green-600">{scan.passed}</div>
            <div className="text-xs text-muted-foreground">Passed</div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4 text-center">
            <div className="text-2xl font-bold text-red-600">{scan.failed}</div>
            <div className="text-xs text-muted-foreground">Failed</div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4 text-center">
            <div className="text-2xl font-bold text-blue-600">{scan.pass_rate}%</div>
            <div className="text-xs text-muted-foreground">Pass Rate</div>
          </CardContent>
        </Card>
      </div>

      {/* Findings List */}
      <Card>
        <CardHeader>
          <CardTitle>Findings ({scan.findings?.length ?? 0})</CardTitle>
          <CardDescription>All security checks from this scan</CardDescription>
        </CardHeader>
        <CardContent className="space-y-3">
          {scan.findings && scan.findings.length > 0 ? (
            scan.findings.map((finding: any, idx: number) => (
              <div
                key={`${finding.check_id}-${idx}`}
                className="flex items-start gap-4 rounded-lg border p-3"
              >
                {finding.status === "PASS" ? (
                  <CheckCircle className="h-5 w-5 text-green-500 shrink-0 mt-0.5" />
                ) : (
                  <XCircle className="h-5 w-5 text-red-500 shrink-0 mt-0.5" />
                )}
                <div className="flex-1 min-w-0">
                  <div className="font-medium text-sm">{finding.check_title}</div>
                  <div className="mt-1 text-xs text-muted-foreground font-mono">
                    {finding.check_id}
                  </div>
                  <div className="mt-1 text-xs text-muted-foreground">
                    {finding.service} &middot; {finding.region} &middot; {finding.resource_id}
                  </div>
                  {finding.status_extended && (
                    <div className="mt-1 text-xs text-muted-foreground">
                      {finding.status_extended}
                    </div>
                  )}
                  {finding.remediation && finding.status === "FAIL" && (
                    <div className="mt-2 text-xs text-blue-600 dark:text-blue-400">
                      Remediation: {finding.remediation}
                    </div>
                  )}
                </div>
                <div className="flex flex-col items-end gap-1">
                  <Badge className={severityColor[finding.severity?.toLowerCase()] || ""}>
                    {finding.severity}
                  </Badge>
                  <Badge variant={finding.status === "PASS" ? "success" : "destructive"}>
                    {finding.status}
                  </Badge>
                </div>
              </div>
            ))
          ) : (
            <p className="text-sm text-muted-foreground text-center py-8">
              No findings in this scan.
            </p>
          )}
        </CardContent>
      </Card>
    </div>
  );
}

"use client";

import { useState } from "react";
import Link from "next/link";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Skeleton } from "@/components/ui/skeleton";
import {
  useProwlerFindingsSummary,
  useProwlerResults,
  useProwlerCompliancePosture,
  useProwlerTriggerScan,
  useIntegrations,
} from "@/hooks/use-api";
import {
  ShieldCheck,
  Play,
  Loader2,
  AlertTriangle,
  CheckCircle,
  XCircle,
  BarChart3,
  X,
} from "lucide-react";
import { useOrgId } from "@/hooks/use-org-id";

type TabValue = "findings" | "scans" | "compliance";

const SEVERITY_FILTERS: { label: string; value: string | undefined }[] = [
  { label: "All", value: undefined },
  { label: "Critical", value: "critical" },
  { label: "High", value: "high" },
  { label: "Medium", value: "medium" },
  { label: "Low", value: "low" },
];

const STATUS_FILTERS: { label: string; value: string | undefined }[] = [
  { label: "All", value: undefined },
  { label: "Pass", value: "PASS" },
  { label: "Fail", value: "FAIL" },
];

const severityColor: Record<string, string> = {
  critical: "bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-100",
  high: "bg-orange-100 text-orange-800 dark:bg-orange-900 dark:text-orange-100",
  medium: "bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-100",
  low: "bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-100",
};

export default function ProwlerPage() {
  const orgId = useOrgId();
  const [activeTab, setActiveTab] = useState<TabValue>("findings");
  const [severityFilter, setSeverityFilter] = useState<string | undefined>(undefined);
  const [statusFilter, setStatusFilter] = useState<string | undefined>(undefined);
  const [showTrigger, setShowTrigger] = useState(false);
  const [scanType, setScanType] = useState("full");
  const [scanIntegration, setScanIntegration] = useState("");
  const [scanServices, setScanServices] = useState("");
  const [scanFramework, setScanFramework] = useState("cis_1.5_aws");

  const { data: summary, isLoading: summaryLoading } = useProwlerFindingsSummary(orgId);
  const { data: resultsData, isLoading: resultsLoading } = useProwlerResults(orgId, {
    severity: severityFilter,
    status: statusFilter,
  });
  const { data: posture, isLoading: postureLoading } = useProwlerCompliancePosture(orgId);
  const { data: integrationsData } = useIntegrations(orgId);
  const triggerScan = useProwlerTriggerScan(orgId);

  const prowlerIntegrations = (integrationsData?.items || []).filter(
    (i: any) => i.provider === "prowler"
  );
  const results = resultsData?.items || [];

  function handleTriggerScan() {
    if (!scanIntegration) return;
    triggerScan.mutate(
      {
        integration_id: scanIntegration,
        scan_type: scanType,
        services: scanType === "service" ? scanServices.split(",").map((s: string) => s.trim()).filter(Boolean) : undefined,
        compliance_framework: scanType === "compliance" ? scanFramework : undefined,
      },
      {
        onSuccess: () => {
          setShowTrigger(false);
        },
      }
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold flex items-center gap-2">
            <ShieldCheck className="h-8 w-8 text-primary" />
            Security Scanner
          </h1>
          <p className="text-muted-foreground">
            Cloud security posture assessment powered by Prowler
          </p>
        </div>
        <Button onClick={() => setShowTrigger((v) => !v)} className="gap-1.5">
          <Play className="h-4 w-4" />
          Trigger Scan
        </Button>
      </div>

      {/* Trigger Scan Modal */}
      {showTrigger && (
        <Card className="border-primary">
          <CardHeader>
            <div className="flex items-center justify-between">
              <CardTitle>Trigger Security Scan</CardTitle>
              <Button size="sm" variant="ghost" onClick={() => setShowTrigger(false)}>
                <X className="h-4 w-4" />
              </Button>
            </div>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="space-y-1">
              <label className="text-sm font-medium">Integration</label>
              <select
                className="w-full rounded-md border bg-background p-2 text-sm"
                value={scanIntegration}
                onChange={(e) => setScanIntegration(e.target.value)}
              >
                <option value="">Select a Prowler integration...</option>
                {prowlerIntegrations.map((i: any) => (
                  <option key={i.id} value={i.id}>
                    {i.name}
                  </option>
                ))}
              </select>
            </div>

            <div className="space-y-1">
              <label className="text-sm font-medium">Scan Type</label>
              <select
                className="w-full rounded-md border bg-background p-2 text-sm"
                value={scanType}
                onChange={(e) => setScanType(e.target.value)}
              >
                <option value="full">Full AWS Scan</option>
                <option value="service">Service-Specific Scan</option>
                <option value="compliance">Compliance Framework Scan</option>
              </select>
            </div>

            {scanType === "service" && (
              <div className="space-y-1">
                <label className="text-sm font-medium">Services (comma-separated)</label>
                <input
                  type="text"
                  className="w-full rounded-md border bg-background p-2 text-sm"
                  placeholder="iam, s3, ec2, rds"
                  value={scanServices}
                  onChange={(e) => setScanServices(e.target.value)}
                />
              </div>
            )}

            {scanType === "compliance" && (
              <div className="space-y-1">
                <label className="text-sm font-medium">Compliance Framework</label>
                <select
                  className="w-full rounded-md border bg-background p-2 text-sm"
                  value={scanFramework}
                  onChange={(e) => setScanFramework(e.target.value)}
                >
                  <option value="cis_1.5_aws">CIS AWS 1.5</option>
                  <option value="cis_2.0_aws">CIS AWS 2.0</option>
                  <option value="soc2_aws">SOC 2</option>
                  <option value="hipaa_aws">HIPAA</option>
                  <option value="pci_3.2.1_aws">PCI DSS 3.2.1</option>
                </select>
              </div>
            )}

            <div className="flex gap-2 pt-2">
              <Button
                onClick={handleTriggerScan}
                disabled={!scanIntegration || triggerScan.isPending}
              >
                {triggerScan.isPending ? (
                  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                ) : (
                  <Play className="mr-2 h-4 w-4" />
                )}
                Start Scan
              </Button>
              <Button variant="ghost" onClick={() => setShowTrigger(false)}>
                Cancel
              </Button>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Stats Cards */}
      {summaryLoading ? (
        <div className="grid grid-cols-4 gap-4">
          {[1, 2, 3, 4].map((i) => (
            <Skeleton key={i} className="h-24 w-full rounded-xl" />
          ))}
        </div>
      ) : summary ? (
        <div className="grid grid-cols-4 gap-4">
          <Card>
            <CardContent className="p-4 text-center">
              <div className="text-2xl font-bold text-green-600">
                {summary.pass_rate ?? 0}%
              </div>
              <div className="text-xs text-muted-foreground">Overall Pass Rate</div>
            </CardContent>
          </Card>
          <Card>
            <CardContent className="p-4 text-center">
              <div className="text-2xl font-bold">{summary.total ?? 0}</div>
              <div className="text-xs text-muted-foreground">Total Checks</div>
            </CardContent>
          </Card>
          <Card>
            <CardContent className="p-4 text-center">
              <div className="text-2xl font-bold text-red-600">{summary.failed ?? 0}</div>
              <div className="text-xs text-muted-foreground">Failed Findings</div>
            </CardContent>
          </Card>
          <Card>
            <CardContent className="p-4 text-center">
              <div className="text-2xl font-bold text-orange-600">
                {(summary.critical_count ?? 0) + (summary.high_count ?? 0)}
              </div>
              <div className="text-xs text-muted-foreground">Critical/High</div>
            </CardContent>
          </Card>
        </div>
      ) : null}

      {/* Tab Buttons */}
      <div className="flex gap-2 border-b pb-1">
        <Button
          variant={activeTab === "findings" ? "default" : "ghost"}
          size="sm"
          onClick={() => setActiveTab("findings")}
          className="gap-1.5"
        >
          <AlertTriangle className="h-4 w-4" />
          Findings
        </Button>
        <Button
          variant={activeTab === "scans" ? "default" : "ghost"}
          size="sm"
          onClick={() => setActiveTab("scans")}
          className="gap-1.5"
        >
          <ShieldCheck className="h-4 w-4" />
          Scans
        </Button>
        <Button
          variant={activeTab === "compliance" ? "default" : "ghost"}
          size="sm"
          onClick={() => setActiveTab("compliance")}
          className="gap-1.5"
        >
          <BarChart3 className="h-4 w-4" />
          Compliance
        </Button>
      </div>

      {/* Findings Tab */}
      {activeTab === "findings" && (
        <div className="space-y-4">
          <div className="flex flex-wrap gap-2">
            <span className="flex items-center text-sm text-muted-foreground mr-1">Severity:</span>
            {SEVERITY_FILTERS.map((f) => (
              <Button
                key={f.label}
                variant={severityFilter === f.value ? "default" : "outline"}
                size="sm"
                onClick={() => setSeverityFilter(f.value)}
              >
                {f.label}
              </Button>
            ))}
            <span className="mx-2 border-l" />
            <span className="flex items-center text-sm text-muted-foreground mr-1">Status:</span>
            {STATUS_FILTERS.map((f) => (
              <Button
                key={f.label}
                variant={statusFilter === f.value ? "default" : "outline"}
                size="sm"
                onClick={() => setStatusFilter(f.value)}
              >
                {f.label}
              </Button>
            ))}
          </div>

          {resultsLoading ? (
            <div className="space-y-3">
              {[1, 2, 3].map((i) => (
                <Skeleton key={i} className="h-20 w-full rounded-xl" />
              ))}
            </div>
          ) : results.length > 0 ? (
            <div className="space-y-3">
              {results.flatMap((scan: any) =>
                (scan.findings || []).map((finding: any, idx: number) => (
                  <Card key={`${scan.job_id}-${idx}`}>
                    <CardContent className="flex items-center gap-4 p-4">
                      {finding.status === "PASS" ? (
                        <CheckCircle className="h-5 w-5 text-green-500 shrink-0" />
                      ) : (
                        <XCircle className="h-5 w-5 text-red-500 shrink-0" />
                      )}
                      <div className="flex-1 min-w-0">
                        <div className="font-medium text-sm">{finding.check_title}</div>
                        <div className="mt-1 text-xs text-muted-foreground">
                          {finding.service} &middot; {finding.region} &middot; {finding.resource_id}
                        </div>
                        {finding.status_extended && (
                          <div className="mt-1 text-xs text-muted-foreground">
                            {finding.status_extended}
                          </div>
                        )}
                      </div>
                      <Badge className={severityColor[finding.severity?.toLowerCase()] || ""}>
                        {finding.severity}
                      </Badge>
                      <Badge variant={finding.status === "PASS" ? "success" : "destructive"}>
                        {finding.status}
                      </Badge>
                    </CardContent>
                  </Card>
                ))
              )}
            </div>
          ) : (
            <Card>
              <CardContent className="flex flex-col items-center justify-center p-12 text-center">
                <ShieldCheck className="h-12 w-12 text-muted-foreground mb-4" />
                <h3 className="text-lg font-medium">No findings</h3>
                <p className="text-sm text-muted-foreground mt-1">
                  Run a security scan to see findings here.
                </p>
              </CardContent>
            </Card>
          )}
        </div>
      )}

      {/* Scans Tab */}
      {activeTab === "scans" && (
        <div className="space-y-3">
          {resultsLoading ? (
            <div className="space-y-3">
              {[1, 2, 3].map((i) => (
                <Skeleton key={i} className="h-20 w-full rounded-xl" />
              ))}
            </div>
          ) : results.length > 0 ? (
            results.map((scan: any) => (
              <Link key={scan.job_id} href={`/prowler/${scan.job_id}`}>
                <Card className="transition-colors hover:bg-accent/50">
                  <CardContent className="flex items-center gap-4 p-4">
                    <ShieldCheck className="h-8 w-8 text-muted-foreground shrink-0" />
                    <div className="flex-1 min-w-0">
                      <div className="font-medium text-sm">
                        {scan.scan_type === "full"
                          ? "Full AWS Scan"
                          : scan.scan_type === "service"
                          ? "Service Scan"
                          : "Compliance Scan"}
                      </div>
                      <div className="mt-1 text-xs text-muted-foreground">
                        {scan.created_at && new Date(scan.created_at).toLocaleString()}
                        {" "}&middot; {scan.cloud_provider?.toUpperCase()}
                      </div>
                    </div>
                    <div className="text-right text-sm">
                      <div className="font-medium text-green-600">{scan.passed} passed</div>
                      <div className="text-red-600">{scan.failed} failed</div>
                    </div>
                    <Badge variant={scan.pass_rate >= 80 ? "success" : scan.pass_rate >= 50 ? "warning" : "destructive"}>
                      {scan.pass_rate}%
                    </Badge>
                    <Badge variant={scan.status === "completed" ? "success" : "secondary"}>
                      {scan.status}
                    </Badge>
                  </CardContent>
                </Card>
              </Link>
            ))
          ) : (
            <Card>
              <CardContent className="flex flex-col items-center justify-center p-12 text-center">
                <ShieldCheck className="h-12 w-12 text-muted-foreground mb-4" />
                <h3 className="text-lg font-medium">No scans yet</h3>
                <p className="text-sm text-muted-foreground mt-1">
                  Trigger a security scan to get started.
                </p>
              </CardContent>
            </Card>
          )}
        </div>
      )}

      {/* Compliance Tab */}
      {activeTab === "compliance" && (
        <div className="space-y-6">
          {postureLoading ? (
            <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
              {[1, 2, 3].map((i) => (
                <Skeleton key={i} className="h-32 w-full rounded-xl" />
              ))}
            </div>
          ) : posture && posture.frameworks?.length > 0 ? (
            <>
              <section className="space-y-3">
                <h2 className="text-lg font-semibold">Compliance Frameworks</h2>
                <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
                  {posture.frameworks.map((fw: any) => (
                    <Card key={fw.framework}>
                      <CardHeader className="pb-2">
                        <CardTitle className="text-base">{fw.framework}</CardTitle>
                        <CardDescription>
                          {fw.total_checks} checks &middot; {fw.passed} passed &middot; {fw.failed} failed
                        </CardDescription>
                      </CardHeader>
                      <CardContent>
                        <div className="flex items-center gap-3">
                          <div className="flex-1 h-2 rounded-full bg-muted overflow-hidden">
                            <div
                              className="h-full bg-green-500 rounded-full transition-all"
                              style={{ width: `${fw.pass_rate}%` }}
                            />
                          </div>
                          <span className="text-sm font-medium">{fw.pass_rate}%</span>
                        </div>
                      </CardContent>
                    </Card>
                  ))}
                </div>
              </section>

              <section className="space-y-3">
                <h2 className="text-lg font-semibold">By Service</h2>
                <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
                  {posture.services.map((svc: any) => (
                    <Card key={svc.service}>
                      <CardHeader className="pb-2">
                        <CardTitle className="text-base">{svc.service}</CardTitle>
                        <CardDescription>
                          {svc.total_checks} checks &middot; {svc.passed} passed &middot; {svc.failed} failed
                        </CardDescription>
                      </CardHeader>
                      <CardContent>
                        <div className="flex items-center gap-3">
                          <div className="flex-1 h-2 rounded-full bg-muted overflow-hidden">
                            <div
                              className="h-full bg-blue-500 rounded-full transition-all"
                              style={{ width: `${svc.pass_rate}%` }}
                            />
                          </div>
                          <span className="text-sm font-medium">{svc.pass_rate}%</span>
                        </div>
                      </CardContent>
                    </Card>
                  ))}
                </div>
              </section>
            </>
          ) : (
            <Card>
              <CardContent className="flex flex-col items-center justify-center p-12 text-center">
                <BarChart3 className="h-12 w-12 text-muted-foreground mb-4" />
                <h3 className="text-lg font-medium">No compliance data</h3>
                <p className="text-sm text-muted-foreground mt-1">
                  Run a security scan to see compliance posture.
                </p>
              </CardContent>
            </Card>
          )}
        </div>
      )}
    </div>
  );
}

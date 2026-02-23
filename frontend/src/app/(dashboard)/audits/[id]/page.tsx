"use client";

import { useState } from "react";
import Link from "next/link";
import { useParams } from "next/navigation";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Skeleton } from "@/components/ui/skeleton";
import {
  useAudit,
  useAuditFindings,
  useAuditTokens,
  useCreateFinding,
  useCreateToken,
  useRevokeToken,
} from "@/hooks/use-api";
import {
  ArrowLeft,
  ClipboardCheck,
  AlertTriangle,
  KeyRound,
  LayoutDashboard,
  Plus,
  Loader2,
  Copy,
  Ban,
} from "lucide-react";
import type { AuditStatus } from "@/lib/types";

const DEMO_ORG_ID = "00000000-0000-0000-0000-000000000000";

type TabValue = "overview" | "findings" | "tokens";

const statusColors: Record<AuditStatus, string> = {
  planning: "secondary",
  preparation: "secondary",
  fieldwork: "warning",
  reporting: "warning",
  completed: "success",
  closed: "outline",
};

const severityColors: Record<string, string> = {
  critical: "bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-100",
  high: "bg-orange-100 text-orange-800 dark:bg-orange-900 dark:text-orange-100",
  medium: "bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-100",
  low: "bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-100",
};

const findingStatusVariant: Record<string, "default" | "secondary" | "success" | "destructive" | "warning"> = {
  open: "destructive",
  in_progress: "warning",
  resolved: "success",
  accepted: "secondary",
};

export default function AuditDetailPage() {
  const params = useParams();
  const auditId = params.id as string;
  const [activeTab, setActiveTab] = useState<TabValue>("overview");

  const { data: audit, isLoading } = useAudit(DEMO_ORG_ID, auditId);
  const { data: findings, isLoading: findingsLoading } = useAuditFindings(
    DEMO_ORG_ID,
    auditId
  );
  const { data: tokens, isLoading: tokensLoading } = useAuditTokens(
    DEMO_ORG_ID,
    auditId
  );

  if (isLoading) {
    return (
      <div className="space-y-4">
        <Skeleton className="h-6 w-32" />
        <Skeleton className="h-10 w-64" />
        <Skeleton className="h-64 w-full rounded-xl" />
      </div>
    );
  }

  if (!audit) {
    return (
      <div className="space-y-4">
        <Link
          href="/audits"
          className="inline-flex items-center gap-1 text-sm text-muted-foreground hover:text-foreground transition-colors"
        >
          <ArrowLeft className="h-4 w-4" />
          Back to Audits
        </Link>
        <p>Audit not found.</p>
      </div>
    );
  }

  const tabs: { value: TabValue; label: string; icon: React.ReactNode }[] = [
    {
      value: "overview",
      label: "Overview",
      icon: <LayoutDashboard className="h-4 w-4" />,
    },
    {
      value: "findings",
      label: `Findings${findings ? ` (${findings.length})` : ""}`,
      icon: <AlertTriangle className="h-4 w-4" />,
    },
    {
      value: "tokens",
      label: `Access Tokens${tokens ? ` (${tokens.length})` : ""}`,
      icon: <KeyRound className="h-4 w-4" />,
    },
  ];

  return (
    <div className="space-y-6">
      {/* Back link */}
      <Link
        href="/audits"
        className="inline-flex items-center gap-1 text-sm text-muted-foreground hover:text-foreground transition-colors"
      >
        <ArrowLeft className="h-4 w-4" />
        Back to Audits
      </Link>

      {/* Header */}
      <div className="flex items-center gap-3">
        <h1 className="text-3xl font-bold">{audit.title}</h1>
        <Badge variant={(statusColors[audit.status] || "secondary") as any}>
          {audit.status}
        </Badge>
        <Badge variant="outline">{audit.audit_type}</Badge>
      </div>

      {/* Tab buttons */}
      <div className="flex gap-2 border-b pb-1">
        {tabs.map((tab) => (
          <Button
            key={tab.value}
            variant={activeTab === tab.value ? "default" : "ghost"}
            size="sm"
            onClick={() => setActiveTab(tab.value)}
            className="gap-1.5"
          >
            {tab.icon}
            {tab.label}
          </Button>
        ))}
      </div>

      {/* Tab content */}
      {activeTab === "overview" && <OverviewTab audit={audit} />}
      {activeTab === "findings" && (
        <FindingsTab findings={findings || []} isLoading={findingsLoading} auditId={auditId} />
      )}
      {activeTab === "tokens" && (
        <TokensTab tokens={tokens || []} isLoading={tokensLoading} auditId={auditId} />
      )}
    </div>
  );
}

/* ------------------------------------------------------------------ */
/* Overview Tab                                                        */
/* ------------------------------------------------------------------ */

function OverviewTab({
  audit,
}: {
  audit: NonNullable<ReturnType<typeof useAudit>["data"]>;
}) {
  return (
    <div className="grid gap-6 md:grid-cols-2">
      <Card>
        <CardHeader>
          <CardTitle>Audit Details</CardTitle>
        </CardHeader>
        <CardContent>
          <dl className="space-y-4 text-sm">
            <div>
              <dt className="font-medium text-muted-foreground">
                Auditor Firm
              </dt>
              <dd className="mt-1">{audit.auditor_firm || "Not specified"}</dd>
            </div>
            <div>
              <dt className="font-medium text-muted-foreground">
                Lead Auditor
              </dt>
              <dd className="mt-1">
                {audit.lead_auditor_name || "Not specified"}
              </dd>
            </div>
            <div>
              <dt className="font-medium text-muted-foreground">Audit Type</dt>
              <dd className="mt-1 capitalize">{audit.audit_type}</dd>
            </div>
            <div>
              <dt className="font-medium text-muted-foreground">Created</dt>
              <dd className="mt-1">
                {new Date(audit.created_at).toLocaleDateString()}
              </dd>
            </div>
          </dl>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Schedule & Readiness</CardTitle>
        </CardHeader>
        <CardContent>
          <dl className="space-y-4 text-sm">
            <div>
              <dt className="font-medium text-muted-foreground">
                Scheduled Start
              </dt>
              <dd className="mt-1">
                {audit.scheduled_start
                  ? new Date(audit.scheduled_start).toLocaleDateString()
                  : "Not scheduled"}
              </dd>
            </div>
            <div>
              <dt className="font-medium text-muted-foreground">
                Scheduled End
              </dt>
              <dd className="mt-1">
                {audit.scheduled_end
                  ? new Date(audit.scheduled_end).toLocaleDateString()
                  : "Not scheduled"}
              </dd>
            </div>
            <div>
              <dt className="font-medium text-muted-foreground">
                Readiness Score
              </dt>
              <dd className="mt-2">
                {audit.readiness_score != null ? (
                  <div className="flex items-center gap-3">
                    <div className="flex-1 h-3 rounded-full bg-primary/20 overflow-hidden">
                      <div
                        className={`h-full rounded-full transition-all ${
                          audit.readiness_score >= 80
                            ? "bg-green-500"
                            : audit.readiness_score >= 50
                            ? "bg-yellow-500"
                            : "bg-red-500"
                        }`}
                        style={{ width: `${Math.round(audit.readiness_score)}%` }}
                      />
                    </div>
                    <span className="text-base font-bold">
                      {Math.round(audit.readiness_score)}%
                    </span>
                  </div>
                ) : (
                  <span className="text-muted-foreground">Not assessed</span>
                )}
              </dd>
            </div>
          </dl>
        </CardContent>
      </Card>
    </div>
  );
}

/* ------------------------------------------------------------------ */
/* Findings Tab                                                        */
/* ------------------------------------------------------------------ */

function FindingsTab({
  findings,
  isLoading,
  auditId,
}: {
  findings: NonNullable<ReturnType<typeof useAuditFindings>["data"]>;
  isLoading: boolean;
  auditId: string;
}) {
  const [showAddFinding, setShowAddFinding] = useState(false);
  const [form, setForm] = useState({ title: "", description: "", severity: "medium" });
  const createFinding = useCreateFinding(DEMO_ORG_ID, auditId);

  if (isLoading) {
    return (
      <div className="space-y-3">
        {[1, 2, 3].map((i) => (
          <Skeleton key={i} className="h-20 w-full rounded-xl" />
        ))}
      </div>
    );
  }

  return (
    <div className="space-y-3">
      {/* Add Finding button */}
      <div className="flex justify-end">
        <Button
          size="sm"
          onClick={() => setShowAddFinding((v) => !v)}
          className="gap-1.5"
        >
          <Plus className="h-4 w-4" />
          Add Finding
        </Button>
      </div>

      {/* Add Finding form */}
      {showAddFinding && (
        <Card>
          <CardHeader>
            <CardTitle>New Finding</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div>
              <label className="text-sm font-medium">Title</label>
              <input
                type="text"
                required
                className="mt-1 w-full rounded-md border bg-background p-2 text-sm"
                placeholder="Finding title"
                value={form.title}
                onChange={(e) => setForm((f) => ({ ...f, title: e.target.value }))}
              />
            </div>
            <div>
              <label className="text-sm font-medium">Description</label>
              <textarea
                className="mt-1 w-full rounded-md border bg-background p-2 text-sm"
                placeholder="Optional description"
                rows={3}
                value={form.description}
                onChange={(e) => setForm((f) => ({ ...f, description: e.target.value }))}
              />
            </div>
            <div>
              <label className="text-sm font-medium">Severity</label>
              <select
                className="mt-1 w-full rounded-md border bg-background p-2 text-sm"
                value={form.severity}
                onChange={(e) => setForm((f) => ({ ...f, severity: e.target.value }))}
              >
                <option value="critical">Critical</option>
                <option value="high">High</option>
                <option value="medium">Medium</option>
                <option value="low">Low</option>
              </select>
            </div>
            <div className="flex gap-2">
              <Button
                size="sm"
                disabled={!form.title.trim() || createFinding.isPending}
                onClick={() =>
                  createFinding.mutate(
                    {
                      title: form.title.trim(),
                      description: form.description.trim() || undefined,
                      severity: form.severity,
                    },
                    {
                      onSuccess: () => {
                        setShowAddFinding(false);
                        setForm({ title: "", description: "", severity: "medium" });
                      },
                    }
                  )
                }
              >
                {createFinding.isPending && (
                  <Loader2 className="mr-1.5 h-4 w-4 animate-spin" />
                )}
                Save
              </Button>
              <Button
                size="sm"
                variant="ghost"
                onClick={() => {
                  setShowAddFinding(false);
                  setForm({ title: "", description: "", severity: "medium" });
                }}
              >
                Cancel
              </Button>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Empty state */}
      {findings.length === 0 && !showAddFinding && (
        <Card>
          <CardContent className="p-12 text-center">
            <AlertTriangle className="mx-auto h-12 w-12 text-muted-foreground" />
            <h3 className="mt-4 text-lg font-semibold">No findings</h3>
            <p className="mt-2 text-sm text-muted-foreground">
              No audit findings have been recorded for this audit.
            </p>
          </CardContent>
        </Card>
      )}

      {/* Findings list */}
      {findings.map((finding) => (
        <Card key={finding.id}>
          <CardContent className="flex items-center gap-4 p-4">
            <div className="flex-1 min-w-0">
              <div className="font-medium">{finding.title}</div>
              {finding.description && (
                <p className="mt-1 text-sm text-muted-foreground line-clamp-2">
                  {finding.description}
                </p>
              )}
              <div className="mt-2 flex flex-wrap items-center gap-2 text-xs text-muted-foreground">
                {finding.control_id && (
                  <Link
                    href={`/controls/${finding.control_id}`}
                    className="hover:underline"
                  >
                    Control: {finding.control_id.slice(0, 8)}...
                  </Link>
                )}
                {finding.remediation_due_date && (
                  <span>
                    Due:{" "}
                    {new Date(finding.remediation_due_date).toLocaleDateString()}
                  </span>
                )}
              </div>
            </div>
            <div className="flex items-center gap-2 shrink-0">
              <Badge className={severityColors[finding.severity] || ""}>
                {finding.severity}
              </Badge>
              <Badge
                variant={
                  (findingStatusVariant[finding.status] || "secondary") as any
                }
              >
                {finding.status.replace(/_/g, " ")}
              </Badge>
            </div>
          </CardContent>
        </Card>
      ))}
    </div>
  );
}

/* ------------------------------------------------------------------ */
/* Tokens Tab                                                          */
/* ------------------------------------------------------------------ */

function TokensTab({
  tokens,
  isLoading,
  auditId,
}: {
  tokens: NonNullable<ReturnType<typeof useAuditTokens>["data"]>;
  isLoading: boolean;
  auditId: string;
}) {
  const [showCreate, setShowCreate] = useState(false);
  const [copiedToken, setCopiedToken] = useState<string | null>(null);
  const [form, setForm] = useState({ auditor_email: "", auditor_name: "", expires_in_days: 30 });
  const createToken = useCreateToken(DEMO_ORG_ID, auditId);
  const revokeToken = useRevokeToken(DEMO_ORG_ID, auditId);

  if (isLoading) {
    return (
      <div className="space-y-3">
        {[1, 2, 3].map((i) => (
          <Skeleton key={i} className="h-16 w-full rounded-xl" />
        ))}
      </div>
    );
  }

  return (
    <div className="space-y-3">
      {/* Generate Token button */}
      <div className="flex justify-end">
        <Button
          size="sm"
          onClick={() => {
            setShowCreate((v) => !v);
            setCopiedToken(null);
          }}
          className="gap-1.5"
        >
          <Plus className="h-4 w-4" />
          Generate Token
        </Button>
      </div>

      {/* Newly generated token display */}
      {copiedToken && (
        <Card className="border-green-500">
          <CardContent className="p-4 space-y-2">
            <p className="text-sm font-medium text-green-700 dark:text-green-400">
              Token generated successfully. Copy it now -- it will not be shown again.
            </p>
            <div className="flex items-center gap-2">
              <code className="flex-1 rounded-md bg-muted p-2 text-xs break-all">
                {copiedToken}
              </code>
              <Button
                size="sm"
                variant="outline"
                className="shrink-0 gap-1.5"
                onClick={() => navigator.clipboard.writeText(copiedToken)}
              >
                <Copy className="h-4 w-4" />
                Copy
              </Button>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Generate Token form */}
      {showCreate && (
        <Card>
          <CardHeader>
            <CardTitle>Generate Access Token</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div>
              <label className="text-sm font-medium">Auditor Email</label>
              <input
                type="email"
                required
                className="mt-1 w-full rounded-md border bg-background p-2 text-sm"
                placeholder="auditor@firm.com"
                value={form.auditor_email}
                onChange={(e) => setForm((f) => ({ ...f, auditor_email: e.target.value }))}
              />
            </div>
            <div>
              <label className="text-sm font-medium">Auditor Name</label>
              <input
                type="text"
                className="mt-1 w-full rounded-md border bg-background p-2 text-sm"
                placeholder="Optional name"
                value={form.auditor_name}
                onChange={(e) => setForm((f) => ({ ...f, auditor_name: e.target.value }))}
              />
            </div>
            <div>
              <label className="text-sm font-medium">Expires In</label>
              <select
                className="mt-1 w-full rounded-md border bg-background p-2 text-sm"
                value={form.expires_in_days}
                onChange={(e) => setForm((f) => ({ ...f, expires_in_days: Number(e.target.value) }))}
              >
                <option value={7}>7 days</option>
                <option value={14}>14 days</option>
                <option value={30}>30 days</option>
                <option value={60}>60 days</option>
                <option value={90}>90 days</option>
              </select>
            </div>
            <div className="flex gap-2">
              <Button
                size="sm"
                disabled={!form.auditor_email.trim() || createToken.isPending}
                onClick={() =>
                  createToken.mutate(
                    {
                      auditor_email: form.auditor_email.trim(),
                      auditor_name: form.auditor_name.trim() || undefined,
                      expires_in_days: form.expires_in_days,
                    },
                    {
                      onSuccess: (data: any) => {
                        setShowCreate(false);
                        setForm({ auditor_email: "", auditor_name: "", expires_in_days: 30 });
                        if (data && data.token) {
                          setCopiedToken(data.token);
                        }
                      },
                    }
                  )
                }
              >
                {createToken.isPending && (
                  <Loader2 className="mr-1.5 h-4 w-4 animate-spin" />
                )}
                Generate
              </Button>
              <Button
                size="sm"
                variant="ghost"
                onClick={() => {
                  setShowCreate(false);
                  setForm({ auditor_email: "", auditor_name: "", expires_in_days: 30 });
                }}
              >
                Cancel
              </Button>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Empty state */}
      {tokens.length === 0 && !showCreate && !copiedToken && (
        <Card>
          <CardContent className="p-12 text-center">
            <KeyRound className="mx-auto h-12 w-12 text-muted-foreground" />
            <h3 className="mt-4 text-lg font-semibold">No access tokens</h3>
            <p className="mt-2 text-sm text-muted-foreground">
              No auditor access tokens have been issued for this audit.
            </p>
          </CardContent>
        </Card>
      )}

      {/* Tokens list */}
      {tokens.map((token) => {
        const isExpired = new Date(token.expires_at) < new Date();

        return (
          <Card key={token.id}>
            <CardContent className="flex items-center gap-4 p-4">
              <KeyRound className="h-5 w-5 text-muted-foreground shrink-0" />
              <div className="flex-1 min-w-0">
                <div className="font-medium text-sm">
                  {token.auditor_name || "Unnamed Auditor"}
                </div>
                <div className="text-sm text-muted-foreground">
                  {token.auditor_email}
                </div>
                <div className="mt-1 text-xs text-muted-foreground">
                  Expires:{" "}
                  {new Date(token.expires_at).toLocaleDateString()}{" "}
                  {new Date(token.expires_at).toLocaleTimeString()}
                </div>
              </div>
              <div className="flex items-center gap-2 shrink-0">
                {isExpired ? (
                  <Badge variant="destructive">Expired</Badge>
                ) : token.is_active ? (
                  <Badge variant="success">Active</Badge>
                ) : (
                  <Badge variant="secondary">Inactive</Badge>
                )}
                {token.is_active && !isExpired && (
                  <Button
                    size="sm"
                    variant="ghost"
                    className="gap-1 text-destructive hover:text-destructive"
                    disabled={revokeToken.isPending}
                    onClick={() => {
                      if (window.confirm("Are you sure you want to revoke this token?")) {
                        revokeToken.mutate(token.id);
                      }
                    }}
                  >
                    <Ban className="h-4 w-4" />
                    Revoke
                  </Button>
                )}
              </div>
            </CardContent>
          </Card>
        );
      })}
    </div>
  );
}

"use client";

import { useState } from "react";
import Link from "next/link";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Skeleton } from "@/components/ui/skeleton";
import { Progress } from "@/components/ui/progress";
import { useAudits, useReadinessScore, useCreateAudit, useFrameworks } from "@/hooks/use-api";
import { ClipboardCheck, ShieldCheck, Plus, Loader2 } from "lucide-react";
import type { AuditStatus } from "@/lib/types";

const DEMO_ORG_ID = "00000000-0000-0000-0000-000000000000";

const statusColors: Record<AuditStatus, string> = {
  planning: "secondary",
  preparation: "secondary",
  fieldwork: "warning",
  reporting: "warning",
  completed: "success",
  closed: "outline",
};

const auditTypeBadgeVariant: Record<string, "default" | "outline" | "secondary"> = {
  internal: "secondary",
  external: "default",
  readiness: "outline",
};

function ReadinessGauge({ score, label }: { score: number; label: string }) {
  return (
    <div className="space-y-1">
      <div className="flex items-center justify-between text-sm">
        <span className="text-muted-foreground">{label}</span>
        <span className="font-medium">{Math.round(score)}%</span>
      </div>
      <Progress value={score} className="h-2" />
    </div>
  );
}

function ReadinessPanel() {
  const { data: readiness, isLoading } = useReadinessScore(DEMO_ORG_ID);

  if (isLoading) {
    return (
      <Card>
        <CardContent className="p-6">
          <div className="flex items-center gap-8">
            <Skeleton className="h-28 w-28 rounded-full" />
            <div className="flex-1 space-y-4">
              <Skeleton className="h-4 w-full" />
              <Skeleton className="h-4 w-full" />
              <Skeleton className="h-4 w-full" />
              <Skeleton className="h-4 w-full" />
            </div>
          </div>
        </CardContent>
      </Card>
    );
  }

  if (!readiness) return null;

  const overall = Math.round(readiness.overall_score);

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <ShieldCheck className="h-5 w-5" />
          Audit Readiness
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className="flex items-center gap-8">
          {/* Large circular score */}
          <div className="relative flex h-28 w-28 shrink-0 items-center justify-center">
            <svg className="h-28 w-28 -rotate-90" viewBox="0 0 120 120">
              <circle
                cx="60"
                cy="60"
                r="52"
                fill="none"
                stroke="currentColor"
                strokeWidth="10"
                className="text-muted/30"
              />
              <circle
                cx="60"
                cy="60"
                r="52"
                fill="none"
                stroke="currentColor"
                strokeWidth="10"
                strokeDasharray={`${(overall / 100) * 2 * Math.PI * 52} ${2 * Math.PI * 52}`}
                strokeLinecap="round"
                className={
                  overall >= 80
                    ? "text-green-500"
                    : overall >= 50
                    ? "text-yellow-500"
                    : "text-red-500"
                }
              />
            </svg>
            <div className="absolute inset-0 flex flex-col items-center justify-center">
              <span className="text-2xl font-bold">{overall}%</span>
              <span className="text-xs text-muted-foreground">Overall</span>
            </div>
          </div>

          {/* Breakdown bars */}
          <div className="flex-1 space-y-3">
            <ReadinessGauge
              score={readiness.controls_score}
              label={`Controls (${readiness.controls_implemented}/${readiness.controls_total})`}
            />
            <ReadinessGauge
              score={readiness.evidence_score}
              label={`Evidence (${readiness.evidence_collected}/${readiness.evidence_total})`}
            />
            <ReadinessGauge
              score={readiness.policies_score}
              label={`Policies (${readiness.policies_published}/${readiness.policies_total})`}
            />
            <ReadinessGauge
              score={readiness.risks_score}
              label={`Risks (${readiness.risks_treated}/${readiness.risks_total})`}
            />
          </div>
        </div>
      </CardContent>
    </Card>
  );
}

export default function AuditsPage() {
  const { data, isLoading } = useAudits(DEMO_ORG_ID);
  const audits = data?.items || [];

  const [showCreate, setShowCreate] = useState(false);
  const [form, setForm] = useState({
    title: "",
    audit_type: "external",
    framework_id: "",
    auditor_firm: "",
  });

  const createAudit = useCreateAudit(DEMO_ORG_ID);
  const { data: frameworks } = useFrameworks();

  const resetForm = () =>
    setForm({ title: "", audit_type: "external", framework_id: "", auditor_firm: "" });

  const handleCreate = () => {
    if (!form.title.trim()) return;
    createAudit.mutate(
      {
        title: form.title,
        audit_type: form.audit_type,
        framework_id: form.framework_id || undefined,
        auditor_firm: form.auditor_firm || undefined,
      },
      {
        onSuccess: () => {
          setShowCreate(false);
          resetForm();
        },
      }
    );
  };

  return (
    <div className="space-y-6">
      {/* Page header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold">Audits</h1>
          <p className="text-muted-foreground">
            Manage compliance audits and readiness
          </p>
        </div>
        <Button onClick={() => setShowCreate((v) => !v)}>
          <Plus className="mr-2 h-4 w-4" />
          New Audit
        </Button>
      </div>

      {/* Inline create form */}
      {showCreate && (
        <Card>
          <CardHeader>
            <CardTitle>Create New Audit</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid gap-4 sm:grid-cols-2">
              <div className="sm:col-span-2">
                <label className="text-sm font-medium">Title</label>
                <input
                  type="text"
                  required
                  className="w-full rounded-md border bg-background p-2 text-sm"
                  placeholder="e.g. ISO 27001 Surveillance Audit 2026"
                  value={form.title}
                  onChange={(e) => setForm({ ...form, title: e.target.value })}
                />
              </div>
              <div>
                <label className="text-sm font-medium">Audit Type</label>
                <select
                  className="w-full rounded-md border bg-background p-2 text-sm"
                  value={form.audit_type}
                  onChange={(e) => setForm({ ...form, audit_type: e.target.value })}
                >
                  <option value="internal">Internal</option>
                  <option value="external">External</option>
                  <option value="readiness">Readiness</option>
                </select>
              </div>
              <div>
                <label className="text-sm font-medium">Framework</label>
                <select
                  className="w-full rounded-md border bg-background p-2 text-sm"
                  value={form.framework_id}
                  onChange={(e) => setForm({ ...form, framework_id: e.target.value })}
                >
                  <option value="">None</option>
                  {frameworks?.map((fw) => (
                    <option key={fw.id} value={fw.id}>
                      {fw.name}
                    </option>
                  ))}
                </select>
              </div>
              <div className="sm:col-span-2">
                <label className="text-sm font-medium">Auditor Firm</label>
                <input
                  type="text"
                  className="w-full rounded-md border bg-background p-2 text-sm"
                  placeholder="e.g. Deloitte, PwC (optional)"
                  value={form.auditor_firm}
                  onChange={(e) => setForm({ ...form, auditor_firm: e.target.value })}
                />
              </div>
            </div>
            <div className="mt-4 flex gap-2 justify-end">
              <Button
                variant="outline"
                onClick={() => {
                  setShowCreate(false);
                  resetForm();
                }}
              >
                Cancel
              </Button>
              <Button onClick={handleCreate} disabled={createAudit.isPending || !form.title.trim()}>
                {createAudit.isPending && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
                Create Audit
              </Button>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Readiness gauge */}
      <ReadinessPanel />

      {/* Audit list */}
      {isLoading ? (
        <div className="space-y-3">
          {[1, 2, 3].map((i) => (
            <Skeleton key={i} className="h-24 w-full rounded-xl" />
          ))}
        </div>
      ) : audits.length > 0 ? (
        <div className="space-y-3">
          {audits.map((audit) => (
            <Link key={audit.id} href={`/audits/${audit.id}`}>
              <Card className="transition-colors hover:bg-muted/50 cursor-pointer">
                <CardContent className="flex items-center gap-4 p-4">
                  <ClipboardCheck className="h-8 w-8 text-muted-foreground shrink-0" />
                  <div className="flex-1 min-w-0">
                    <div className="font-medium">{audit.title}</div>
                    <div className="mt-1 flex flex-wrap items-center gap-2 text-sm text-muted-foreground">
                      {audit.auditor_firm && (
                        <span>{audit.auditor_firm}</span>
                      )}
                      {audit.scheduled_start && audit.scheduled_end && (
                        <span>
                          {new Date(audit.scheduled_start).toLocaleDateString()} &ndash;{" "}
                          {new Date(audit.scheduled_end).toLocaleDateString()}
                        </span>
                      )}
                      {audit.readiness_score != null && (
                        <span>Readiness: {Math.round(audit.readiness_score)}%</span>
                      )}
                    </div>
                  </div>
                  <div className="flex items-center gap-2 shrink-0">
                    <Badge
                      variant={
                        (auditTypeBadgeVariant[audit.audit_type] ||
                          "outline") as any
                      }
                    >
                      {audit.audit_type}
                    </Badge>
                    <Badge
                      variant={
                        (statusColors[audit.status] || "secondary") as any
                      }
                    >
                      {audit.status}
                    </Badge>
                  </div>
                </CardContent>
              </Card>
            </Link>
          ))}
        </div>
      ) : (
        <Card>
          <CardContent className="p-12 text-center">
            <ClipboardCheck className="mx-auto h-12 w-12 text-muted-foreground" />
            <h3 className="mt-4 text-lg font-semibold">No audits yet</h3>
            <p className="mt-2 text-sm text-muted-foreground">
              Create your first audit to start tracking compliance readiness.
            </p>
          </CardContent>
        </Card>
      )}

      {data && data.total_pages > 1 && (
        <div className="flex justify-center gap-2 pt-4">
          <p className="text-sm text-muted-foreground">
            Page {data.page} of {data.total_pages} ({data.total} total)
          </p>
        </div>
      )}
    </div>
  );
}

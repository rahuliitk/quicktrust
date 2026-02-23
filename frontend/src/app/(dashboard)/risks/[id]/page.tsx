"use client";

import { useState } from "react";
import Link from "next/link";
import { useParams, useRouter } from "next/navigation";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Skeleton } from "@/components/ui/skeleton";
import { useRisk, useUpdateRisk, useDeleteRisk } from "@/hooks/use-api";
import { ArrowLeft, Shield, Pencil, Trash2, Loader2, Save, X } from "lucide-react";
import type { RiskLevel, RiskStatus } from "@/lib/types";

const DEMO_ORG_ID = "00000000-0000-0000-0000-000000000000";

const riskLevelColor: Record<RiskLevel, string> = {
  critical: "bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-100",
  high: "bg-orange-100 text-orange-800 dark:bg-orange-900 dark:text-orange-100",
  medium: "bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-100",
  low: "bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-100",
};

const statusLabels: Record<string, string> = {
  identified: "Identified - Risk has been logged",
  assessed: "Assessed - Likelihood and impact scored",
  treating: "Treating - Mitigation in progress",
  accepted: "Accepted - Risk formally accepted",
  closed: "Closed - Risk resolved or no longer applicable",
};

const treatmentTypeLabels: Record<string, string> = {
  mitigate: "Mitigate",
  transfer: "Transfer",
  accept: "Accept",
  avoid: "Avoid",
};

const treatmentStatusLabels: Record<string, string> = {
  not_started: "Not Started",
  in_progress: "In Progress",
  completed: "Completed",
  overdue: "Overdue",
};

function ScoreCell({ label, value }: { label: string; value: number | string }) {
  return (
    <div className="text-center">
      <div className="text-sm font-medium text-muted-foreground">{label}</div>
      <div className="mt-1 text-2xl font-bold">{value}</div>
    </div>
  );
}

interface EditFormState {
  status: string;
  likelihood: number;
  impact: number;
  treatment_type: string;
  treatment_plan: string;
}

export default function RiskDetailPage() {
  const params = useParams();
  const router = useRouter();
  const riskId = params.id as string;
  const { data: risk, isLoading } = useRisk(DEMO_ORG_ID, riskId);
  const updateRisk = useUpdateRisk(DEMO_ORG_ID);
  const deleteRisk = useDeleteRisk(DEMO_ORG_ID);

  const [editing, setEditing] = useState(false);
  const [form, setForm] = useState<EditFormState>({
    status: "",
    likelihood: 1,
    impact: 1,
    treatment_type: "",
    treatment_plan: "",
  });

  function enterEditMode() {
    if (!risk) return;
    setForm({
      status: risk.status,
      likelihood: risk.likelihood,
      impact: risk.impact,
      treatment_type: risk.treatment_type || "",
      treatment_plan: risk.treatment_plan || "",
    });
    setEditing(true);
  }

  function handleSave() {
    if (!risk) return;
    updateRisk.mutate(
      {
        riskId: risk.id,
        status: form.status as RiskStatus,
        likelihood: form.likelihood,
        impact: form.impact,
        treatment_type: form.treatment_type || null,
        treatment_plan: form.treatment_plan || null,
      },
      {
        onSuccess: () => {
          setEditing(false);
        },
      }
    );
  }

  function handleDelete() {
    if (!risk) return;
    const confirmed = window.confirm(
      `Are you sure you want to delete the risk "${risk.title}"? This action cannot be undone.`
    );
    if (!confirmed) return;
    deleteRisk.mutate(risk.id, {
      onSuccess: () => {
        router.push("/risks");
      },
    });
  }

  if (isLoading) {
    return (
      <div className="space-y-4">
        <Skeleton className="h-6 w-32" />
        <Skeleton className="h-10 w-64" />
        <Skeleton className="h-64 w-full" />
      </div>
    );
  }

  if (!risk) return <p>Risk not found.</p>;

  const hasResidualScoring =
    risk.residual_likelihood != null &&
    risk.residual_impact != null &&
    risk.residual_score != null;

  const hasTreatment =
    risk.treatment_type || risk.treatment_plan || risk.treatment_status;

  return (
    <div className="space-y-6">
      {/* Back link */}
      <Link
        href="/risks"
        className="inline-flex items-center gap-1 text-sm text-muted-foreground hover:text-foreground transition-colors"
      >
        <ArrowLeft className="h-4 w-4" />
        Back to Risk Register
      </Link>

      {/* Header */}
      <div>
        <div className="flex items-center gap-3">
          <h1 className="text-3xl font-bold">{risk.title}</h1>
          <Badge className={riskLevelColor[risk.risk_level]}>
            {risk.risk_level}
          </Badge>
          <Badge variant="outline" className="capitalize">
            {risk.category}
          </Badge>
          <div className="ml-auto flex items-center gap-2">
            {!editing && (
              <Button variant="outline" size="sm" onClick={enterEditMode}>
                <Pencil className="mr-1 h-4 w-4" />
                Edit
              </Button>
            )}
            <Button
              variant="destructive"
              size="sm"
              onClick={handleDelete}
              disabled={deleteRisk.isPending}
            >
              {deleteRisk.isPending ? (
                <Loader2 className="mr-1 h-4 w-4 animate-spin" />
              ) : (
                <Trash2 className="mr-1 h-4 w-4" />
              )}
              Delete
            </Button>
          </div>
        </div>
        <p className="mt-1 text-muted-foreground">
          Created {new Date(risk.created_at).toLocaleDateString()}
          {risk.last_review_date &&
            ` \u00b7 Last reviewed ${new Date(risk.last_review_date).toLocaleDateString()}`}
          {risk.next_review_date &&
            ` \u00b7 Next review ${new Date(risk.next_review_date).toLocaleDateString()}`}
        </p>
      </div>

      {/* Edit Form */}
      {editing && (
        <Card>
          <CardHeader>
            <CardTitle>Edit Risk</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
              {/* Status */}
              <div>
                <label className="text-sm font-medium">Status</label>
                <select
                  className="mt-1 w-full rounded-md border bg-background p-2 text-sm"
                  value={form.status}
                  onChange={(e) => setForm({ ...form, status: e.target.value })}
                >
                  <option value="identified">Identified</option>
                  <option value="assessed">Assessed</option>
                  <option value="treating">Treating</option>
                  <option value="accepted">Accepted</option>
                  <option value="closed">Closed</option>
                </select>
              </div>

              {/* Likelihood */}
              <div>
                <label className="text-sm font-medium">Likelihood (1-5)</label>
                <select
                  className="mt-1 w-full rounded-md border bg-background p-2 text-sm"
                  value={form.likelihood}
                  onChange={(e) =>
                    setForm({ ...form, likelihood: Number(e.target.value) })
                  }
                >
                  {[1, 2, 3, 4, 5].map((n) => (
                    <option key={n} value={n}>
                      {n}
                    </option>
                  ))}
                </select>
              </div>

              {/* Impact */}
              <div>
                <label className="text-sm font-medium">Impact (1-5)</label>
                <select
                  className="mt-1 w-full rounded-md border bg-background p-2 text-sm"
                  value={form.impact}
                  onChange={(e) =>
                    setForm({ ...form, impact: Number(e.target.value) })
                  }
                >
                  {[1, 2, 3, 4, 5].map((n) => (
                    <option key={n} value={n}>
                      {n}
                    </option>
                  ))}
                </select>
              </div>

              {/* Treatment Type */}
              <div>
                <label className="text-sm font-medium">Treatment Type</label>
                <select
                  className="mt-1 w-full rounded-md border bg-background p-2 text-sm"
                  value={form.treatment_type}
                  onChange={(e) =>
                    setForm({ ...form, treatment_type: e.target.value })
                  }
                >
                  <option value="">None</option>
                  <option value="mitigate">Mitigate</option>
                  <option value="transfer">Transfer</option>
                  <option value="accept">Accept</option>
                  <option value="avoid">Avoid</option>
                </select>
              </div>

              {/* Treatment Plan - full width */}
              <div className="sm:col-span-2">
                <label className="text-sm font-medium">Treatment Plan</label>
                <textarea
                  className="mt-1 w-full rounded-md border bg-background p-2 text-sm"
                  rows={4}
                  value={form.treatment_plan}
                  onChange={(e) =>
                    setForm({ ...form, treatment_plan: e.target.value })
                  }
                  placeholder="Describe the treatment plan..."
                />
              </div>
            </div>

            {/* Save / Cancel */}
            <div className="mt-4 flex items-center gap-2">
              <Button
                size="sm"
                onClick={handleSave}
                disabled={updateRisk.isPending}
              >
                {updateRisk.isPending ? (
                  <Loader2 className="mr-1 h-4 w-4 animate-spin" />
                ) : (
                  <Save className="mr-1 h-4 w-4" />
                )}
                Save
              </Button>
              <Button
                variant="outline"
                size="sm"
                onClick={() => setEditing(false)}
                disabled={updateRisk.isPending}
              >
                <X className="mr-1 h-4 w-4" />
                Cancel
              </Button>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Description */}
      {risk.description && (
        <Card>
          <CardHeader>
            <CardTitle>Description</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="whitespace-pre-wrap">{risk.description}</p>
          </CardContent>
        </Card>
      )}

      {/* Scoring panel */}
      <Card>
        <CardHeader>
          <CardTitle>Risk Scoring</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex items-center justify-center gap-8">
            <ScoreCell label="Likelihood" value={risk.likelihood} />
            <span className="text-2xl text-muted-foreground">&times;</span>
            <ScoreCell label="Impact" value={risk.impact} />
            <span className="text-2xl text-muted-foreground">=</span>
            <ScoreCell label="Risk Score" value={risk.risk_score} />
            <div className="text-center">
              <div className="text-sm font-medium text-muted-foreground">
                Risk Level
              </div>
              <div className="mt-1">
                <Badge className={`text-sm px-3 py-1 ${riskLevelColor[risk.risk_level]}`}>
                  {risk.risk_level}
                </Badge>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Status */}
      <Card>
        <CardHeader>
          <CardTitle>Status</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex items-center gap-3">
            <Badge variant="default" className="capitalize text-sm px-3 py-1">
              {risk.status}
            </Badge>
            <span className="text-sm text-muted-foreground">
              {statusLabels[risk.status] || risk.status}
            </span>
          </div>
        </CardContent>
      </Card>

      {/* Treatment */}
      {hasTreatment && (
        <Card>
          <CardHeader>
            <CardTitle>Treatment</CardTitle>
          </CardHeader>
          <CardContent>
            <dl className="grid grid-cols-2 gap-4 text-sm">
              {risk.treatment_type && (
                <div>
                  <dt className="font-medium text-muted-foreground">
                    Treatment Type
                  </dt>
                  <dd className="mt-1 capitalize">
                    {treatmentTypeLabels[risk.treatment_type] || risk.treatment_type}
                  </dd>
                </div>
              )}
              {risk.treatment_status && (
                <div>
                  <dt className="font-medium text-muted-foreground">
                    Treatment Status
                  </dt>
                  <dd className="mt-1">
                    <Badge
                      variant={
                        risk.treatment_status === "completed"
                          ? "success"
                          : risk.treatment_status === "overdue"
                          ? "destructive"
                          : "secondary"
                      }
                    >
                      {treatmentStatusLabels[risk.treatment_status] || risk.treatment_status}
                    </Badge>
                  </dd>
                </div>
              )}
              {risk.treatment_due_date && (
                <div>
                  <dt className="font-medium text-muted-foreground">
                    Due Date
                  </dt>
                  <dd className="mt-1">
                    {new Date(risk.treatment_due_date).toLocaleDateString()}
                  </dd>
                </div>
              )}
            </dl>
            {risk.treatment_plan && (
              <div className="mt-4">
                <div className="text-sm font-medium text-muted-foreground mb-1">
                  Treatment Plan
                </div>
                <div className="rounded-md border bg-muted/50 p-3">
                  <p className="whitespace-pre-wrap text-sm">
                    {risk.treatment_plan}
                  </p>
                </div>
              </div>
            )}
          </CardContent>
        </Card>
      )}

      {/* Residual risk */}
      {hasResidualScoring && (
        <Card>
          <CardHeader>
            <CardTitle>Residual Risk</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="flex items-center justify-center gap-8">
              <ScoreCell
                label="Residual Likelihood"
                value={risk.residual_likelihood!}
              />
              <span className="text-2xl text-muted-foreground">&times;</span>
              <ScoreCell
                label="Residual Impact"
                value={risk.residual_impact!}
              />
              <span className="text-2xl text-muted-foreground">=</span>
              <ScoreCell
                label="Residual Score"
                value={risk.residual_score!}
              />
            </div>
          </CardContent>
        </Card>
      )}

      {/* Linked controls */}
      <Card>
        <CardHeader>
          <CardTitle>Linked Controls</CardTitle>
        </CardHeader>
        <CardContent>
          {risk.control_mappings && risk.control_mappings.length > 0 ? (
            <div className="space-y-3">
              {risk.control_mappings.map((mapping) => (
                <div
                  key={mapping.id}
                  className="flex items-center gap-4 rounded-lg border p-3"
                >
                  <Shield className="h-5 w-5 text-muted-foreground shrink-0" />
                  <div className="flex-1 min-w-0">
                    <Link
                      href={`/controls/${mapping.control_id}`}
                      className="text-sm font-medium hover:underline"
                    >
                      Control {mapping.control_id.slice(0, 8)}...
                    </Link>
                    {mapping.notes && (
                      <p className="text-xs text-muted-foreground mt-0.5">
                        {mapping.notes}
                      </p>
                    )}
                  </div>
                  <Badge
                    variant={
                      mapping.effectiveness === "effective"
                        ? "success"
                        : mapping.effectiveness === "ineffective"
                        ? "destructive"
                        : "secondary"
                    }
                    className="capitalize"
                  >
                    {mapping.effectiveness}
                  </Badge>
                </div>
              ))}
            </div>
          ) : (
            <div className="flex flex-col items-center justify-center py-6 text-center">
              <Shield className="h-10 w-10 text-muted-foreground mb-3" />
              <p className="text-sm text-muted-foreground">
                No controls linked to this risk.
              </p>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}

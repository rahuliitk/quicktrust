"use client";

import { useState } from "react";
import Link from "next/link";
import { useParams, useRouter } from "next/navigation";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Skeleton } from "@/components/ui/skeleton";
import {
  useMonitorRule,
  useUpdateMonitorRule,
  useDeleteMonitorRule,
  useMonitorAlerts,
} from "@/hooks/use-api";
import {
  ArrowLeft,
  Pencil,
  Trash2,
  Loader2,
  Save,
  X,
  Activity,
  Bell,
} from "lucide-react";

const DEMO_ORG_ID = "00000000-0000-0000-0000-000000000000";

const severityColor: Record<string, string> = {
  critical: "bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-100",
  high: "bg-orange-100 text-orange-800 dark:bg-orange-900 dark:text-orange-100",
  medium:
    "bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-100",
  low: "bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-100",
};

const alertStatusColor: Record<string, string> = {
  open: "bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-100",
  acknowledged:
    "bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-100",
  resolved:
    "bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-100",
};

export default function MonitorRuleDetailPage() {
  const params = useParams();
  const router = useRouter();
  const ruleId = params.id as string;

  const { data: rule, isLoading } = useMonitorRule(DEMO_ORG_ID, ruleId);
  const { data: alertsData, isLoading: alertsLoading } = useMonitorAlerts(
    DEMO_ORG_ID,
    { rule_id: ruleId }
  );
  const updateRule = useUpdateMonitorRule(DEMO_ORG_ID);
  const deleteRule = useDeleteMonitorRule(DEMO_ORG_ID);

  const [editing, setEditing] = useState(false);
  const [form, setForm] = useState({
    title: "",
    check_type: "",
    schedule: "",
    is_active: true,
    description: "",
  });

  function enterEditMode() {
    if (!rule) return;
    setForm({
      title: rule.title || "",
      check_type: rule.check_type || "policy",
      schedule: rule.schedule || "daily",
      is_active: rule.is_active ?? true,
      description: rule.description || "",
    });
    setEditing(true);
  }

  function handleSave() {
    if (!rule) return;
    updateRule.mutate(
      { ruleId: rule.id, ...form },
      { onSuccess: () => setEditing(false) }
    );
  }

  function handleDelete() {
    if (!rule) return;
    const confirmed = window.confirm(
      `Are you sure you want to delete "${rule.title}"? This action cannot be undone.`
    );
    if (!confirmed) return;
    deleteRule.mutate(rule.id, {
      onSuccess: () => router.push("/monitoring"),
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

  if (!rule) return <p>Monitoring rule not found.</p>;

  const alerts = alertsData?.items || [];

  return (
    <div className="space-y-6">
      <Link
        href="/monitoring"
        className="inline-flex items-center gap-1 text-sm text-muted-foreground hover:text-foreground transition-colors"
      >
        <ArrowLeft className="h-4 w-4" />
        Back to Monitoring
      </Link>

      {/* Header */}
      <div className="flex items-center gap-3">
        <h1 className="text-3xl font-bold">{rule.title}</h1>
        <Badge variant={rule.is_active ? "success" : "secondary"}>
          {rule.is_active ? "Active" : "Inactive"}
        </Badge>
        <Badge variant="outline" className="capitalize">
          {rule.check_type}
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
            disabled={deleteRule.isPending}
          >
            {deleteRule.isPending ? (
              <Loader2 className="mr-1 h-4 w-4 animate-spin" />
            ) : (
              <Trash2 className="mr-1 h-4 w-4" />
            )}
            Delete
          </Button>
        </div>
      </div>

      {/* Edit Form */}
      {editing && (
        <Card>
          <CardHeader>
            <CardTitle>Edit Rule</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div>
              <label className="text-sm font-medium">Title</label>
              <input
                type="text"
                className="mt-1 w-full rounded-md border bg-background p-2 text-sm"
                value={form.title}
                onChange={(e) => setForm({ ...form, title: e.target.value })}
              />
            </div>

            <div>
              <label className="text-sm font-medium">Description</label>
              <textarea
                className="mt-1 w-full rounded-md border bg-background p-2 text-sm"
                rows={3}
                value={form.description}
                onChange={(e) =>
                  setForm({ ...form, description: e.target.value })
                }
              />
            </div>

            <div className="grid grid-cols-3 gap-4">
              <div>
                <label className="text-sm font-medium">Check Type</label>
                <select
                  className="mt-1 w-full rounded-md border bg-background p-2 text-sm"
                  value={form.check_type}
                  onChange={(e) =>
                    setForm({ ...form, check_type: e.target.value })
                  }
                >
                  <option value="policy">Policy</option>
                  <option value="access">Access</option>
                  <option value="configuration">Configuration</option>
                  <option value="vulnerability">Vulnerability</option>
                </select>
              </div>

              <div>
                <label className="text-sm font-medium">Schedule</label>
                <select
                  className="mt-1 w-full rounded-md border bg-background p-2 text-sm"
                  value={form.schedule}
                  onChange={(e) =>
                    setForm({ ...form, schedule: e.target.value })
                  }
                >
                  <option value="hourly">Hourly</option>
                  <option value="daily">Daily</option>
                  <option value="weekly">Weekly</option>
                  <option value="monthly">Monthly</option>
                </select>
              </div>

              <div>
                <label className="text-sm font-medium">Active</label>
                <div className="flex items-center gap-2 mt-2">
                  <input
                    type="checkbox"
                    checked={form.is_active}
                    onChange={(e) =>
                      setForm({ ...form, is_active: e.target.checked })
                    }
                    className="h-4 w-4 rounded border"
                  />
                  <span className="text-sm">Enabled</span>
                </div>
              </div>
            </div>

            <div className="flex items-center gap-2">
              <Button
                size="sm"
                onClick={handleSave}
                disabled={updateRule.isPending}
              >
                {updateRule.isPending ? (
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
                disabled={updateRule.isPending}
              >
                <X className="mr-1 h-4 w-4" />
                Cancel
              </Button>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Rule Details */}
      {!editing && (
        <div className="grid gap-6 md:grid-cols-2">
          <Card>
            <CardHeader>
              <CardTitle>Rule Details</CardTitle>
            </CardHeader>
            <CardContent>
              <dl className="space-y-3 text-sm">
                <div>
                  <dt className="font-medium text-muted-foreground">
                    Check Type
                  </dt>
                  <dd className="mt-1 capitalize">{rule.check_type}</dd>
                </div>
                <div>
                  <dt className="font-medium text-muted-foreground">
                    Schedule
                  </dt>
                  <dd className="mt-1 capitalize">{rule.schedule}</dd>
                </div>
                {rule.description && (
                  <div>
                    <dt className="font-medium text-muted-foreground">
                      Description
                    </dt>
                    <dd className="mt-1">{rule.description}</dd>
                  </div>
                )}
                <div>
                  <dt className="font-medium text-muted-foreground">
                    Created
                  </dt>
                  <dd className="mt-1">
                    {new Date(rule.created_at).toLocaleDateString()}
                  </dd>
                </div>
              </dl>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Configuration</CardTitle>
            </CardHeader>
            <CardContent>
              {rule.config ? (
                <pre className="rounded-md border bg-muted p-3 text-xs overflow-auto max-h-48">
                  {JSON.stringify(rule.config, null, 2)}
                </pre>
              ) : (
                <p className="text-sm text-muted-foreground">
                  No custom configuration set.
                </p>
              )}
              {rule.last_run_at && (
                <div className="mt-4 text-sm">
                  <span className="font-medium text-muted-foreground">
                    Last Run:{" "}
                  </span>
                  {new Date(rule.last_run_at).toLocaleString()}
                </div>
              )}
            </CardContent>
          </Card>
        </div>
      )}

      {/* Alert History */}
      <Card>
        <CardHeader>
          <CardTitle>
            Alert History {alerts.length > 0 && `(${alerts.length})`}
          </CardTitle>
        </CardHeader>
        <CardContent>
          {alertsLoading ? (
            <div className="space-y-3">
              {[1, 2, 3].map((i) => (
                <Skeleton key={i} className="h-16 w-full rounded-lg" />
              ))}
            </div>
          ) : alerts.length > 0 ? (
            <div className="space-y-3">
              {alerts.map((alert: any) => (
                <div
                  key={alert.id}
                  className="flex items-center gap-4 rounded-lg border p-3"
                >
                  <Bell className="h-5 w-5 text-muted-foreground shrink-0" />
                  <div className="flex-1 min-w-0">
                    <div className="text-sm font-medium">
                      {alert.title || alert.message}
                    </div>
                    <div className="mt-1 text-xs text-muted-foreground">
                      {alert.created_at &&
                        new Date(alert.created_at).toLocaleString()}
                    </div>
                  </div>
                  <Badge
                    className={severityColor[alert.severity] || ""}
                  >
                    {alert.severity}
                  </Badge>
                  <Badge
                    className={alertStatusColor[alert.status] || ""}
                  >
                    {alert.status}
                  </Badge>
                </div>
              ))}
            </div>
          ) : (
            <div className="flex flex-col items-center justify-center py-6 text-center">
              <Activity className="h-10 w-10 text-muted-foreground mb-3" />
              <p className="text-sm text-muted-foreground">
                No alerts generated by this rule yet.
              </p>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}

"use client";

import { useState } from "react";
import Link from "next/link";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Skeleton } from "@/components/ui/skeleton";
import {
  useMonitorRules,
  useCreateMonitorRule,
  useRunMonitorRule,
  useMonitorAlerts,
  useUpdateMonitorAlert,
  useMonitoringStats,
} from "@/hooks/use-api";
import {
  Activity,
  Bell,
  Plus,
  Loader2,
  Play,
  CheckCircle,
  Eye,
} from "lucide-react";
import { useOrgId } from "@/hooks/use-org-id";

type TabValue = "rules" | "alerts";

const CHECK_TYPE_FILTERS: { label: string; value: string | undefined }[] = [
  { label: "All", value: undefined },
  { label: "Policy", value: "policy" },
  { label: "Access", value: "access" },
  { label: "Configuration", value: "configuration" },
  { label: "Vulnerability", value: "vulnerability" },
];

const ALERT_STATUS_FILTERS: { label: string; value: string | undefined }[] = [
  { label: "All", value: undefined },
  { label: "Open", value: "open" },
  { label: "Acknowledged", value: "acknowledged" },
  { label: "Resolved", value: "resolved" },
];

const ALERT_SEVERITY_FILTERS: { label: string; value: string | undefined }[] = [
  { label: "All", value: undefined },
  { label: "Critical", value: "critical" },
  { label: "High", value: "high" },
  { label: "Medium", value: "medium" },
  { label: "Low", value: "low" },
];

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

export default function MonitoringPage() {
  const orgId = useOrgId();
  const [activeTab, setActiveTab] = useState<TabValue>("rules");
  const [checkTypeFilter, setCheckTypeFilter] = useState<string | undefined>(
    undefined
  );
  const [activeFilter, setActiveFilter] = useState<string | undefined>(
    undefined
  );
  const [alertStatusFilter, setAlertStatusFilter] = useState<
    string | undefined
  >(undefined);
  const [alertSeverityFilter, setAlertSeverityFilter] = useState<
    string | undefined
  >(undefined);

  const { data: rulesData, isLoading: rulesLoading } = useMonitorRules(
    orgId,
    { check_type: checkTypeFilter, is_active: activeFilter }
  );
  const { data: alertsData, isLoading: alertsLoading } = useMonitorAlerts(
    orgId,
    { status: alertStatusFilter, severity: alertSeverityFilter }
  );
  const { data: stats } = useMonitoringStats(orgId);

  const [showCreate, setShowCreate] = useState(false);
  const [form, setForm] = useState({
    title: "",
    check_type: "policy",
    schedule: "daily",
    is_active: true,
  });
  const createRule = useCreateMonitorRule(orgId);
  const runRule = useRunMonitorRule(orgId);
  const updateAlert = useUpdateMonitorAlert(orgId);

  const resetForm = () =>
    setForm({ title: "", check_type: "policy", schedule: "daily", is_active: true });

  const handleCreate = () => {
    createRule.mutate(form, {
      onSuccess: () => {
        setShowCreate(false);
        resetForm();
      },
    });
  };

  const rules = rulesData?.items || [];
  const alerts = alertsData?.items || [];

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold">Continuous Monitoring</h1>
          <p className="text-muted-foreground">
            Monitor compliance rules and manage alerts
          </p>
        </div>
      </div>

      {/* Stats */}
      {stats && (
        <div className="grid grid-cols-4 gap-4">
          {[
            { label: "Total Rules", value: stats.total_rules ?? 0 },
            { label: "Active Rules", value: stats.active_rules ?? 0 },
            { label: "Open Alerts", value: stats.open_alerts ?? 0 },
            { label: "Critical", value: stats.by_severity?.critical ?? 0 },
          ].map((s) => (
            <Card key={s.label}>
              <CardContent className="p-4 text-center">
                <div className="text-2xl font-bold">{s.value}</div>
                <div className="text-xs text-muted-foreground">{s.label}</div>
              </CardContent>
            </Card>
          ))}
        </div>
      )}

      {/* Tab buttons */}
      <div className="flex gap-2 border-b pb-1">
        <Button
          variant={activeTab === "rules" ? "default" : "ghost"}
          size="sm"
          onClick={() => setActiveTab("rules")}
          className="gap-1.5"
        >
          <Activity className="h-4 w-4" />
          Rules
        </Button>
        <Button
          variant={activeTab === "alerts" ? "default" : "ghost"}
          size="sm"
          onClick={() => setActiveTab("alerts")}
          className="gap-1.5"
        >
          <Bell className="h-4 w-4" />
          Alerts
        </Button>
      </div>

      {/* Rules Tab */}
      {activeTab === "rules" && (
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <div className="flex flex-wrap gap-2">
              {CHECK_TYPE_FILTERS.map((f) => (
                <Button
                  key={f.label}
                  variant={
                    checkTypeFilter === f.value ? "default" : "outline"
                  }
                  size="sm"
                  onClick={() => setCheckTypeFilter(f.value)}
                >
                  {f.label}
                </Button>
              ))}
              <span className="mx-2 border-l" />
              <Button
                variant={activeFilter === undefined ? "default" : "outline"}
                size="sm"
                onClick={() => setActiveFilter(undefined)}
              >
                All
              </Button>
              <Button
                variant={activeFilter === "true" ? "default" : "outline"}
                size="sm"
                onClick={() => setActiveFilter("true")}
              >
                Active
              </Button>
              <Button
                variant={activeFilter === "false" ? "default" : "outline"}
                size="sm"
                onClick={() => setActiveFilter("false")}
              >
                Inactive
              </Button>
            </div>
            <Button
              size="sm"
              onClick={() => setShowCreate((v) => !v)}
              className="gap-1.5"
            >
              <Plus className="h-4 w-4" />
              New Rule
            </Button>
          </div>

          {showCreate && (
            <Card>
              <CardContent className="p-4 space-y-4">
                <h2 className="text-lg font-semibold">Create Monitoring Rule</h2>

                <div className="space-y-1">
                  <label className="text-sm font-medium">Title</label>
                  <input
                    type="text"
                    required
                    className="w-full rounded-md border bg-background p-2 text-sm"
                    placeholder="Rule title"
                    value={form.title}
                    onChange={(e) =>
                      setForm({ ...form, title: e.target.value })
                    }
                  />
                </div>

                <div className="grid grid-cols-3 gap-4">
                  <div className="space-y-1">
                    <label className="text-sm font-medium">Check Type</label>
                    <select
                      className="w-full rounded-md border bg-background p-2 text-sm"
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

                  <div className="space-y-1">
                    <label className="text-sm font-medium">Schedule</label>
                    <select
                      className="w-full rounded-md border bg-background p-2 text-sm"
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

                  <div className="space-y-1">
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
                      <span className="text-sm">Enable rule</span>
                    </div>
                  </div>
                </div>

                <div className="flex items-center gap-2 pt-2">
                  <Button
                    onClick={handleCreate}
                    disabled={!form.title.trim() || createRule.isPending}
                  >
                    {createRule.isPending && (
                      <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                    )}
                    Create Rule
                  </Button>
                  <Button
                    variant="outline"
                    onClick={() => {
                      setShowCreate(false);
                      resetForm();
                    }}
                  >
                    Cancel
                  </Button>
                </div>
              </CardContent>
            </Card>
          )}

          {rulesLoading ? (
            <div className="space-y-3">
              {[1, 2, 3].map((i) => (
                <Skeleton key={i} className="h-24 w-full rounded-xl" />
              ))}
            </div>
          ) : rules.length > 0 ? (
            <div className="space-y-3">
              {rules.map((rule: any) => (
                <Card
                  key={rule.id}
                  className="transition-colors hover:bg-accent/50"
                >
                  <CardContent className="flex items-center gap-4 p-4">
                    <Activity className="h-8 w-8 text-muted-foreground shrink-0" />
                    <Link
                      href={`/monitoring/${rule.id}`}
                      className="flex-1 min-w-0"
                    >
                      <div className="font-medium">{rule.title}</div>
                      <div className="mt-1 text-xs text-muted-foreground">
                        {rule.check_type?.replace(/_/g, " ")} &middot;{" "}
                        {rule.schedule}
                        {rule.last_run_at && (
                          <>
                            {" "}
                            &middot; Last run:{" "}
                            {new Date(
                              rule.last_run_at
                            ).toLocaleString()}
                          </>
                        )}
                      </div>
                    </Link>
                    <Badge
                      variant={rule.is_active ? "success" : "secondary"}
                    >
                      {rule.is_active ? "Active" : "Inactive"}
                    </Badge>
                    <Badge variant="outline" className="capitalize">
                      {rule.check_type}
                    </Badge>
                    <Button
                      size="sm"
                      variant="outline"
                      className="gap-1"
                      onClick={() => runRule.mutate(rule.id)}
                      disabled={runRule.isPending}
                    >
                      <Play className="h-3 w-3" />
                      Run Now
                    </Button>
                  </CardContent>
                </Card>
              ))}
            </div>
          ) : (
            <Card>
              <CardContent className="flex flex-col items-center justify-center p-12 text-center">
                <Activity className="h-12 w-12 text-muted-foreground mb-4" />
                <h3 className="text-lg font-medium">No rules found</h3>
                <p className="text-sm text-muted-foreground mt-1">
                  Create monitoring rules to continuously check compliance.
                </p>
              </CardContent>
            </Card>
          )}
        </div>
      )}

      {/* Alerts Tab */}
      {activeTab === "alerts" && (
        <div className="space-y-4">
          <div className="space-y-3">
            <div className="flex flex-wrap gap-2">
              <span className="flex items-center text-sm text-muted-foreground mr-1">
                Status:
              </span>
              {ALERT_STATUS_FILTERS.map((f) => (
                <Button
                  key={f.label}
                  variant={
                    alertStatusFilter === f.value ? "default" : "outline"
                  }
                  size="sm"
                  onClick={() => setAlertStatusFilter(f.value)}
                >
                  {f.label}
                </Button>
              ))}
            </div>
            <div className="flex flex-wrap gap-2">
              <span className="flex items-center text-sm text-muted-foreground mr-1">
                Severity:
              </span>
              {ALERT_SEVERITY_FILTERS.map((f) => (
                <Button
                  key={f.label}
                  variant={
                    alertSeverityFilter === f.value ? "default" : "outline"
                  }
                  size="sm"
                  onClick={() => setAlertSeverityFilter(f.value)}
                >
                  {f.label}
                </Button>
              ))}
            </div>
          </div>

          {alertsLoading ? (
            <div className="space-y-3">
              {[1, 2, 3].map((i) => (
                <Skeleton key={i} className="h-20 w-full rounded-xl" />
              ))}
            </div>
          ) : alerts.length > 0 ? (
            <div className="space-y-3">
              {alerts.map((alert: any) => (
                <Card key={alert.id}>
                  <CardContent className="flex items-center gap-4 p-4">
                    <Bell className="h-6 w-6 text-muted-foreground shrink-0" />
                    <div className="flex-1 min-w-0">
                      <div className="text-sm font-medium">
                        {alert.title || alert.message}
                      </div>
                      <div className="mt-1 text-xs text-muted-foreground">
                        {alert.created_at &&
                          new Date(alert.created_at).toLocaleString()}
                        {alert.rule_id && (
                          <span>
                            {" "}
                            &middot; Rule: {alert.rule_id.slice(0, 8)}...
                          </span>
                        )}
                      </div>
                    </div>
                    <Badge
                      className={severityColor[alert.severity] || ""}
                    >
                      {alert.severity}
                    </Badge>
                    <Badge
                      className={
                        alertStatusColor[alert.status] || ""
                      }
                    >
                      {alert.status}
                    </Badge>
                    {alert.status === "open" && (
                      <Button
                        size="sm"
                        variant="outline"
                        className="gap-1"
                        onClick={() =>
                          updateAlert.mutate({
                            alertId: alert.id,
                            status: "acknowledged",
                          })
                        }
                        disabled={updateAlert.isPending}
                      >
                        <Eye className="h-3 w-3" />
                        Acknowledge
                      </Button>
                    )}
                    {(alert.status === "open" ||
                      alert.status === "acknowledged") && (
                      <Button
                        size="sm"
                        variant="outline"
                        className="gap-1"
                        onClick={() =>
                          updateAlert.mutate({
                            alertId: alert.id,
                            status: "resolved",
                          })
                        }
                        disabled={updateAlert.isPending}
                      >
                        <CheckCircle className="h-3 w-3" />
                        Resolve
                      </Button>
                    )}
                  </CardContent>
                </Card>
              ))}
            </div>
          ) : (
            <Card>
              <CardContent className="flex flex-col items-center justify-center p-12 text-center">
                <Bell className="h-12 w-12 text-muted-foreground mb-4" />
                <h3 className="text-lg font-medium">No alerts found</h3>
                <p className="text-sm text-muted-foreground mt-1">
                  No alerts match the current filters.
                </p>
              </CardContent>
            </Card>
          )}
        </div>
      )}
    </div>
  );
}

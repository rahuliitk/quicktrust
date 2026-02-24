"use client";

import { useState } from "react";
import Link from "next/link";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Skeleton } from "@/components/ui/skeleton";
import {
  useIncidents,
  useIncidentStats,
  useCreateIncident,
} from "@/hooks/use-api";
import { useOrgId } from "@/hooks/use-org-id";
import { AlertOctagon, Plus, Loader2 } from "lucide-react";
import type { IncidentSeverity } from "@/lib/types";

const STATUS_FILTERS: { label: string; value: string | undefined }[] = [
  { label: "All", value: undefined },
  { label: "Open", value: "open" },
  { label: "Investigating", value: "investigating" },
  { label: "Resolved", value: "resolved" },
  { label: "Closed", value: "closed" },
];

const SEVERITY_FILTERS: { label: string; value: string | undefined }[] = [
  { label: "All", value: undefined },
  { label: "P1", value: "P1" },
  { label: "P2", value: "P2" },
  { label: "P3", value: "P3" },
  { label: "P4", value: "P4" },
];

const severityColor: Record<string, string> = {
  P1: "bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-100",
  P2: "bg-orange-100 text-orange-800 dark:bg-orange-900 dark:text-orange-100",
  P3: "bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-100",
  P4: "bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-100",
};

const statusColor: Record<string, string> = {
  open: "bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-100",
  investigating:
    "bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-100",
  resolved:
    "bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-100",
  closed: "bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-100",
};

export default function IncidentsPage() {
  const orgId = useOrgId();
  const [statusFilter, setStatusFilter] = useState<string | undefined>(
    undefined
  );
  const [severityFilter, setSeverityFilter] = useState<string | undefined>(
    undefined
  );
  const { data, isLoading } = useIncidents(orgId, {
    status: statusFilter,
    severity: severityFilter,
  });
  const { data: stats } = useIncidentStats(orgId);

  const [showCreate, setShowCreate] = useState(false);
  const [form, setForm] = useState({
    title: "",
    severity: "P3",
    category: "security",
    description: "",
  });
  const createIncident = useCreateIncident(orgId);

  const resetForm = () =>
    setForm({ title: "", severity: "P3", category: "security", description: "" });

  const handleCreate = () => {
    createIncident.mutate(
      { ...form, severity: form.severity as IncidentSeverity },
      {
        onSuccess: () => {
          setShowCreate(false);
          resetForm();
        },
      }
    );
  };

  const incidents = data?.items || [];

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold">Incidents</h1>
          <p className="text-muted-foreground">
            Track and manage security incidents
          </p>
        </div>
        <Button onClick={() => setShowCreate((v) => !v)}>
          <Plus className="mr-2 h-4 w-4" />
          New Incident
        </Button>
      </div>

      {/* Stats bar */}
      {stats && (
        <div className="grid grid-cols-4 gap-4">
          {[
            { label: "Open", value: stats.by_status?.open ?? 0 },
            { label: "Investigating", value: stats.by_status?.investigating ?? 0 },
            { label: "Resolved", value: stats.by_status?.resolved ?? 0 },
            { label: "Closed", value: stats.by_status?.closed ?? 0 },
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

      {showCreate && (
        <Card>
          <CardContent className="p-4 space-y-4">
            <h2 className="text-lg font-semibold">Create New Incident</h2>

            <div className="space-y-1">
              <label className="text-sm font-medium">Title</label>
              <input
                type="text"
                required
                className="w-full rounded-md border bg-background p-2 text-sm"
                placeholder="Incident title"
                value={form.title}
                onChange={(e) => setForm({ ...form, title: e.target.value })}
              />
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-1">
                <label className="text-sm font-medium">Severity</label>
                <select
                  className="w-full rounded-md border bg-background p-2 text-sm"
                  value={form.severity}
                  onChange={(e) =>
                    setForm({ ...form, severity: e.target.value })
                  }
                >
                  <option value="P1">P1 - Critical</option>
                  <option value="P2">P2 - High</option>
                  <option value="P3">P3 - Medium</option>
                  <option value="P4">P4 - Low</option>
                </select>
              </div>

              <div className="space-y-1">
                <label className="text-sm font-medium">Category</label>
                <input
                  type="text"
                  className="w-full rounded-md border bg-background p-2 text-sm"
                  placeholder="e.g. security, availability"
                  value={form.category}
                  onChange={(e) =>
                    setForm({ ...form, category: e.target.value })
                  }
                />
              </div>
            </div>

            <div className="space-y-1">
              <label className="text-sm font-medium">Description</label>
              <textarea
                className="w-full rounded-md border bg-background p-2 text-sm"
                placeholder="Describe the incident"
                rows={3}
                value={form.description}
                onChange={(e) =>
                  setForm({ ...form, description: e.target.value })
                }
              />
            </div>

            <div className="flex items-center gap-2 pt-2">
              <Button
                onClick={handleCreate}
                disabled={!form.title.trim() || createIncident.isPending}
              >
                {createIncident.isPending && (
                  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                )}
                Create Incident
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

      {/* Filters */}
      <div className="space-y-3">
        <div className="flex flex-wrap gap-2">
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

        <div className="flex flex-wrap gap-2">
          <span className="flex items-center text-sm text-muted-foreground mr-1">
            Severity:
          </span>
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
        </div>
      </div>

      {isLoading ? (
        <div className="space-y-3">
          {[1, 2, 3, 4, 5].map((i) => (
            <Skeleton key={i} className="h-24 w-full rounded-xl" />
          ))}
        </div>
      ) : incidents.length > 0 ? (
        <div className="space-y-3">
          {incidents.map((incident: any) => (
            <Link key={incident.id} href={`/incidents/${incident.id}`}>
              <Card className="transition-colors hover:bg-accent/50">
                <CardContent className="flex items-center gap-4 p-4">
                  <AlertOctagon className="h-8 w-8 text-muted-foreground shrink-0" />
                  <div className="flex-1 min-w-0">
                    <div className="font-medium">{incident.title}</div>
                    <div className="mt-1 text-xs text-muted-foreground">
                      {incident.category && (
                        <span className="capitalize">
                          {incident.category}
                        </span>
                      )}
                      {incident.created_at && (
                        <>
                          <span> &middot; </span>
                          <span>
                            Created{" "}
                            {new Date(incident.created_at).toLocaleDateString()}
                          </span>
                        </>
                      )}
                    </div>
                  </div>
                  <Badge className={severityColor[incident.severity] || ""}>
                    {incident.severity}
                  </Badge>
                  <Badge className={statusColor[incident.status] || ""}>
                    {incident.status}
                  </Badge>
                </CardContent>
              </Card>
            </Link>
          ))}
        </div>
      ) : (
        <Card>
          <CardContent className="flex flex-col items-center justify-center p-12 text-center">
            <AlertOctagon className="h-12 w-12 text-muted-foreground mb-4" />
            <h3 className="text-lg font-medium">No incidents found</h3>
            <p className="text-sm text-muted-foreground mt-1">
              No incidents match the current filters, or no incidents have been
              reported yet.
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

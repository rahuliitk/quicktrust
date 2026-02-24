"use client";

import { useState } from "react";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Skeleton } from "@/components/ui/skeleton";
import { useReports, useCreateReport, useReportStats } from "@/hooks/use-api";
import { useOrgId } from "@/hooks/use-org-id";
import {
  FileBarChart,
  Plus,
  Loader2,
  ExternalLink,
} from "lucide-react";

const TYPE_FILTERS: { label: string; value: string | undefined }[] = [
  { label: "All Types", value: undefined },
  { label: "Compliance Summary", value: "compliance_summary" },
  { label: "Risk Report", value: "risk_report" },
  { label: "Evidence Audit", value: "evidence_audit" },
  { label: "Training Completion", value: "training_completion" },
];

const STATUS_FILTERS: { label: string; value: string | undefined }[] = [
  { label: "All Status", value: undefined },
  { label: "Pending", value: "pending" },
  { label: "Generating", value: "generating" },
  { label: "Completed", value: "completed" },
  { label: "Failed", value: "failed" },
];

const statusColor: Record<string, string> = {
  pending: "bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-100",
  generating:
    "bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-100",
  completed:
    "bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-100",
  failed: "bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-100",
};

const typeColor: Record<string, string> = {
  compliance_summary:
    "bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-100",
  risk_report:
    "bg-orange-100 text-orange-800 dark:bg-orange-900 dark:text-orange-100",
  evidence_audit:
    "bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-100",
  training_completion:
    "bg-teal-100 text-teal-800 dark:bg-teal-900 dark:text-teal-100",
};

export default function ReportsPage() {
  const orgId = useOrgId();
  const [typeFilter, setTypeFilter] = useState<string | undefined>(undefined);
  const [statusFilter, setStatusFilter] = useState<string | undefined>(
    undefined
  );
  const { data, isLoading } = useReports(orgId, {
    report_type: typeFilter,
    status: statusFilter,
  });
  const { data: stats } = useReportStats(orgId);

  const [showCreate, setShowCreate] = useState(false);
  const [form, setForm] = useState({
    title: "",
    report_type: "compliance_summary",
    format: "json",
  });
  const createReport = useCreateReport(orgId);

  const resetForm = () =>
    setForm({ title: "", report_type: "compliance_summary", format: "json" });

  const handleCreate = () => {
    createReport.mutate(form, {
      onSuccess: () => {
        setShowCreate(false);
        resetForm();
      },
    });
  };

  const reports = data?.items || [];

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold">Reports</h1>
          <p className="text-muted-foreground">
            Generate and download compliance reports
          </p>
        </div>
        <Button onClick={() => setShowCreate((v) => !v)}>
          <Plus className="mr-2 h-4 w-4" />
          New Report
        </Button>
      </div>

      {/* Stats */}
      {stats && (
        <div className="grid grid-cols-4 gap-4">
          {[
            { label: "Total Reports", value: stats.total ?? 0 },
            { label: "Completed", value: stats.by_status?.completed ?? 0 },
            { label: "Pending", value: stats.by_status?.pending ?? 0 },
            { label: "Failed", value: stats.by_status?.failed ?? 0 },
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
            <h2 className="text-lg font-semibold">Generate New Report</h2>

            <div className="space-y-1">
              <label className="text-sm font-medium">Title</label>
              <input
                type="text"
                required
                className="w-full rounded-md border bg-background p-2 text-sm"
                placeholder="Report title"
                value={form.title}
                onChange={(e) => setForm({ ...form, title: e.target.value })}
              />
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-1">
                <label className="text-sm font-medium">Report Type</label>
                <select
                  className="w-full rounded-md border bg-background p-2 text-sm"
                  value={form.report_type}
                  onChange={(e) =>
                    setForm({ ...form, report_type: e.target.value })
                  }
                >
                  <option value="compliance_summary">
                    Compliance Summary
                  </option>
                  <option value="risk_report">Risk Report</option>
                  <option value="evidence_audit">Evidence Audit</option>
                  <option value="training_completion">
                    Training Completion
                  </option>
                </select>
              </div>

              <div className="space-y-1">
                <label className="text-sm font-medium">Format</label>
                <select
                  className="w-full rounded-md border bg-background p-2 text-sm"
                  value={form.format}
                  onChange={(e) =>
                    setForm({ ...form, format: e.target.value })
                  }
                >
                  <option value="json">JSON</option>
                  <option value="csv">CSV</option>
                  <option value="pdf">PDF</option>
                </select>
              </div>
            </div>

            <div className="flex items-center gap-2 pt-2">
              <Button
                onClick={handleCreate}
                disabled={!form.title.trim() || createReport.isPending}
              >
                {createReport.isPending && (
                  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                )}
                Generate Report
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
          {TYPE_FILTERS.map((f) => (
            <Button
              key={f.label}
              variant={typeFilter === f.value ? "default" : "outline"}
              size="sm"
              onClick={() => setTypeFilter(f.value)}
            >
              {f.label}
            </Button>
          ))}
        </div>
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
      </div>

      {isLoading ? (
        <div className="space-y-3">
          {[1, 2, 3].map((i) => (
            <Skeleton key={i} className="h-24 w-full rounded-xl" />
          ))}
        </div>
      ) : reports.length > 0 ? (
        <div className="space-y-3">
          {reports.map((report: any) => (
            <Card key={report.id}>
              <CardContent className="flex items-center gap-4 p-4">
                <FileBarChart className="h-8 w-8 text-muted-foreground shrink-0" />
                <div className="flex-1 min-w-0">
                  <div className="font-medium">{report.title}</div>
                  <div className="mt-1 text-xs text-muted-foreground">
                    {report.format && (
                      <span className="uppercase">{report.format}</span>
                    )}
                    {report.created_at && (
                      <>
                        <span> &middot; </span>
                        <span>
                          Created{" "}
                          {new Date(report.created_at).toLocaleDateString()}
                        </span>
                      </>
                    )}
                  </div>
                </div>
                <Badge
                  className={
                    typeColor[report.report_type] || ""
                  }
                >
                  {report.report_type?.replace(/_/g, " ")}
                </Badge>
                <Badge
                  className={statusColor[report.status] || ""}
                >
                  {report.status}
                </Badge>
                {report.status === "completed" && report.data_url && (
                  <a
                    href={report.data_url}
                    target="_blank"
                    rel="noopener noreferrer"
                  >
                    <Button size="sm" variant="outline" className="gap-1">
                      <ExternalLink className="h-3 w-3" />
                      View Data
                    </Button>
                  </a>
                )}
                {report.status === "completed" && !report.data_url && (
                  <Button size="sm" variant="outline" className="gap-1" disabled>
                    <ExternalLink className="h-3 w-3" />
                    View Data
                  </Button>
                )}
              </CardContent>
            </Card>
          ))}
        </div>
      ) : (
        <Card>
          <CardContent className="flex flex-col items-center justify-center p-12 text-center">
            <FileBarChart className="h-12 w-12 text-muted-foreground mb-4" />
            <h3 className="text-lg font-medium">No reports found</h3>
            <p className="text-sm text-muted-foreground mt-1">
              Generate a report to get started.
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

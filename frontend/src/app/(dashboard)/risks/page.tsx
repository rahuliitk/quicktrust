"use client";

import { useState } from "react";
import Link from "next/link";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Skeleton } from "@/components/ui/skeleton";
import { useRisks, useCreateRisk } from "@/hooks/use-api";
import { AlertTriangle, Grid3X3, Plus, Loader2 } from "lucide-react";
import type { RiskLevel, RiskStatus } from "@/lib/types";

const DEMO_ORG_ID = "00000000-0000-0000-0000-000000000000";

const STATUS_FILTERS: { label: string; value: string | undefined }[] = [
  { label: "All", value: undefined },
  { label: "Identified", value: "identified" },
  { label: "Assessed", value: "assessed" },
  { label: "Treating", value: "treating" },
  { label: "Accepted", value: "accepted" },
  { label: "Closed", value: "closed" },
];

const RISK_LEVEL_FILTERS: { label: string; value: string | undefined }[] = [
  { label: "All", value: undefined },
  { label: "Critical", value: "critical" },
  { label: "High", value: "high" },
  { label: "Medium", value: "medium" },
  { label: "Low", value: "low" },
];

const riskLevelVariant: Record<RiskLevel, string> = {
  critical: "destructive",
  high: "warning",
  medium: "warning",
  low: "success",
};

const riskLevelColor: Record<RiskLevel, string> = {
  critical: "bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-100",
  high: "bg-orange-100 text-orange-800 dark:bg-orange-900 dark:text-orange-100",
  medium: "bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-100",
  low: "bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-100",
};

const statusVariant: Record<RiskStatus, "default" | "secondary" | "success" | "outline"> = {
  identified: "secondary",
  assessed: "default",
  treating: "default",
  accepted: "success",
  closed: "outline",
};

export default function RisksPage() {
  const [statusFilter, setStatusFilter] = useState<string | undefined>(undefined);
  const [riskLevelFilter, setRiskLevelFilter] = useState<string | undefined>(undefined);
  const { data, isLoading } = useRisks(DEMO_ORG_ID, {
    status: statusFilter,
    risk_level: riskLevelFilter,
  });

  const [showCreate, setShowCreate] = useState(false);
  const [form, setForm] = useState({
    title: "",
    description: "",
    category: "operational" as const,
    likelihood: 3,
    impact: 3,
  });

  const createRisk = useCreateRisk(DEMO_ORG_ID);

  const resetForm = () =>
    setForm({ title: "", description: "", category: "operational", likelihood: 3, impact: 3 });

  const handleCreate = () => {
    createRisk.mutate(form, {
      onSuccess: () => {
        setShowCreate(false);
        resetForm();
      },
    });
  };

  const risks = data?.items || [];

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold">Risk Register</h1>
          <p className="text-muted-foreground">
            Track and manage organizational risks
          </p>
        </div>
        <div className="flex items-center gap-2">
          <Button onClick={() => setShowCreate((v) => !v)}>
            <Plus className="mr-2 h-4 w-4" />
            New Risk
          </Button>
          <Link href="/risks/matrix">
            <Button variant="outline">
              <Grid3X3 className="mr-2 h-4 w-4" />
              View Risk Matrix
            </Button>
          </Link>
        </div>
      </div>

      {showCreate && (
        <Card>
          <CardContent className="p-4 space-y-4">
            <h2 className="text-lg font-semibold">Create New Risk</h2>

            <div className="space-y-1">
              <label className="text-sm font-medium">Title</label>
              <input
                type="text"
                required
                className="w-full rounded-md border bg-background p-2 text-sm"
                placeholder="Risk title"
                value={form.title}
                onChange={(e) => setForm({ ...form, title: e.target.value })}
              />
            </div>

            <div className="space-y-1">
              <label className="text-sm font-medium">Description</label>
              <textarea
                className="w-full rounded-md border bg-background p-2 text-sm"
                placeholder="Optional description"
                rows={3}
                value={form.description}
                onChange={(e) => setForm({ ...form, description: e.target.value })}
              />
            </div>

            <div className="grid grid-cols-3 gap-4">
              <div className="space-y-1">
                <label className="text-sm font-medium">Category</label>
                <select
                  className="w-full rounded-md border bg-background p-2 text-sm"
                  value={form.category}
                  onChange={(e) => setForm({ ...form, category: e.target.value as typeof form.category })}
                >
                  <option value="operational">Operational</option>
                  <option value="security">Security</option>
                  <option value="compliance">Compliance</option>
                  <option value="financial">Financial</option>
                </select>
              </div>

              <div className="space-y-1">
                <label className="text-sm font-medium">Likelihood</label>
                <select
                  className="w-full rounded-md border bg-background p-2 text-sm"
                  value={form.likelihood}
                  onChange={(e) => setForm({ ...form, likelihood: Number(e.target.value) })}
                >
                  {[1, 2, 3, 4, 5].map((n) => (
                    <option key={n} value={n}>
                      {n}
                    </option>
                  ))}
                </select>
              </div>

              <div className="space-y-1">
                <label className="text-sm font-medium">Impact</label>
                <select
                  className="w-full rounded-md border bg-background p-2 text-sm"
                  value={form.impact}
                  onChange={(e) => setForm({ ...form, impact: Number(e.target.value) })}
                >
                  {[1, 2, 3, 4, 5].map((n) => (
                    <option key={n} value={n}>
                      {n}
                    </option>
                  ))}
                </select>
              </div>
            </div>

            <div className="flex items-center gap-2 pt-2">
              <Button onClick={handleCreate} disabled={!form.title.trim() || createRisk.isPending}>
                {createRisk.isPending && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
                Create Risk
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

      {/* Status filters */}
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

        {/* Risk level filters */}
        <div className="flex flex-wrap gap-2">
          <span className="flex items-center text-sm text-muted-foreground mr-1">
            Risk Level:
          </span>
          {RISK_LEVEL_FILTERS.map((f) => (
            <Button
              key={f.label}
              variant={riskLevelFilter === f.value ? "default" : "outline"}
              size="sm"
              onClick={() => setRiskLevelFilter(f.value)}
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
      ) : risks.length > 0 ? (
        <div className="space-y-3">
          {risks.map((risk) => (
            <Link key={risk.id} href={`/risks/${risk.id}`}>
              <Card className="transition-colors hover:bg-accent/50">
                <CardContent className="flex items-center gap-4 p-4">
                  <AlertTriangle className="h-8 w-8 text-muted-foreground shrink-0" />
                  <div className="flex-1 min-w-0">
                    <div className="font-medium">{risk.title}</div>
                    <div className="mt-1 flex items-center gap-2 text-xs text-muted-foreground">
                      <span>
                        Score: {risk.likelihood} x {risk.impact} ={" "}
                        <span className="font-semibold">{risk.risk_score}</span>
                      </span>
                      {risk.created_at && (
                        <>
                          <span>&middot;</span>
                          <span>
                            Created{" "}
                            {new Date(risk.created_at).toLocaleDateString()}
                          </span>
                        </>
                      )}
                    </div>
                  </div>
                  <Badge variant="outline" className="capitalize">
                    {risk.category}
                  </Badge>
                  <Badge
                    className={riskLevelColor[risk.risk_level]}
                  >
                    {risk.risk_level}
                  </Badge>
                  <Badge variant={statusVariant[risk.status] || "secondary"}>
                    {risk.status}
                  </Badge>
                </CardContent>
              </Card>
            </Link>
          ))}
        </div>
      ) : (
        <Card>
          <CardContent className="flex flex-col items-center justify-center p-12 text-center">
            <AlertTriangle className="h-12 w-12 text-muted-foreground mb-4" />
            <h3 className="text-lg font-medium">No risks found</h3>
            <p className="text-sm text-muted-foreground mt-1">
              No risks match the current filters, or the risk register is empty.
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

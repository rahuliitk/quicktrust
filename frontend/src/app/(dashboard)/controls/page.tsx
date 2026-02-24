"use client";

import Link from "next/link";
import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Skeleton } from "@/components/ui/skeleton";
import { useControls, useBulkApprove } from "@/hooks/use-api";
import { useOrgId } from "@/hooks/use-org-id";
import type { ControlStatus } from "@/lib/types";
import { CheckCircle, ListChecks, AlertTriangle } from "lucide-react";

const statusColors: Record<ControlStatus, string> = {
  draft: "secondary",
  implemented: "success",
  partially_implemented: "warning",
  not_implemented: "destructive",
  not_applicable: "outline",
};

export default function ControlsPage() {
  const orgId = useOrgId();
  const [statusFilter, setStatusFilter] = useState<string | undefined>();
  const [selectedIds, setSelectedIds] = useState<Set<string>>(new Set());
  const { data, isLoading, error } = useControls(orgId, { status: statusFilter });
  const bulkApprove = useBulkApprove(orgId);

  const controls = data?.items || [];

  function toggleSelect(id: string) {
    setSelectedIds((prev) => {
      const next = new Set(prev);
      if (next.has(id)) next.delete(id);
      else next.add(id);
      return next;
    });
  }

  function handleBulkApprove() {
    if (selectedIds.size === 0) return;
    bulkApprove.mutate(
      { control_ids: Array.from(selectedIds), status: "implemented" },
      { onSuccess: () => setSelectedIds(new Set()) }
    );
  }

  const filters: { label: string; value: string | undefined }[] = [
    { label: "All", value: undefined },
    { label: "Draft", value: "draft" },
    { label: "Implemented", value: "implemented" },
    { label: "Partial", value: "partially_implemented" },
    { label: "Not Implemented", value: "not_implemented" },
  ];

  if (error) {
    return (
      <div className="space-y-6">
        <div>
          <h1 className="text-3xl font-bold">Controls</h1>
          <p className="text-muted-foreground">Manage your organization's security controls</p>
        </div>
        <Card className="border-destructive">
          <CardContent className="flex flex-col items-center justify-center p-12 text-center">
            <AlertTriangle className="h-12 w-12 text-destructive mb-4" />
            <h3 className="text-lg font-semibold">Failed to load controls</h3>
            <p className="text-sm text-muted-foreground mt-2">
              {error.message || "An unexpected error occurred. Please try again later."}
            </p>
            <Button className="mt-4" onClick={() => window.location.reload()}>
              Retry
            </Button>
          </CardContent>
        </Card>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold">Controls</h1>
          <p className="text-muted-foreground">
            Manage your organization's security controls
          </p>
        </div>
        {selectedIds.size > 0 && (
          <Button onClick={handleBulkApprove} disabled={bulkApprove.isPending}>
            <CheckCircle className="mr-2 h-4 w-4" />
            Approve {selectedIds.size} Selected
          </Button>
        )}
      </div>

      <div className="flex gap-2">
        {filters.map((f) => (
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

      {isLoading ? (
        <div className="space-y-3">
          {[1, 2, 3, 4, 5].map((i) => (
            <Skeleton key={i} className="h-20 w-full rounded-xl" />
          ))}
        </div>
      ) : controls.length > 0 ? (
        <div className="space-y-3">
          {controls.map((control) => (
            <Card
              key={control.id}
              className={`transition-colors ${
                selectedIds.has(control.id)
                  ? "ring-2 ring-primary"
                  : ""
              }`}
            >
              <CardContent className="flex items-center gap-4 p-4">
                <input
                  type="checkbox"
                  checked={selectedIds.has(control.id)}
                  onChange={() => toggleSelect(control.id)}
                  className="h-4 w-4 rounded border-gray-300"
                />
                <div className="flex-1">
                  <Link
                    href={`/controls/${control.id}`}
                    className="font-medium hover:underline"
                  >
                    {control.title}
                  </Link>
                  {control.description && (
                    <p className="mt-1 text-sm text-muted-foreground line-clamp-1">
                      {control.description}
                    </p>
                  )}
                </div>
                <Badge
                  variant={
                    statusColors[control.status] as any
                  }
                >
                  {control.status.replace(/_/g, " ")}
                </Badge>
                <Badge variant="outline">{control.automation_level}</Badge>
              </CardContent>
            </Card>
          ))}
        </div>
      ) : (
        <Card>
          <CardContent className="p-12 text-center">
            <ListChecks className="mx-auto h-12 w-12 text-muted-foreground" />
            <h3 className="mt-4 text-lg font-semibold">No controls found</h3>
            <p className="mt-2 text-sm text-muted-foreground">
              Run the AI agent to generate controls from a framework.
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

"use client";

import { useState } from "react";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Skeleton } from "@/components/ui/skeleton";
import { useEvidence } from "@/hooks/use-api";
import { Shield, FileCheck } from "lucide-react";

const DEMO_ORG_ID = "00000000-0000-0000-0000-000000000000";

const STATUS_FILTERS: { label: string; value: string | undefined }[] = [
  { label: "All", value: undefined },
  { label: "Pending", value: "pending" },
  { label: "Collected", value: "collected" },
  { label: "Valid", value: "valid" },
  { label: "Expired", value: "expired" },
];

const METHOD_FILTERS: { label: string; value: string | undefined }[] = [
  { label: "All", value: undefined },
  { label: "Manual", value: "manual" },
  { label: "Automated", value: "automated" },
  { label: "API", value: "api" },
];

const statusBadgeVariant: Record<string, "default" | "secondary" | "success" | "destructive" | "outline"> = {
  pending: "secondary",
  collected: "success",
  valid: "success",
  expired: "destructive",
  invalid: "destructive",
};

const methodBadgeVariant: Record<string, "default" | "secondary" | "outline"> = {
  manual: "outline",
  automated: "default",
  api: "secondary",
};

export default function EvidencePage() {
  const [statusFilter, setStatusFilter] = useState<string | undefined>(undefined);
  const [methodFilter, setMethodFilter] = useState<string | undefined>(undefined);

  const { data, isLoading } = useEvidence(DEMO_ORG_ID);

  const allItems = data?.items || [];

  // Client-side filtering for status and method
  const evidenceItems = allItems.filter((item) => {
    if (statusFilter && item.status !== statusFilter) return false;
    if (methodFilter && item.collection_method !== methodFilter) return false;
    return true;
  });

  return (
    <div className="space-y-6">
      {/* Page header */}
      <div>
        <h1 className="text-3xl font-bold">Evidence Library</h1>
        <p className="text-muted-foreground">
          Track evidence collection status
        </p>
      </div>

      {/* Filters */}
      <div className="space-y-3">
        {/* Status filters */}
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

        {/* Collection method filters */}
        <div className="flex flex-wrap gap-2">
          <span className="flex items-center text-sm text-muted-foreground mr-1">
            Method:
          </span>
          {METHOD_FILTERS.map((f) => (
            <Button
              key={f.label}
              variant={methodFilter === f.value ? "default" : "outline"}
              size="sm"
              onClick={() => setMethodFilter(f.value)}
            >
              {f.label}
            </Button>
          ))}
        </div>
      </div>

      {/* Evidence list */}
      {isLoading ? (
        <div className="space-y-3">
          {[1, 2, 3, 4, 5].map((i) => (
            <Skeleton key={i} className="h-24 w-full rounded-xl" />
          ))}
        </div>
      ) : evidenceItems.length > 0 ? (
        <div className="space-y-3">
          {evidenceItems.map((evidence) => (
            <Card key={evidence.id} className="transition-colors hover:bg-muted/50">
              <CardContent className="flex items-center gap-4 p-4">
                <Shield className="h-8 w-8 text-muted-foreground shrink-0" />
                <div className="flex-1 min-w-0">
                  <div className="font-medium">{evidence.title}</div>
                  <div className="mt-1 flex flex-wrap items-center gap-2 text-sm text-muted-foreground">
                    {evidence.collected_at && (
                      <span>
                        Collected{" "}
                        {new Date(evidence.collected_at).toLocaleDateString()}
                      </span>
                    )}
                    {evidence.expires_at && (
                      <>
                        <span>&middot;</span>
                        <span>
                          Expires{" "}
                          {new Date(evidence.expires_at).toLocaleDateString()}
                        </span>
                      </>
                    )}
                    {evidence.collector && (
                      <>
                        <span>&middot;</span>
                        <span>{evidence.collector}</span>
                      </>
                    )}
                  </div>
                </div>
                <div className="flex items-center gap-2 shrink-0">
                  <Badge
                    variant={
                      (methodBadgeVariant[evidence.collection_method] ||
                        "outline") as any
                    }
                  >
                    {evidence.collection_method}
                  </Badge>
                  <Badge
                    variant={
                      (statusBadgeVariant[evidence.status] ||
                        "secondary") as any
                    }
                  >
                    {evidence.status}
                  </Badge>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      ) : (
        <Card>
          <CardContent className="flex flex-col items-center justify-center p-12 text-center">
            <FileCheck className="h-12 w-12 text-muted-foreground mb-4" />
            <h3 className="text-lg font-medium">No evidence found</h3>
            <p className="text-sm text-muted-foreground mt-1">
              No evidence items match the current filters, or the evidence library is empty.
            </p>
          </CardContent>
        </Card>
      )}

      {/* Pagination info */}
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

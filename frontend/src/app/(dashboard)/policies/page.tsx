"use client";

import { useState } from "react";
import Link from "next/link";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Skeleton } from "@/components/ui/skeleton";
import { usePolicies } from "@/hooks/use-api";
import { FileText } from "lucide-react";
import type { PolicyStatus } from "@/lib/types";

const DEMO_ORG_ID = "00000000-0000-0000-0000-000000000000";

const STATUS_FILTERS: { label: string; value: string | undefined }[] = [
  { label: "All", value: undefined },
  { label: "Draft", value: "draft" },
  { label: "In Review", value: "in_review" },
  { label: "Approved", value: "approved" },
  { label: "Published", value: "published" },
];

const statusVariant: Record<string, "default" | "secondary" | "success" | "destructive" | "outline"> = {
  draft: "secondary",
  in_review: "default",
  approved: "success",
  published: "success",
  archived: "outline",
};

export default function PoliciesPage() {
  const [statusFilter, setStatusFilter] = useState<string | undefined>(undefined);
  const { data, isLoading } = usePolicies(DEMO_ORG_ID, { status: statusFilter });

  const policies = data?.items || [];

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold">Policies</h1>
        <p className="text-muted-foreground">
          Manage your organization's security and compliance policies
        </p>
      </div>

      <div className="flex gap-2">
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

      {isLoading ? (
        <div className="space-y-3">
          {[1, 2, 3].map((i) => (
            <Skeleton key={i} className="h-24 w-full" />
          ))}
        </div>
      ) : policies.length > 0 ? (
        <div className="space-y-3">
          {policies.map((policy) => (
            <Link key={policy.id} href={`/policies/${policy.id}`}>
              <Card className="transition-colors hover:bg-accent/50">
                <CardContent className="flex items-center gap-4 p-4">
                  <FileText className="h-8 w-8 text-muted-foreground shrink-0" />
                  <div className="flex-1 min-w-0">
                    <div className="font-medium">{policy.title}</div>
                    <div className="text-xs text-muted-foreground mt-1">
                      Version {policy.version} &middot; Created{" "}
                      {new Date(policy.created_at).toLocaleDateString()}
                      {policy.published_at &&
                        ` &middot; Published ${new Date(policy.published_at).toLocaleDateString()}`}
                    </div>
                  </div>
                  <Badge variant={statusVariant[policy.status] || "secondary"}>
                    {policy.status.replace(/_/g, " ")}
                  </Badge>
                </CardContent>
              </Card>
            </Link>
          ))}
        </div>
      ) : (
        <Card>
          <CardContent className="flex flex-col items-center justify-center p-12 text-center">
            <FileText className="h-12 w-12 text-muted-foreground mb-4" />
            <h3 className="text-lg font-medium">No policies yet</h3>
            <p className="text-sm text-muted-foreground mt-1">
              Use the AI Policy Generation agent to create policies, or create them manually.
            </p>
            <Link href="/agents/policy-generation">
              <Button className="mt-4">Generate Policies with AI</Button>
            </Link>
          </CardContent>
        </Card>
      )}
    </div>
  );
}

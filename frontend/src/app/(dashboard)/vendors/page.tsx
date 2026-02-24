"use client";

import { useState } from "react";
import Link from "next/link";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Skeleton } from "@/components/ui/skeleton";
import {
  useVendors,
  useVendorStats,
  useCreateVendor,
} from "@/hooks/use-api";
import { useOrgId } from "@/hooks/use-org-id";
import { Building2, Plus, Loader2 } from "lucide-react";
import type { VendorRiskTier } from "@/lib/types";

const RISK_TIER_FILTERS: { label: string; value: string | undefined }[] = [
  { label: "All", value: undefined },
  { label: "Critical", value: "critical" },
  { label: "High", value: "high" },
  { label: "Medium", value: "medium" },
  { label: "Low", value: "low" },
];

const STATUS_FILTERS: { label: string; value: string | undefined }[] = [
  { label: "All", value: undefined },
  { label: "Active", value: "active" },
  { label: "Under Review", value: "under_review" },
  { label: "Terminated", value: "terminated" },
];

const riskTierColor: Record<string, string> = {
  critical: "bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-100",
  high: "bg-orange-100 text-orange-800 dark:bg-orange-900 dark:text-orange-100",
  medium:
    "bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-100",
  low: "bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-100",
};

const statusVariant: Record<string, "default" | "secondary" | "success" | "destructive" | "outline"> = {
  active: "success",
  under_review: "warning" as any,
  terminated: "destructive",
};

export default function VendorsPage() {
  const orgId = useOrgId();
  const [riskTierFilter, setRiskTierFilter] = useState<string | undefined>(
    undefined
  );
  const [statusFilter, setStatusFilter] = useState<string | undefined>(
    undefined
  );
  const { data, isLoading } = useVendors(orgId, {
    risk_tier: riskTierFilter,
    status: statusFilter,
  });
  const { data: stats } = useVendorStats(orgId);

  const [showCreate, setShowCreate] = useState(false);
  const [form, setForm] = useState({
    name: "",
    category: "",
    website: "",
    risk_tier: "medium",
    contact_name: "",
    contact_email: "",
  });
  const createVendor = useCreateVendor(orgId);

  const resetForm = () =>
    setForm({
      name: "",
      category: "",
      website: "",
      risk_tier: "medium",
      contact_name: "",
      contact_email: "",
    });

  const handleCreate = () => {
    createVendor.mutate(
      { ...form, risk_tier: form.risk_tier as VendorRiskTier },
      {
        onSuccess: () => {
          setShowCreate(false);
          resetForm();
        },
      }
    );
  };

  const vendors = data?.items || [];

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold">Vendor Management</h1>
          <p className="text-muted-foreground">
            Track and assess third-party vendors
          </p>
        </div>
        <Button onClick={() => setShowCreate((v) => !v)}>
          <Plus className="mr-2 h-4 w-4" />
          New Vendor
        </Button>
      </div>

      {/* Stats */}
      {stats && (
        <div className="grid grid-cols-4 gap-4">
          {[
            { label: "Total", value: stats.total ?? 0 },
            { label: "Critical", value: stats.by_risk_tier?.critical ?? 0 },
            { label: "High", value: stats.by_risk_tier?.high ?? 0 },
            { label: "Active", value: stats.by_status?.active ?? 0 },
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
            <h2 className="text-lg font-semibold">Add New Vendor</h2>

            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-1">
                <label className="text-sm font-medium">Name</label>
                <input
                  type="text"
                  required
                  className="w-full rounded-md border bg-background p-2 text-sm"
                  placeholder="Vendor name"
                  value={form.name}
                  onChange={(e) => setForm({ ...form, name: e.target.value })}
                />
              </div>

              <div className="space-y-1">
                <label className="text-sm font-medium">Category</label>
                <input
                  type="text"
                  className="w-full rounded-md border bg-background p-2 text-sm"
                  placeholder="e.g. Cloud Provider, SaaS"
                  value={form.category}
                  onChange={(e) =>
                    setForm({ ...form, category: e.target.value })
                  }
                />
              </div>

              <div className="space-y-1">
                <label className="text-sm font-medium">Website</label>
                <input
                  type="url"
                  className="w-full rounded-md border bg-background p-2 text-sm"
                  placeholder="https://vendor.com"
                  value={form.website}
                  onChange={(e) =>
                    setForm({ ...form, website: e.target.value })
                  }
                />
              </div>

              <div className="space-y-1">
                <label className="text-sm font-medium">Risk Tier</label>
                <select
                  className="w-full rounded-md border bg-background p-2 text-sm"
                  value={form.risk_tier}
                  onChange={(e) =>
                    setForm({ ...form, risk_tier: e.target.value })
                  }
                >
                  <option value="critical">Critical</option>
                  <option value="high">High</option>
                  <option value="medium">Medium</option>
                  <option value="low">Low</option>
                </select>
              </div>

              <div className="space-y-1">
                <label className="text-sm font-medium">Contact Name</label>
                <input
                  type="text"
                  className="w-full rounded-md border bg-background p-2 text-sm"
                  placeholder="Primary contact"
                  value={form.contact_name}
                  onChange={(e) =>
                    setForm({ ...form, contact_name: e.target.value })
                  }
                />
              </div>

              <div className="space-y-1">
                <label className="text-sm font-medium">Contact Email</label>
                <input
                  type="email"
                  className="w-full rounded-md border bg-background p-2 text-sm"
                  placeholder="contact@vendor.com"
                  value={form.contact_email}
                  onChange={(e) =>
                    setForm({ ...form, contact_email: e.target.value })
                  }
                />
              </div>
            </div>

            <div className="flex items-center gap-2 pt-2">
              <Button
                onClick={handleCreate}
                disabled={!form.name.trim() || createVendor.isPending}
              >
                {createVendor.isPending && (
                  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                )}
                Add Vendor
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
          <span className="flex items-center text-sm text-muted-foreground mr-1">
            Risk Tier:
          </span>
          {RISK_TIER_FILTERS.map((f) => (
            <Button
              key={f.label}
              variant={riskTierFilter === f.value ? "default" : "outline"}
              size="sm"
              onClick={() => setRiskTierFilter(f.value)}
            >
              {f.label}
            </Button>
          ))}
        </div>

        <div className="flex flex-wrap gap-2">
          <span className="flex items-center text-sm text-muted-foreground mr-1">
            Status:
          </span>
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
          {[1, 2, 3, 4, 5].map((i) => (
            <Skeleton key={i} className="h-24 w-full rounded-xl" />
          ))}
        </div>
      ) : vendors.length > 0 ? (
        <div className="space-y-3">
          {vendors.map((vendor: any) => (
            <Link key={vendor.id} href={`/vendors/${vendor.id}`}>
              <Card className="transition-colors hover:bg-accent/50">
                <CardContent className="flex items-center gap-4 p-4">
                  <Building2 className="h-8 w-8 text-muted-foreground shrink-0" />
                  <div className="flex-1 min-w-0">
                    <div className="font-medium">{vendor.name}</div>
                    <div className="mt-1 text-xs text-muted-foreground">
                      {vendor.category && (
                        <span className="capitalize">{vendor.category}</span>
                      )}
                      {vendor.website && (
                        <>
                          <span> &middot; </span>
                          <span>{vendor.website}</span>
                        </>
                      )}
                    </div>
                  </div>
                  <Badge className={riskTierColor[vendor.risk_tier] || ""}>
                    {vendor.risk_tier}
                  </Badge>
                  <Badge
                    variant={statusVariant[vendor.status] || "secondary"}
                  >
                    {vendor.status?.replace(/_/g, " ")}
                  </Badge>
                </CardContent>
              </Card>
            </Link>
          ))}
        </div>
      ) : (
        <Card>
          <CardContent className="flex flex-col items-center justify-center p-12 text-center">
            <Building2 className="h-12 w-12 text-muted-foreground mb-4" />
            <h3 className="text-lg font-medium">No vendors found</h3>
            <p className="text-sm text-muted-foreground mt-1">
              No vendors match the current filters, or no vendors have been
              added yet.
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

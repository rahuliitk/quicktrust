"use client";

import { useState } from "react";
import Link from "next/link";
import { useParams, useRouter } from "next/navigation";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Skeleton } from "@/components/ui/skeleton";
import {
  useVendor,
  useUpdateVendor,
  useDeleteVendor,
  useVendorAssessments,
  useCreateVendorAssessment,
} from "@/hooks/use-api";
import {
  ArrowLeft,
  Pencil,
  Trash2,
  Loader2,
  Save,
  X,
  ClipboardCheck,
  Plus,
  Building2,
} from "lucide-react";

const DEMO_ORG_ID = "00000000-0000-0000-0000-000000000000";

const riskTierColor: Record<string, string> = {
  critical: "bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-100",
  high: "bg-orange-100 text-orange-800 dark:bg-orange-900 dark:text-orange-100",
  medium:
    "bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-100",
  low: "bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-100",
};

export default function VendorDetailPage() {
  const params = useParams();
  const router = useRouter();
  const vendorId = params.id as string;

  const { data: vendor, isLoading } = useVendor(DEMO_ORG_ID, vendorId);
  const { data: assessments, isLoading: assessmentsLoading } =
    useVendorAssessments(DEMO_ORG_ID, vendorId);
  const updateVendor = useUpdateVendor(DEMO_ORG_ID);
  const deleteVendor = useDeleteVendor(DEMO_ORG_ID);
  const createAssessment = useCreateVendorAssessment(DEMO_ORG_ID, vendorId);

  const [editing, setEditing] = useState(false);
  const [form, setForm] = useState({
    name: "",
    category: "",
    website: "",
    risk_tier: "medium",
    status: "active",
    contact_name: "",
    contact_email: "",
    contract_start_date: "",
    contract_end_date: "",
    data_classification: "",
    description: "",
  });

  const [showAddAssessment, setShowAddAssessment] = useState(false);
  const [assessmentForm, setAssessmentForm] = useState({
    score: 50,
    risk_tier_assigned: "medium",
    notes: "",
  });

  function enterEditMode() {
    if (!vendor) return;
    setForm({
      name: vendor.name || "",
      category: vendor.category || "",
      website: vendor.website || "",
      risk_tier: vendor.risk_tier || "medium",
      status: vendor.status || "active",
      contact_name: vendor.contact_name || "",
      contact_email: vendor.contact_email || "",
      contract_start_date: vendor.contract_start_date || "",
      contract_end_date: vendor.contract_end_date || "",
      data_classification: vendor.data_classification || "",
      description: vendor.description || "",
    });
    setEditing(true);
  }

  function handleSave() {
    if (!vendor) return;
    updateVendor.mutate(
      { vendorId: vendor.id, ...form },
      { onSuccess: () => setEditing(false) }
    );
  }

  function handleDelete() {
    if (!vendor) return;
    const confirmed = window.confirm(
      `Are you sure you want to delete vendor "${vendor.name}"? This action cannot be undone.`
    );
    if (!confirmed) return;
    deleteVendor.mutate(vendor.id, {
      onSuccess: () => router.push("/vendors"),
    });
  }

  function handleAddAssessment() {
    createAssessment.mutate(
      {
        score: assessmentForm.score,
        risk_tier_assigned: assessmentForm.risk_tier_assigned,
        notes: assessmentForm.notes || undefined,
      },
      {
        onSuccess: () => {
          setShowAddAssessment(false);
          setAssessmentForm({ score: 50, risk_tier_assigned: "medium", notes: "" });
        },
      }
    );
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

  if (!vendor) return <p>Vendor not found.</p>;

  return (
    <div className="space-y-6">
      <Link
        href="/vendors"
        className="inline-flex items-center gap-1 text-sm text-muted-foreground hover:text-foreground transition-colors"
      >
        <ArrowLeft className="h-4 w-4" />
        Back to Vendors
      </Link>

      {/* Header */}
      <div className="flex items-center gap-3">
        <h1 className="text-3xl font-bold">{vendor.name}</h1>
        <Badge className={riskTierColor[vendor.risk_tier] || ""}>
          {vendor.risk_tier}
        </Badge>
        <Badge variant="outline" className="capitalize">
          {vendor.status?.replace(/_/g, " ")}
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
            disabled={deleteVendor.isPending}
          >
            {deleteVendor.isPending ? (
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
            <CardTitle>Edit Vendor</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="text-sm font-medium">Name</label>
                <input
                  type="text"
                  className="mt-1 w-full rounded-md border bg-background p-2 text-sm"
                  value={form.name}
                  onChange={(e) => setForm({ ...form, name: e.target.value })}
                />
              </div>
              <div>
                <label className="text-sm font-medium">Category</label>
                <input
                  type="text"
                  className="mt-1 w-full rounded-md border bg-background p-2 text-sm"
                  value={form.category}
                  onChange={(e) =>
                    setForm({ ...form, category: e.target.value })
                  }
                />
              </div>
              <div>
                <label className="text-sm font-medium">Website</label>
                <input
                  type="url"
                  className="mt-1 w-full rounded-md border bg-background p-2 text-sm"
                  value={form.website}
                  onChange={(e) =>
                    setForm({ ...form, website: e.target.value })
                  }
                />
              </div>
              <div>
                <label className="text-sm font-medium">Risk Tier</label>
                <select
                  className="mt-1 w-full rounded-md border bg-background p-2 text-sm"
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
              <div>
                <label className="text-sm font-medium">Status</label>
                <select
                  className="mt-1 w-full rounded-md border bg-background p-2 text-sm"
                  value={form.status}
                  onChange={(e) =>
                    setForm({ ...form, status: e.target.value })
                  }
                >
                  <option value="active">Active</option>
                  <option value="under_review">Under Review</option>
                  <option value="terminated">Terminated</option>
                </select>
              </div>
              <div>
                <label className="text-sm font-medium">
                  Data Classification
                </label>
                <input
                  type="text"
                  className="mt-1 w-full rounded-md border bg-background p-2 text-sm"
                  placeholder="e.g. confidential, public"
                  value={form.data_classification}
                  onChange={(e) =>
                    setForm({ ...form, data_classification: e.target.value })
                  }
                />
              </div>
              <div>
                <label className="text-sm font-medium">Contact Name</label>
                <input
                  type="text"
                  className="mt-1 w-full rounded-md border bg-background p-2 text-sm"
                  value={form.contact_name}
                  onChange={(e) =>
                    setForm({ ...form, contact_name: e.target.value })
                  }
                />
              </div>
              <div>
                <label className="text-sm font-medium">Contact Email</label>
                <input
                  type="email"
                  className="mt-1 w-full rounded-md border bg-background p-2 text-sm"
                  value={form.contact_email}
                  onChange={(e) =>
                    setForm({ ...form, contact_email: e.target.value })
                  }
                />
              </div>
              <div>
                <label className="text-sm font-medium">
                  Contract Start Date
                </label>
                <input
                  type="date"
                  className="mt-1 w-full rounded-md border bg-background p-2 text-sm"
                  value={form.contract_start_date}
                  onChange={(e) =>
                    setForm({ ...form, contract_start_date: e.target.value })
                  }
                />
              </div>
              <div>
                <label className="text-sm font-medium">
                  Contract End Date
                </label>
                <input
                  type="date"
                  className="mt-1 w-full rounded-md border bg-background p-2 text-sm"
                  value={form.contract_end_date}
                  onChange={(e) =>
                    setForm({ ...form, contract_end_date: e.target.value })
                  }
                />
              </div>
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

            <div className="flex items-center gap-2">
              <Button
                size="sm"
                onClick={handleSave}
                disabled={updateVendor.isPending}
              >
                {updateVendor.isPending ? (
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
                disabled={updateVendor.isPending}
              >
                <X className="mr-1 h-4 w-4" />
                Cancel
              </Button>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Vendor info cards */}
      {!editing && (
        <div className="grid gap-6 md:grid-cols-2">
          <Card>
            <CardHeader>
              <CardTitle>Vendor Details</CardTitle>
            </CardHeader>
            <CardContent>
              <dl className="space-y-3 text-sm">
                <div>
                  <dt className="font-medium text-muted-foreground">
                    Category
                  </dt>
                  <dd className="mt-1 capitalize">
                    {vendor.category || "Not specified"}
                  </dd>
                </div>
                <div>
                  <dt className="font-medium text-muted-foreground">
                    Website
                  </dt>
                  <dd className="mt-1">{vendor.website || "Not specified"}</dd>
                </div>
                <div>
                  <dt className="font-medium text-muted-foreground">
                    Contact
                  </dt>
                  <dd className="mt-1">
                    {vendor.contact_name || "Not specified"}
                    {vendor.contact_email && ` (${vendor.contact_email})`}
                  </dd>
                </div>
                {vendor.data_classification && (
                  <div>
                    <dt className="font-medium text-muted-foreground">
                      Data Classification
                    </dt>
                    <dd className="mt-1 capitalize">
                      {vendor.data_classification}
                    </dd>
                  </div>
                )}
                {vendor.description && (
                  <div>
                    <dt className="font-medium text-muted-foreground">
                      Description
                    </dt>
                    <dd className="mt-1">{vendor.description}</dd>
                  </div>
                )}
              </dl>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Contract Information</CardTitle>
            </CardHeader>
            <CardContent>
              <dl className="space-y-3 text-sm">
                <div>
                  <dt className="font-medium text-muted-foreground">
                    Contract Start
                  </dt>
                  <dd className="mt-1">
                    {vendor.contract_start_date
                      ? new Date(
                          vendor.contract_start_date
                        ).toLocaleDateString()
                      : "Not specified"}
                  </dd>
                </div>
                <div>
                  <dt className="font-medium text-muted-foreground">
                    Contract End
                  </dt>
                  <dd className="mt-1">
                    {vendor.contract_end_date
                      ? new Date(
                          vendor.contract_end_date
                        ).toLocaleDateString()
                      : "Not specified"}
                  </dd>
                </div>
                <div>
                  <dt className="font-medium text-muted-foreground">
                    Created
                  </dt>
                  <dd className="mt-1">
                    {new Date(vendor.created_at).toLocaleDateString()}
                  </dd>
                </div>
              </dl>
            </CardContent>
          </Card>
        </div>
      )}

      {/* Assessments */}
      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <CardTitle>Assessments</CardTitle>
            <Button
              size="sm"
              variant="outline"
              onClick={() => setShowAddAssessment((v) => !v)}
            >
              <Plus className="mr-1 h-4 w-4" />
              Add Assessment
            </Button>
          </div>
        </CardHeader>
        <CardContent className="space-y-4">
          {showAddAssessment && (
            <div className="space-y-3 rounded-lg border p-4">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="text-sm font-medium">Score (0-100)</label>
                  <input
                    type="number"
                    min={0}
                    max={100}
                    className="mt-1 w-full rounded-md border bg-background p-2 text-sm"
                    value={assessmentForm.score}
                    onChange={(e) =>
                      setAssessmentForm({
                        ...assessmentForm,
                        score: Number(e.target.value),
                      })
                    }
                  />
                </div>
                <div>
                  <label className="text-sm font-medium">
                    Risk Tier Assigned
                  </label>
                  <select
                    className="mt-1 w-full rounded-md border bg-background p-2 text-sm"
                    value={assessmentForm.risk_tier_assigned}
                    onChange={(e) =>
                      setAssessmentForm({
                        ...assessmentForm,
                        risk_tier_assigned: e.target.value,
                      })
                    }
                  >
                    <option value="critical">Critical</option>
                    <option value="high">High</option>
                    <option value="medium">Medium</option>
                    <option value="low">Low</option>
                  </select>
                </div>
              </div>
              <div>
                <label className="text-sm font-medium">Notes</label>
                <textarea
                  className="mt-1 w-full rounded-md border bg-background p-2 text-sm"
                  rows={3}
                  placeholder="Assessment notes..."
                  value={assessmentForm.notes}
                  onChange={(e) =>
                    setAssessmentForm({
                      ...assessmentForm,
                      notes: e.target.value,
                    })
                  }
                />
              </div>
              <div className="flex gap-2">
                <Button
                  size="sm"
                  onClick={handleAddAssessment}
                  disabled={createAssessment.isPending}
                >
                  {createAssessment.isPending && (
                    <Loader2 className="mr-1 h-4 w-4 animate-spin" />
                  )}
                  Save Assessment
                </Button>
                <Button
                  size="sm"
                  variant="ghost"
                  onClick={() => {
                    setShowAddAssessment(false);
                    setAssessmentForm({
                      score: 50,
                      risk_tier_assigned: "medium",
                      notes: "",
                    });
                  }}
                >
                  Cancel
                </Button>
              </div>
            </div>
          )}

          {assessmentsLoading ? (
            <div className="space-y-3">
              {[1, 2].map((i) => (
                <Skeleton key={i} className="h-16 w-full rounded-lg" />
              ))}
            </div>
          ) : assessments && assessments.length > 0 ? (
            <div className="space-y-3">
              {assessments.map((a: any) => (
                <div
                  key={a.id}
                  className="flex items-center gap-4 rounded-lg border p-3"
                >
                  <ClipboardCheck className="h-5 w-5 text-muted-foreground shrink-0" />
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2">
                      <span className="text-sm font-medium">
                        Score: {a.score}/100
                      </span>
                      <Badge
                        className={
                          riskTierColor[a.risk_tier_assigned] || ""
                        }
                      >
                        {a.risk_tier_assigned}
                      </Badge>
                    </div>
                    {a.notes && (
                      <p className="mt-1 text-xs text-muted-foreground">
                        {a.notes}
                      </p>
                    )}
                    <p className="mt-1 text-xs text-muted-foreground">
                      {a.created_at &&
                        new Date(a.created_at).toLocaleDateString()}
                    </p>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="flex flex-col items-center justify-center py-6 text-center">
              <Building2 className="h-10 w-10 text-muted-foreground mb-3" />
              <p className="text-sm text-muted-foreground">
                No assessments yet.
              </p>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}

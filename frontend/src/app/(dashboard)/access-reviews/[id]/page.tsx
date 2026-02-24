"use client";

import { useState } from "react";
import Link from "next/link";
import { useParams } from "next/navigation";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Skeleton } from "@/components/ui/skeleton";
import { Progress } from "@/components/ui/progress";
import {
  useAccessReviewCampaign,
  useUpdateAccessReviewCampaign,
  useAccessReviewEntries,
  useCreateAccessReviewEntry,
  useUpdateAccessReviewEntry,
} from "@/hooks/use-api";
import {
  ArrowLeft,
  Pencil,
  Loader2,
  Save,
  X,
  ShieldCheck,
  Plus,
  CheckCircle,
  XCircle,
  UserCheck,
} from "lucide-react";
import { useOrgId } from "@/hooks/use-org-id";

const statusColor: Record<string, string> = {
  draft: "bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-100",
  active: "bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-100",
  completed:
    "bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-100",
  cancelled: "bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-100",
};

const decisionColor: Record<string, string> = {
  approved:
    "bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-100",
  revoked: "bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-100",
  pending:
    "bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-100",
};

export default function AccessReviewDetailPage() {
  const orgId = useOrgId();
  const params = useParams();
  const campaignId = params.id as string;

  const { data: campaign, isLoading } = useAccessReviewCampaign(
    orgId,
    campaignId
  );
  const { data: entries, isLoading: entriesLoading } =
    useAccessReviewEntries(orgId, campaignId);
  const updateCampaign = useUpdateAccessReviewCampaign(orgId);
  const createEntry = useCreateAccessReviewEntry(orgId, campaignId);
  const updateEntry = useUpdateAccessReviewEntry(orgId, campaignId);

  const [editing, setEditing] = useState(false);
  const [form, setForm] = useState({
    title: "",
    description: "",
    status: "draft",
    due_date: "",
  });

  const [showAddEntry, setShowAddEntry] = useState(false);
  const [entryForm, setEntryForm] = useState({
    user_name: "",
    user_email: "",
    system_name: "",
    resource: "",
    current_access: "",
  });

  function enterEditMode() {
    if (!campaign) return;
    setForm({
      title: campaign.title || "",
      description: campaign.description || "",
      status: campaign.status || "draft",
      due_date: campaign.due_date || "",
    });
    setEditing(true);
  }

  function handleSave() {
    if (!campaign) return;
    updateCampaign.mutate(
      { campaignId: campaign.id, ...form },
      { onSuccess: () => setEditing(false) }
    );
  }

  function handleAddEntry() {
    createEntry.mutate(entryForm, {
      onSuccess: () => {
        setShowAddEntry(false);
        setEntryForm({
          user_name: "",
          user_email: "",
          system_name: "",
          resource: "",
          current_access: "",
        });
      },
    });
  }

  function handleDecision(entryId: string, decision: "approved" | "revoked") {
    updateEntry.mutate({ entryId, decision });
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

  if (!campaign) return <p>Campaign not found.</p>;

  const totalEntries = entries?.length ?? 0;
  const decidedEntries =
    entries?.filter(
      (e: any) => e.decision === "approved" || e.decision === "revoked"
    ).length ?? 0;
  const progressPct =
    totalEntries > 0
      ? Math.round((decidedEntries / totalEntries) * 100)
      : 0;

  return (
    <div className="space-y-6">
      <Link
        href="/access-reviews"
        className="inline-flex items-center gap-1 text-sm text-muted-foreground hover:text-foreground transition-colors"
      >
        <ArrowLeft className="h-4 w-4" />
        Back to Access Reviews
      </Link>

      {/* Header */}
      <div className="flex items-center gap-3">
        <h1 className="text-3xl font-bold">{campaign.title}</h1>
        <Badge className={statusColor[campaign.status] || ""}>
          {campaign.status}
        </Badge>
        <div className="ml-auto flex items-center gap-2">
          {!editing && (
            <Button variant="outline" size="sm" onClick={enterEditMode}>
              <Pencil className="mr-1 h-4 w-4" />
              Edit
            </Button>
          )}
        </div>
      </div>

      {/* Progress */}
      {totalEntries > 0 && (
        <Card>
          <CardContent className="p-4 space-y-2">
            <div className="flex justify-between text-sm">
              <span>
                {decidedEntries} / {totalEntries} entries reviewed
              </span>
              <span className="font-medium">{progressPct}%</span>
            </div>
            <Progress value={progressPct} />
          </CardContent>
        </Card>
      )}

      {/* Edit Form */}
      {editing && (
        <Card>
          <CardHeader>
            <CardTitle>Edit Campaign</CardTitle>
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

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="text-sm font-medium">Status</label>
                <select
                  className="mt-1 w-full rounded-md border bg-background p-2 text-sm"
                  value={form.status}
                  onChange={(e) =>
                    setForm({ ...form, status: e.target.value })
                  }
                >
                  <option value="draft">Draft</option>
                  <option value="active">Active</option>
                  <option value="completed">Completed</option>
                  <option value="cancelled">Cancelled</option>
                </select>
              </div>
              <div>
                <label className="text-sm font-medium">Due Date</label>
                <input
                  type="date"
                  className="mt-1 w-full rounded-md border bg-background p-2 text-sm"
                  value={form.due_date}
                  onChange={(e) =>
                    setForm({ ...form, due_date: e.target.value })
                  }
                />
              </div>
            </div>

            <div className="flex items-center gap-2">
              <Button
                size="sm"
                onClick={handleSave}
                disabled={updateCampaign.isPending}
              >
                {updateCampaign.isPending ? (
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
                disabled={updateCampaign.isPending}
              >
                <X className="mr-1 h-4 w-4" />
                Cancel
              </Button>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Campaign Info */}
      {!editing && campaign.description && (
        <Card>
          <CardHeader>
            <CardTitle>Description</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="whitespace-pre-wrap">{campaign.description}</p>
            {campaign.due_date && (
              <p className="mt-2 text-sm text-muted-foreground">
                Due: {new Date(campaign.due_date).toLocaleDateString()}
              </p>
            )}
          </CardContent>
        </Card>
      )}

      {/* Entries */}
      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <CardTitle>
              Review Entries{" "}
              {totalEntries > 0 && `(${totalEntries})`}
            </CardTitle>
            <Button
              size="sm"
              variant="outline"
              onClick={() => setShowAddEntry((v) => !v)}
            >
              <Plus className="mr-1 h-4 w-4" />
              Add Entry
            </Button>
          </div>
        </CardHeader>
        <CardContent className="space-y-4">
          {showAddEntry && (
            <div className="space-y-3 rounded-lg border p-4">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="text-sm font-medium">User Name</label>
                  <input
                    type="text"
                    className="mt-1 w-full rounded-md border bg-background p-2 text-sm"
                    placeholder="John Doe"
                    value={entryForm.user_name}
                    onChange={(e) =>
                      setEntryForm({
                        ...entryForm,
                        user_name: e.target.value,
                      })
                    }
                  />
                </div>
                <div>
                  <label className="text-sm font-medium">User Email</label>
                  <input
                    type="email"
                    className="mt-1 w-full rounded-md border bg-background p-2 text-sm"
                    placeholder="john@company.com"
                    value={entryForm.user_email}
                    onChange={(e) =>
                      setEntryForm({
                        ...entryForm,
                        user_email: e.target.value,
                      })
                    }
                  />
                </div>
                <div>
                  <label className="text-sm font-medium">System Name</label>
                  <input
                    type="text"
                    className="mt-1 w-full rounded-md border bg-background p-2 text-sm"
                    placeholder="AWS Console"
                    value={entryForm.system_name}
                    onChange={(e) =>
                      setEntryForm({
                        ...entryForm,
                        system_name: e.target.value,
                      })
                    }
                  />
                </div>
                <div>
                  <label className="text-sm font-medium">Resource</label>
                  <input
                    type="text"
                    className="mt-1 w-full rounded-md border bg-background p-2 text-sm"
                    placeholder="S3 bucket, database, etc."
                    value={entryForm.resource}
                    onChange={(e) =>
                      setEntryForm({
                        ...entryForm,
                        resource: e.target.value,
                      })
                    }
                  />
                </div>
              </div>
              <div>
                <label className="text-sm font-medium">Current Access</label>
                <input
                  type="text"
                  className="mt-1 w-full rounded-md border bg-background p-2 text-sm"
                  placeholder="admin, read-only, write, etc."
                  value={entryForm.current_access}
                  onChange={(e) =>
                    setEntryForm({
                      ...entryForm,
                      current_access: e.target.value,
                    })
                  }
                />
              </div>
              <div className="flex gap-2">
                <Button
                  size="sm"
                  onClick={handleAddEntry}
                  disabled={
                    !entryForm.user_name.trim() ||
                    !entryForm.user_email.trim() ||
                    !entryForm.system_name.trim() ||
                    createEntry.isPending
                  }
                >
                  {createEntry.isPending && (
                    <Loader2 className="mr-1 h-4 w-4 animate-spin" />
                  )}
                  Add Entry
                </Button>
                <Button
                  size="sm"
                  variant="ghost"
                  onClick={() => {
                    setShowAddEntry(false);
                    setEntryForm({
                      user_name: "",
                      user_email: "",
                      system_name: "",
                      resource: "",
                      current_access: "",
                    });
                  }}
                >
                  Cancel
                </Button>
              </div>
            </div>
          )}

          {entriesLoading ? (
            <div className="space-y-3">
              {[1, 2, 3].map((i) => (
                <Skeleton key={i} className="h-20 w-full rounded-lg" />
              ))}
            </div>
          ) : entries && entries.length > 0 ? (
            <div className="space-y-3">
              {entries.map((entry: any) => (
                <div
                  key={entry.id}
                  className="flex items-center gap-4 rounded-lg border p-3"
                >
                  <UserCheck className="h-5 w-5 text-muted-foreground shrink-0" />
                  <div className="flex-1 min-w-0">
                    <div className="text-sm font-medium">
                      {entry.user_name}{" "}
                      <span className="text-muted-foreground font-normal">
                        ({entry.user_email})
                      </span>
                    </div>
                    <div className="mt-1 text-xs text-muted-foreground">
                      {entry.system_name}
                      {entry.resource && ` / ${entry.resource}`}
                      {entry.current_access &&
                        ` - ${entry.current_access}`}
                    </div>
                  </div>
                  <Badge
                    className={
                      decisionColor[entry.decision || "pending"] || ""
                    }
                  >
                    {entry.decision || "pending"}
                  </Badge>
                  {(!entry.decision || entry.decision === "pending") && (
                    <div className="flex gap-1">
                      <Button
                        size="sm"
                        variant="outline"
                        className="gap-1 text-green-600 hover:text-green-700"
                        onClick={() =>
                          handleDecision(entry.id, "approved")
                        }
                        disabled={updateEntry.isPending}
                      >
                        <CheckCircle className="h-4 w-4" />
                        Approve
                      </Button>
                      <Button
                        size="sm"
                        variant="outline"
                        className="gap-1 text-red-600 hover:text-red-700"
                        onClick={() =>
                          handleDecision(entry.id, "revoked")
                        }
                        disabled={updateEntry.isPending}
                      >
                        <XCircle className="h-4 w-4" />
                        Revoke
                      </Button>
                    </div>
                  )}
                </div>
              ))}
            </div>
          ) : (
            <div className="flex flex-col items-center justify-center py-6 text-center">
              <ShieldCheck className="h-10 w-10 text-muted-foreground mb-3" />
              <p className="text-sm text-muted-foreground">
                No entries in this campaign yet.
              </p>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}

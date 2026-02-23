"use client";

import { useState } from "react";
import { useParams } from "next/navigation";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Skeleton } from "@/components/ui/skeleton";
import { usePolicy, useUpdatePolicy } from "@/hooks/use-api";

const DEMO_ORG_ID = "00000000-0000-0000-0000-000000000000";

const statusVariant: Record<string, "default" | "secondary" | "success" | "destructive" | "outline"> = {
  draft: "secondary",
  in_review: "default",
  approved: "success",
  published: "success",
  archived: "outline",
};

const statusTransitions: Record<string, { label: string; nextStatus: string }[]> = {
  draft: [{ label: "Submit for Review", nextStatus: "in_review" }],
  in_review: [
    { label: "Approve", nextStatus: "approved" },
    { label: "Return to Draft", nextStatus: "draft" },
  ],
  approved: [{ label: "Publish", nextStatus: "published" }],
  published: [{ label: "Archive", nextStatus: "archived" }],
  archived: [{ label: "Reactivate as Draft", nextStatus: "draft" }],
};

export default function PolicyDetailPage() {
  const params = useParams();
  const policyId = params.id as string;
  const { data: policy, isLoading } = usePolicy(DEMO_ORG_ID, policyId);
  const updatePolicy = useUpdatePolicy(DEMO_ORG_ID);
  const [editing, setEditing] = useState(false);
  const [editContent, setEditContent] = useState("");

  if (isLoading) {
    return (
      <div className="space-y-4">
        <Skeleton className="h-10 w-64" />
        <Skeleton className="h-64 w-full" />
      </div>
    );
  }

  if (!policy) return <p>Policy not found.</p>;

  function handleStatusChange(nextStatus: string) {
    updatePolicy.mutate({ policyId, status: nextStatus });
  }

  function handleStartEdit() {
    setEditContent(policy!.content || "");
    setEditing(true);
  }

  function handleSaveContent() {
    updatePolicy.mutate(
      { policyId, content: editContent },
      { onSuccess: () => setEditing(false) }
    );
  }

  const transitions = statusTransitions[policy.status] || [];

  return (
    <div className="space-y-6">
      <div>
        <div className="flex items-center gap-3">
          <h1 className="text-3xl font-bold">{policy.title}</h1>
          <Badge variant={statusVariant[policy.status] || "secondary"}>
            {policy.status.replace(/_/g, " ")}
          </Badge>
          <Badge variant="outline">v{policy.version}</Badge>
        </div>
        <p className="mt-1 text-muted-foreground">
          Created {new Date(policy.created_at).toLocaleDateString()}
          {policy.published_at &&
            ` · Published ${new Date(policy.published_at).toLocaleDateString()}`}
          {policy.next_review_date &&
            ` · Next review ${new Date(policy.next_review_date).toLocaleDateString()}`}
        </p>
        {transitions.length > 0 && (
          <div className="mt-3 flex gap-2">
            {transitions.map((t) => (
              <Button
                key={t.nextStatus}
                size="sm"
                variant={t.nextStatus === "draft" ? "outline" : "default"}
                onClick={() => handleStatusChange(t.nextStatus)}
                disabled={updatePolicy.isPending}
              >
                {t.label}
              </Button>
            ))}
          </div>
        )}
      </div>

      <Tabs defaultValue="overview">
        <TabsList>
          <TabsTrigger value="overview">Overview</TabsTrigger>
          <TabsTrigger value="controls">Linked Controls</TabsTrigger>
          <TabsTrigger value="settings">Settings</TabsTrigger>
        </TabsList>

        <TabsContent value="overview">
          <Card>
            <CardHeader className="flex flex-row items-center justify-between">
              <CardTitle>Policy Content</CardTitle>
              {!editing && (
                <Button variant="outline" size="sm" onClick={handleStartEdit}>
                  Edit
                </Button>
              )}
            </CardHeader>
            <CardContent>
              {editing ? (
                <div className="space-y-3">
                  <textarea
                    className="w-full min-h-[400px] rounded-md border bg-background p-3 text-sm font-mono"
                    value={editContent}
                    onChange={(e) => setEditContent(e.target.value)}
                  />
                  <div className="flex gap-2">
                    <Button
                      size="sm"
                      onClick={handleSaveContent}
                      disabled={updatePolicy.isPending}
                    >
                      Save
                    </Button>
                    <Button
                      size="sm"
                      variant="outline"
                      onClick={() => setEditing(false)}
                    >
                      Cancel
                    </Button>
                  </div>
                </div>
              ) : (
                <div className="prose prose-sm dark:prose-invert max-w-none whitespace-pre-wrap">
                  {policy.content || "No content yet. Click Edit to add policy content."}
                </div>
              )}
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="controls">
          <Card>
            <CardHeader>
              <CardTitle>Linked Controls</CardTitle>
            </CardHeader>
            <CardContent>
              {policy.control_ids && policy.control_ids.length > 0 ? (
                <div className="space-y-2">
                  {policy.control_ids.map((controlId) => (
                    <div
                      key={controlId}
                      className="flex items-center gap-2 rounded-lg border p-3 text-sm"
                    >
                      <span className="font-mono text-xs text-muted-foreground">
                        {controlId.slice(0, 8)}...
                      </span>
                    </div>
                  ))}
                </div>
              ) : (
                <p className="text-sm text-muted-foreground">
                  No controls linked to this policy.
                </p>
              )}
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="settings">
          <Card>
            <CardHeader>
              <CardTitle>Policy Metadata</CardTitle>
            </CardHeader>
            <CardContent>
              <dl className="grid grid-cols-2 gap-4 text-sm">
                <div>
                  <dt className="font-medium text-muted-foreground">Version</dt>
                  <dd>{policy.version}</dd>
                </div>
                <div>
                  <dt className="font-medium text-muted-foreground">Status</dt>
                  <dd className="capitalize">{policy.status.replace(/_/g, " ")}</dd>
                </div>
                <div>
                  <dt className="font-medium text-muted-foreground">Created</dt>
                  <dd>{new Date(policy.created_at).toLocaleDateString()}</dd>
                </div>
                <div>
                  <dt className="font-medium text-muted-foreground">Last Updated</dt>
                  <dd>{new Date(policy.updated_at).toLocaleDateString()}</dd>
                </div>
                {policy.approved_at && (
                  <div>
                    <dt className="font-medium text-muted-foreground">Approved</dt>
                    <dd>{new Date(policy.approved_at).toLocaleDateString()}</dd>
                  </div>
                )}
                {policy.published_at && (
                  <div>
                    <dt className="font-medium text-muted-foreground">Published</dt>
                    <dd>{new Date(policy.published_at).toLocaleDateString()}</dd>
                  </div>
                )}
                {policy.next_review_date && (
                  <div>
                    <dt className="font-medium text-muted-foreground">Next Review</dt>
                    <dd>{new Date(policy.next_review_date).toLocaleDateString()}</dd>
                  </div>
                )}
                <div>
                  <dt className="font-medium text-muted-foreground">Frameworks</dt>
                  <dd>
                    {policy.framework_ids && policy.framework_ids.length > 0
                      ? `${policy.framework_ids.length} framework(s)`
                      : "None"}
                  </dd>
                </div>
              </dl>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
}

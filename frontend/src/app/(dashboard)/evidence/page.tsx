"use client";

import { useState, useRef } from "react";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Skeleton } from "@/components/ui/skeleton";
import { useEvidence, useCreateEvidence, useUploadEvidence } from "@/hooks/use-api";
import { useOrgId } from "@/hooks/use-org-id";
import {
  Shield,
  FileCheck,
  AlertTriangle,
  Upload,
  Plus,
  Loader2,
  FileUp,
  Download,
} from "lucide-react";

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

const statusBadgeVariant: Record<
  string,
  "default" | "secondary" | "success" | "destructive" | "outline"
> = {
  pending: "secondary",
  collected: "success",
  valid: "success",
  expired: "destructive",
  invalid: "destructive",
};

const methodBadgeVariant: Record<string, "default" | "secondary" | "outline"> =
  {
    manual: "outline",
    automated: "default",
    api: "secondary",
  };

export default function EvidencePage() {
  const orgId = useOrgId();
  const [statusFilter, setStatusFilter] = useState<string | undefined>(
    undefined
  );
  const [methodFilter, setMethodFilter] = useState<string | undefined>(
    undefined
  );
  const [showCreate, setShowCreate] = useState(false);
  const [createTitle, setCreateTitle] = useState("");
  const [uploadingId, setUploadingId] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const { data, isLoading, error } = useEvidence(orgId);
  const createEvidence = useCreateEvidence(orgId);
  const uploadEvidence = useUploadEvidence(orgId);

  const allItems = data?.items || [];

  const evidenceItems = allItems.filter((item) => {
    if (statusFilter && item.status !== statusFilter) return false;
    if (methodFilter && item.collection_method !== methodFilter) return false;
    return true;
  });

  function handleCreate() {
    if (!createTitle.trim()) return;
    createEvidence.mutate(
      { title: createTitle, status: "pending", collection_method: "manual" },
      {
        onSuccess: () => {
          setCreateTitle("");
          setShowCreate(false);
        },
      }
    );
  }

  function handleUploadClick(evidenceId: string) {
    setUploadingId(evidenceId);
    fileInputRef.current?.click();
  }

  function handleFileSelected(e: React.ChangeEvent<HTMLInputElement>) {
    const file = e.target.files?.[0];
    if (!file || !uploadingId) return;
    uploadEvidence.mutate(
      { evidenceId: uploadingId, file },
      {
        onSettled: () => {
          setUploadingId(null);
          if (fileInputRef.current) fileInputRef.current.value = "";
        },
      }
    );
  }

  const apiUrl =
    process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

  if (error) {
    return (
      <div className="space-y-6">
        <div>
          <h1 className="text-3xl font-bold">Evidence Library</h1>
          <p className="text-muted-foreground">
            Track evidence collection status
          </p>
        </div>
        <Card className="border-destructive">
          <CardContent className="flex flex-col items-center justify-center p-12 text-center">
            <AlertTriangle className="h-12 w-12 text-destructive mb-4" />
            <h3 className="text-lg font-semibold">Failed to load evidence</h3>
            <p className="text-sm text-muted-foreground mt-2">
              {error.message ||
                "An unexpected error occurred. Please try again later."}
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
      {/* Hidden file input for uploads */}
      <input
        ref={fileInputRef}
        type="file"
        className="hidden"
        onChange={handleFileSelected}
        accept=".pdf,.png,.jpg,.jpeg,.csv,.xlsx,.docx,.txt,.json,.zip"
      />

      {/* Page header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold">Evidence Library</h1>
          <p className="text-muted-foreground">
            Track evidence collection status
          </p>
        </div>
        <Button onClick={() => setShowCreate((v) => !v)}>
          <Plus className="mr-2 h-4 w-4" />
          Add Evidence
        </Button>
      </div>

      {/* Create evidence form */}
      {showCreate && (
        <Card>
          <CardContent className="p-4 space-y-3">
            <div>
              <label className="text-sm font-medium">Evidence Title</label>
              <input
                type="text"
                className="mt-1 w-full rounded-md border bg-background p-2 text-sm"
                placeholder="e.g., MFA Enrollment Screenshot"
                value={createTitle}
                onChange={(e) => setCreateTitle(e.target.value)}
              />
            </div>
            <div className="flex gap-2">
              <Button
                size="sm"
                onClick={handleCreate}
                disabled={!createTitle.trim() || createEvidence.isPending}
              >
                {createEvidence.isPending && (
                  <Loader2 className="mr-1 h-4 w-4 animate-spin" />
                )}
                Create
              </Button>
              <Button
                size="sm"
                variant="ghost"
                onClick={() => setShowCreate(false)}
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
            <Card
              key={evidence.id}
              className="transition-colors hover:bg-muted/50"
            >
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
                    {evidence.file_name && (
                      <>
                        <span>&middot;</span>
                        <FileUp className="h-3 w-3 inline" />
                        <span>{evidence.file_name}</span>
                      </>
                    )}
                  </div>
                </div>
                <div className="flex items-center gap-2 shrink-0">
                  {/* Upload / Download button */}
                  {evidence.file_url ? (
                    <a
                      href={`${apiUrl}/api/v1/organizations/${orgId}/evidence/${evidence.id}/download`}
                      target="_blank"
                      rel="noopener noreferrer"
                    >
                      <Button size="sm" variant="outline">
                        <Download className="mr-1 h-4 w-4" />
                        Download
                      </Button>
                    </a>
                  ) : (
                    <Button
                      size="sm"
                      variant="outline"
                      onClick={() => handleUploadClick(evidence.id)}
                      disabled={
                        uploadEvidence.isPending && uploadingId === evidence.id
                      }
                    >
                      {uploadEvidence.isPending &&
                      uploadingId === evidence.id ? (
                        <Loader2 className="mr-1 h-4 w-4 animate-spin" />
                      ) : (
                        <Upload className="mr-1 h-4 w-4" />
                      )}
                      Upload
                    </Button>
                  )}
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
              No evidence items match the current filters, or the evidence
              library is empty.
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

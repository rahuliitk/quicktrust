"use client";

import { useState, useCallback, useEffect } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Skeleton } from "@/components/ui/skeleton";
import {
  Shield,
  ShieldCheck,
  FileText,
  AlertTriangle,
  LogIn,
  KeyRound,
  ClipboardCheck,
} from "lucide-react";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
const BASE = `${API_URL}/api/v1/auditor/portal`;

type TabValue = "overview" | "controls" | "evidence" | "policies" | "risks";

interface PortalOverview {
  audit: {
    id: string;
    title: string;
    audit_type: string;
    status: string;
    auditor_firm: string | null;
    lead_auditor_name: string | null;
    scheduled_start: string | null;
    scheduled_end: string | null;
  };
  readiness: {
    overall_score: number;
    controls_score: number;
    evidence_score: number;
    policies_score: number;
    risks_score: number;
  };
}

interface PortalControl {
  id: string;
  title: string;
  description: string | null;
  status: string;
  automation_level: string;
  effectiveness: string | null;
}

interface PortalEvidence {
  id: string;
  title: string;
  status: string;
  collected_at: string | null;
  collection_method: string;
  expires_at: string | null;
}

interface PortalPolicy {
  id: string;
  title: string;
  status: string;
  version: string;
  published_at: string | null;
}

interface PortalRisk {
  id: string;
  title: string;
  category: string;
  risk_level: string;
  risk_score: number;
  status: string;
  treatment_type: string | null;
}

async function portalFetch<T>(path: string, token: string): Promise<T> {
  const res = await fetch(`${BASE}${path}`, {
    headers: {
      "Content-Type": "application/json",
      "X-Auditor-Token": token,
    },
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(err.detail || `Portal API error: ${res.status}`);
  }
  return res.json();
}

export default function AuditorPortalPage() {
  const [tokenInput, setTokenInput] = useState("");
  const [token, setToken] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [authenticating, setAuthenticating] = useState(false);

  const [activeTab, setActiveTab] = useState<TabValue>("overview");

  const handleAccess = useCallback(async () => {
    const trimmed = tokenInput.trim();
    if (!trimmed) return;
    setError(null);
    setAuthenticating(true);
    try {
      // Validate token by fetching overview
      await portalFetch("/overview", trimmed);
      setToken(trimmed);
    } catch (err: any) {
      setError(err.message || "Invalid or expired token");
    } finally {
      setAuthenticating(false);
    }
  }, [tokenInput]);

  if (!token) {
    return <LoginPanel
      tokenInput={tokenInput}
      setTokenInput={setTokenInput}
      onAccess={handleAccess}
      authenticating={authenticating}
      error={error}
    />;
  }

  const tabs: { value: TabValue; label: string; icon: React.ReactNode }[] = [
    { value: "overview", label: "Overview", icon: <ClipboardCheck className="h-4 w-4" /> },
    { value: "controls", label: "Controls", icon: <ShieldCheck className="h-4 w-4" /> },
    { value: "evidence", label: "Evidence", icon: <Shield className="h-4 w-4" /> },
    { value: "policies", label: "Policies", icon: <FileText className="h-4 w-4" /> },
    { value: "risks", label: "Risks", icon: <AlertTriangle className="h-4 w-4" /> },
  ];

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold">Auditor Portal</h1>
          <p className="text-muted-foreground">
            Read-only view of audit materials
          </p>
        </div>
        <Button
          variant="outline"
          size="sm"
          onClick={() => {
            setToken(null);
            setTokenInput("");
            setActiveTab("overview");
          }}
        >
          <KeyRound className="mr-2 h-4 w-4" />
          Change Token
        </Button>
      </div>

      {/* Tab buttons */}
      <div className="flex gap-2 border-b pb-1">
        {tabs.map((tab) => (
          <Button
            key={tab.value}
            variant={activeTab === tab.value ? "default" : "ghost"}
            size="sm"
            onClick={() => setActiveTab(tab.value)}
            className="gap-1.5"
          >
            {tab.icon}
            {tab.label}
          </Button>
        ))}
      </div>

      {/* Tab content */}
      {activeTab === "overview" && <OverviewPanel token={token} />}
      {activeTab === "controls" && <ControlsPanel token={token} />}
      {activeTab === "evidence" && <EvidencePanel token={token} />}
      {activeTab === "policies" && <PoliciesPanel token={token} />}
      {activeTab === "risks" && <RisksPanel token={token} />}
    </div>
  );
}

/* ------------------------------------------------------------------ */
/* Login Panel                                                         */
/* ------------------------------------------------------------------ */

function LoginPanel({
  tokenInput,
  setTokenInput,
  onAccess,
  authenticating,
  error,
}: {
  tokenInput: string;
  setTokenInput: (v: string) => void;
  onAccess: () => void;
  authenticating: boolean;
  error: string | null;
}) {
  return (
    <div className="flex items-center justify-center min-h-[60vh]">
      <Card className="w-full max-w-md">
        <CardHeader className="text-center">
          <div className="mx-auto mb-4 flex h-14 w-14 items-center justify-center rounded-full bg-primary/10">
            <LogIn className="h-7 w-7 text-primary" />
          </div>
          <CardTitle className="text-xl">Auditor Access</CardTitle>
          <p className="mt-2 text-sm text-muted-foreground">
            Enter your auditor access token to view audit materials
          </p>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div>
              <label
                htmlFor="auditor-token"
                className="block text-sm font-medium mb-1.5"
              >
                Access Token
              </label>
              <input
                id="auditor-token"
                type="text"
                value={tokenInput}
                onChange={(e) => setTokenInput(e.target.value)}
                onKeyDown={(e) => {
                  if (e.key === "Enter") onAccess();
                }}
                placeholder="Paste your token here"
                className="w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
              />
            </div>
            {error && (
              <p className="text-sm text-destructive">{error}</p>
            )}
            <Button
              className="w-full"
              onClick={onAccess}
              disabled={authenticating || !tokenInput.trim()}
            >
              {authenticating ? "Validating..." : "Access Portal"}
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}

/* ------------------------------------------------------------------ */
/* Generic fetch hook for portal panels                                */
/* ------------------------------------------------------------------ */

function usePortalData<T>(path: string, token: string) {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;
    setLoading(true);
    setError(null);
    portalFetch<T>(path, token)
      .then((result) => {
        if (!cancelled) setData(result);
      })
      .catch((err) => {
        if (!cancelled) setError(err.message);
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });
    return () => {
      cancelled = true;
    };
  }, [path, token]);

  return { data, loading, error };
}

/* ------------------------------------------------------------------ */
/* Overview Panel                                                      */
/* ------------------------------------------------------------------ */

function OverviewPanel({ token }: { token: string }) {
  const { data, loading, error } = usePortalData<PortalOverview>(
    "/overview",
    token
  );

  if (loading) {
    return (
      <div className="space-y-4">
        <Skeleton className="h-32 w-full rounded-xl" />
        <Skeleton className="h-32 w-full rounded-xl" />
      </div>
    );
  }

  if (error) return <ErrorCard message={error} />;
  if (!data) return null;

  const { audit, readiness } = data;

  return (
    <div className="grid gap-6 md:grid-cols-2">
      <Card>
        <CardHeader>
          <CardTitle>Audit Information</CardTitle>
        </CardHeader>
        <CardContent>
          <dl className="space-y-4 text-sm">
            <div>
              <dt className="font-medium text-muted-foreground">Title</dt>
              <dd className="mt-1">{audit.title}</dd>
            </div>
            <div>
              <dt className="font-medium text-muted-foreground">Type</dt>
              <dd className="mt-1 capitalize">{audit.audit_type}</dd>
            </div>
            <div>
              <dt className="font-medium text-muted-foreground">Status</dt>
              <dd className="mt-1">
                <Badge variant="outline" className="capitalize">
                  {audit.status}
                </Badge>
              </dd>
            </div>
            <div>
              <dt className="font-medium text-muted-foreground">
                Auditor Firm
              </dt>
              <dd className="mt-1">{audit.auditor_firm || "Not specified"}</dd>
            </div>
            <div>
              <dt className="font-medium text-muted-foreground">
                Lead Auditor
              </dt>
              <dd className="mt-1">
                {audit.lead_auditor_name || "Not specified"}
              </dd>
            </div>
            {audit.scheduled_start && (
              <div>
                <dt className="font-medium text-muted-foreground">Schedule</dt>
                <dd className="mt-1">
                  {new Date(audit.scheduled_start).toLocaleDateString()}
                  {audit.scheduled_end &&
                    ` - ${new Date(audit.scheduled_end).toLocaleDateString()}`}
                </dd>
              </div>
            )}
          </dl>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Readiness Scores</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div className="text-center">
              <div className="text-4xl font-bold">
                {Math.round(readiness.overall_score)}%
              </div>
              <div className="text-sm text-muted-foreground">Overall Score</div>
            </div>
            <div className="space-y-3">
              <ScoreBar label="Controls" score={readiness.controls_score} />
              <ScoreBar label="Evidence" score={readiness.evidence_score} />
              <ScoreBar label="Policies" score={readiness.policies_score} />
              <ScoreBar label="Risks" score={readiness.risks_score} />
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}

function ScoreBar({ label, score }: { label: string; score: number }) {
  const rounded = Math.round(score);
  return (
    <div className="space-y-1">
      <div className="flex justify-between text-sm">
        <span className="text-muted-foreground">{label}</span>
        <span className="font-medium">{rounded}%</span>
      </div>
      <div className="h-2 rounded-full bg-primary/20 overflow-hidden">
        <div
          className={`h-full rounded-full transition-all ${
            rounded >= 80
              ? "bg-green-500"
              : rounded >= 50
              ? "bg-yellow-500"
              : "bg-red-500"
          }`}
          style={{ width: `${rounded}%` }}
        />
      </div>
    </div>
  );
}

/* ------------------------------------------------------------------ */
/* Controls Panel                                                      */
/* ------------------------------------------------------------------ */

function ControlsPanel({ token }: { token: string }) {
  const { data, loading, error } = usePortalData<PortalControl[]>(
    "/controls",
    token
  );

  if (loading) return <ListSkeleton />;
  if (error) return <ErrorCard message={error} />;
  if (!data || data.length === 0) {
    return <EmptyCard icon={ShieldCheck} message="No controls available." />;
  }

  const statusVariant: Record<string, "success" | "warning" | "secondary" | "destructive"> = {
    implemented: "success",
    partially_implemented: "warning",
    draft: "secondary",
    not_implemented: "destructive",
  };

  return (
    <div className="space-y-3">
      {data.map((control) => (
        <Card key={control.id}>
          <CardContent className="flex items-center gap-4 p-4">
            <ShieldCheck className="h-5 w-5 text-muted-foreground shrink-0" />
            <div className="flex-1 min-w-0">
              <div className="font-medium text-sm">{control.title}</div>
              {control.description && (
                <p className="mt-1 text-xs text-muted-foreground line-clamp-2">
                  {control.description}
                </p>
              )}
            </div>
            <div className="flex items-center gap-2 shrink-0">
              <Badge variant="outline">{control.automation_level}</Badge>
              <Badge
                variant={
                  (statusVariant[control.status] || "secondary") as any
                }
              >
                {control.status.replace(/_/g, " ")}
              </Badge>
            </div>
          </CardContent>
        </Card>
      ))}
    </div>
  );
}

/* ------------------------------------------------------------------ */
/* Evidence Panel                                                      */
/* ------------------------------------------------------------------ */

function EvidencePanel({ token }: { token: string }) {
  const { data, loading, error } = usePortalData<PortalEvidence[]>(
    "/evidence",
    token
  );

  if (loading) return <ListSkeleton />;
  if (error) return <ErrorCard message={error} />;
  if (!data || data.length === 0) {
    return <EmptyCard icon={Shield} message="No evidence available." />;
  }

  const evidenceStatusVariant: Record<string, "success" | "warning" | "secondary"> = {
    valid: "success",
    expired: "warning",
    pending: "secondary",
  };

  return (
    <div className="space-y-3">
      {data.map((evidence) => (
        <Card key={evidence.id}>
          <CardContent className="flex items-center gap-4 p-4">
            <Shield className="h-5 w-5 text-muted-foreground shrink-0" />
            <div className="flex-1 min-w-0">
              <div className="font-medium text-sm">{evidence.title}</div>
              <div className="mt-1 flex flex-wrap items-center gap-2 text-xs text-muted-foreground">
                <span className="capitalize">
                  {evidence.collection_method}
                </span>
                {evidence.collected_at && (
                  <span>
                    Collected:{" "}
                    {new Date(evidence.collected_at).toLocaleDateString()}
                  </span>
                )}
                {evidence.expires_at && (
                  <span>
                    Expires:{" "}
                    {new Date(evidence.expires_at).toLocaleDateString()}
                  </span>
                )}
              </div>
            </div>
            <Badge
              variant={
                (evidenceStatusVariant[evidence.status] || "secondary") as any
              }
            >
              {evidence.status}
            </Badge>
          </CardContent>
        </Card>
      ))}
    </div>
  );
}

/* ------------------------------------------------------------------ */
/* Policies Panel                                                      */
/* ------------------------------------------------------------------ */

function PoliciesPanel({ token }: { token: string }) {
  const { data, loading, error } = usePortalData<PortalPolicy[]>(
    "/policies",
    token
  );

  if (loading) return <ListSkeleton />;
  if (error) return <ErrorCard message={error} />;
  if (!data || data.length === 0) {
    return <EmptyCard icon={FileText} message="No policies available." />;
  }

  const policyStatusVariant: Record<string, "success" | "secondary" | "warning" | "default"> = {
    published: "success",
    approved: "success",
    draft: "secondary",
    in_review: "warning",
  };

  return (
    <div className="space-y-3">
      {data.map((policy) => (
        <Card key={policy.id}>
          <CardContent className="flex items-center gap-4 p-4">
            <FileText className="h-5 w-5 text-muted-foreground shrink-0" />
            <div className="flex-1 min-w-0">
              <div className="font-medium text-sm">{policy.title}</div>
              <div className="mt-1 flex flex-wrap items-center gap-2 text-xs text-muted-foreground">
                <span>v{policy.version}</span>
                {policy.published_at && (
                  <span>
                    Published:{" "}
                    {new Date(policy.published_at).toLocaleDateString()}
                  </span>
                )}
              </div>
            </div>
            <Badge
              variant={
                (policyStatusVariant[policy.status] || "secondary") as any
              }
            >
              {policy.status.replace(/_/g, " ")}
            </Badge>
          </CardContent>
        </Card>
      ))}
    </div>
  );
}

/* ------------------------------------------------------------------ */
/* Risks Panel                                                         */
/* ------------------------------------------------------------------ */

function RisksPanel({ token }: { token: string }) {
  const { data, loading, error } = usePortalData<PortalRisk[]>(
    "/risks",
    token
  );

  if (loading) return <ListSkeleton />;
  if (error) return <ErrorCard message={error} />;
  if (!data || data.length === 0) {
    return <EmptyCard icon={AlertTriangle} message="No risks available." />;
  }

  const riskLevelColor: Record<string, string> = {
    critical: "bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-100",
    high: "bg-orange-100 text-orange-800 dark:bg-orange-900 dark:text-orange-100",
    medium: "bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-100",
    low: "bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-100",
  };

  return (
    <div className="space-y-3">
      {data.map((risk) => (
        <Card key={risk.id}>
          <CardContent className="flex items-center gap-4 p-4">
            <AlertTriangle className="h-5 w-5 text-muted-foreground shrink-0" />
            <div className="flex-1 min-w-0">
              <div className="font-medium text-sm">{risk.title}</div>
              <div className="mt-1 flex flex-wrap items-center gap-2 text-xs text-muted-foreground">
                <span className="capitalize">{risk.category}</span>
                <span>Score: {risk.risk_score}</span>
                {risk.treatment_type && (
                  <span className="capitalize">
                    Treatment: {risk.treatment_type}
                  </span>
                )}
              </div>
            </div>
            <div className="flex items-center gap-2 shrink-0">
              <Badge className={riskLevelColor[risk.risk_level] || ""}>
                {risk.risk_level}
              </Badge>
              <Badge variant="outline" className="capitalize">
                {risk.status}
              </Badge>
            </div>
          </CardContent>
        </Card>
      ))}
    </div>
  );
}

/* ------------------------------------------------------------------ */
/* Shared small components                                             */
/* ------------------------------------------------------------------ */

function ListSkeleton() {
  return (
    <div className="space-y-3">
      {[1, 2, 3, 4, 5].map((i) => (
        <Skeleton key={i} className="h-20 w-full rounded-xl" />
      ))}
    </div>
  );
}

function ErrorCard({ message }: { message: string }) {
  return (
    <Card>
      <CardContent className="p-8 text-center">
        <AlertTriangle className="mx-auto h-10 w-10 text-destructive" />
        <p className="mt-3 text-sm text-destructive">{message}</p>
      </CardContent>
    </Card>
  );
}

function EmptyCard({
  icon: Icon,
  message,
}: {
  icon: React.ComponentType<{ className?: string }>;
  message: string;
}) {
  return (
    <Card>
      <CardContent className="p-12 text-center">
        <Icon className="mx-auto h-12 w-12 text-muted-foreground" />
        <p className="mt-4 text-sm text-muted-foreground">{message}</p>
      </CardContent>
    </Card>
  );
}

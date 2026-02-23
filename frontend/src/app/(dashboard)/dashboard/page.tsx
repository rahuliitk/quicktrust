"use client";

import Link from "next/link";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { Button } from "@/components/ui/button";
import {
  useControlStats,
  useFrameworks,
  useAgentRuns,
  usePolicyStats,
  useRiskStats,
  useLatestOnboarding,
} from "@/hooks/use-api";
import { Skeleton } from "@/components/ui/skeleton";
import { Shield, ListChecks, Bot, CheckCircle, FileText, AlertTriangle, Rocket } from "lucide-react";

// Hardcoded org ID for demo — in production, this comes from auth context
const DEMO_ORG_ID = "00000000-0000-0000-0000-000000000000";

export default function DashboardPage() {
  const { data: stats, isLoading: statsLoading } = useControlStats(DEMO_ORG_ID);
  const { data: frameworks, isLoading: fwLoading } = useFrameworks();
  const { data: agentRuns, isLoading: runsLoading } = useAgentRuns(DEMO_ORG_ID);
  const { data: policyStats, isLoading: policyLoading } = usePolicyStats(DEMO_ORG_ID);
  const { data: riskStats, isLoading: riskLoading } = useRiskStats(DEMO_ORG_ID);
  const { data: latestOnboarding } = useLatestOnboarding(DEMO_ORG_ID);

  const complianceScore = stats
    ? stats.total > 0
      ? Math.round((stats.implemented / stats.total) * 100)
      : 0
    : 0;

  const showGetStarted = !latestOnboarding || latestOnboarding.status === "failed";

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold">Dashboard</h1>
        <p className="text-muted-foreground">Your compliance posture at a glance</p>
      </div>

      {/* Get Started CTA */}
      {showGetStarted && (
        <Card className="border-primary/50 bg-primary/5">
          <CardContent className="flex items-center justify-between p-6">
            <div className="flex items-center gap-4">
              <Rocket className="h-8 w-8 text-primary" />
              <div>
                <h3 className="text-lg font-semibold">Get Started with QuickTrust</h3>
                <p className="text-sm text-muted-foreground">
                  Launch the onboarding wizard to auto-generate controls, policies, and evidence for your organization.
                </p>
              </div>
            </div>
            <Link href="/onboarding">
              <Button>Start Setup</Button>
            </Link>
          </CardContent>
        </Card>
      )}

      {/* Top-level stats */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-6">
        <Link href="/controls">
          <Card className="transition-colors hover:bg-muted/50 cursor-pointer">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Compliance Score</CardTitle>
              <CheckCircle className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              {statsLoading ? (
                <Skeleton className="h-8 w-20" />
              ) : (
                <>
                  <div className="text-2xl font-bold">{complianceScore}%</div>
                  <Progress value={complianceScore} className="mt-2" />
                </>
              )}
            </CardContent>
          </Card>
        </Link>

        <Link href="/controls">
          <Card className="transition-colors hover:bg-muted/50 cursor-pointer">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Total Controls</CardTitle>
              <ListChecks className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              {statsLoading ? (
                <Skeleton className="h-8 w-16" />
              ) : (
                <div className="text-2xl font-bold">{stats?.total || 0}</div>
              )}
            </CardContent>
          </Card>
        </Link>

        <Link href="/frameworks">
          <Card className="transition-colors hover:bg-muted/50 cursor-pointer">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Frameworks</CardTitle>
              <Shield className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              {fwLoading ? (
                <Skeleton className="h-8 w-8" />
              ) : (
                <div className="text-2xl font-bold">{frameworks?.length || 0}</div>
              )}
            </CardContent>
          </Card>
        </Link>

        <Link href="/policies">
          <Card className="transition-colors hover:bg-muted/50 cursor-pointer">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Policies</CardTitle>
              <FileText className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              {policyLoading ? (
                <Skeleton className="h-8 w-8" />
              ) : (
                <div className="text-2xl font-bold">{policyStats?.published || 0}</div>
              )}
              <p className="text-xs text-muted-foreground">published</p>
            </CardContent>
          </Card>
        </Link>

        <Link href="/risks">
          <Card className="transition-colors hover:bg-muted/50 cursor-pointer">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Open Risks</CardTitle>
              <AlertTriangle className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              {riskLoading ? (
                <Skeleton className="h-8 w-8" />
              ) : (
                <>
                  <div className="text-2xl font-bold">{riskStats?.total || 0}</div>
                  {riskStats && riskStats.by_risk_level?.critical > 0 && (
                    <p className="text-xs text-red-500">
                      {riskStats.by_risk_level.critical} critical
                    </p>
                  )}
                </>
              )}
            </CardContent>
          </Card>
        </Link>

        <Link href="/agents/controls-generation">
          <Card className="transition-colors hover:bg-muted/50 cursor-pointer">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Agent Runs</CardTitle>
              <Bot className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              {runsLoading ? (
                <Skeleton className="h-8 w-8" />
              ) : (
                <div className="text-2xl font-bold">{agentRuns?.total || 0}</div>
              )}
            </CardContent>
          </Card>
        </Link>
      </div>

      {/* Controls breakdown */}
      <div className="grid gap-4 md:grid-cols-2">
        <Card>
          <CardHeader>
            <Link href="/controls"><CardTitle className="hover:underline">Controls by Status</CardTitle></Link>
          </CardHeader>
          <CardContent>
            {statsLoading ? (
              <div className="space-y-3">
                {[1, 2, 3, 4].map((i) => (
                  <Skeleton key={i} className="h-6 w-full" />
                ))}
              </div>
            ) : (
              <div className="space-y-3">
                <StatusBar label="Implemented" count={stats?.implemented || 0} total={stats?.total || 1} color="bg-green-500" />
                <StatusBar label="Draft" count={stats?.draft || 0} total={stats?.total || 1} color="bg-blue-500" />
                <StatusBar label="Partially Implemented" count={stats?.partially_implemented || 0} total={stats?.total || 1} color="bg-yellow-500" />
                <StatusBar label="Not Implemented" count={stats?.not_implemented || 0} total={stats?.total || 1} color="bg-red-500" />
                <StatusBar label="Not Applicable" count={stats?.not_applicable || 0} total={stats?.total || 1} color="bg-gray-400" />
              </div>
            )}
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <Link href="/frameworks"><CardTitle className="hover:underline">Frameworks</CardTitle></Link>
          </CardHeader>
          <CardContent>
            {fwLoading ? (
              <Skeleton className="h-20 w-full" />
            ) : frameworks && frameworks.length > 0 ? (
              <div className="space-y-3">
                {frameworks.map((fw) => (
                  <div key={fw.id} className="flex items-center justify-between rounded-lg border p-3">
                    <div>
                      <div className="font-medium">{fw.name}</div>
                      <div className="text-xs text-muted-foreground">Version {fw.version}</div>
                    </div>
                    <Badge variant={fw.is_active ? "success" : "secondary"}>
                      {fw.is_active ? "Active" : "Inactive"}
                    </Badge>
                  </div>
                ))}
              </div>
            ) : (
              <p className="text-sm text-muted-foreground">
                No frameworks loaded. Run the seed script to load SOC 2.
              </p>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  );
}

function StatusBar({
  label,
  count,
  total,
  color,
}: {
  label: string;
  count: number;
  total: number;
  color: string;
}) {
  const pct = total > 0 ? Math.round((count / total) * 100) : 0;
  return (
    <div className="space-y-1">
      <div className="flex items-center justify-between text-sm">
        <span>{label}</span>
        <span className="text-muted-foreground">
          {count} ({pct}%)
        </span>
      </div>
      <div className="h-2 w-full rounded-full bg-muted">
        <div className={`h-full rounded-full ${color}`} style={{ width: `${pct}%` }} />
      </div>
    </div>
  );
}

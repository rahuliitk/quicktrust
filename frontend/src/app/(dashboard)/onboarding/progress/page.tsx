"use client";

import { Suspense } from "react";
import { useSearchParams } from "next/navigation";
import Link from "next/link";
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
  CardDescription,
} from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Skeleton } from "@/components/ui/skeleton";
import { useOnboardingStatus } from "@/hooks/use-api";
import {
  CheckCircle,
  Circle,
  Loader2,
  PartyPopper,
  XCircle,
  LayoutDashboard,
  ListChecks,
  FileText,
  ArrowLeft,
  RotateCcw,
} from "lucide-react";

const DEMO_ORG_ID = "00000000-0000-0000-0000-000000000000";

interface ProgressStep {
  key: string;
  label: string;
  description: string;
}

const PROGRESS_STEPS: ProgressStep[] = [
  {
    key: "organization_updated",
    label: "Updating organization details",
    description: "Saving your company information and preferences",
  },
  {
    key: "controls_generated",
    label: "Generating security controls",
    description: "Creating tailored controls based on your frameworks",
  },
  {
    key: "policies_generated",
    label: "Creating compliance policies",
    description: "Drafting policies aligned with your controls",
  },
  {
    key: "evidence_generated",
    label: "Collecting initial evidence",
    description: "Setting up evidence collection for your controls",
  },
];

function OnboardingProgressContent() {
  const searchParams = useSearchParams();
  const sessionId = searchParams.get("session") || "";

  const { data: session, isLoading, isError } = useOnboardingStatus(
    DEMO_ORG_ID,
    sessionId
  );

  if (!sessionId) {
    return (
      <div className="mx-auto max-w-2xl space-y-6">
        <Card>
          <CardContent className="flex flex-col items-center justify-center p-12 text-center">
            <XCircle className="h-12 w-12 text-muted-foreground mb-4" />
            <h3 className="text-lg font-medium">No session ID provided</h3>
            <p className="text-sm text-muted-foreground mt-1">
              A valid onboarding session is required to view progress.
            </p>
            <Link href="/onboarding" className="mt-4">
              <Button>
                <ArrowLeft className="mr-2 h-4 w-4" />
                Start Onboarding
              </Button>
            </Link>
          </CardContent>
        </Card>
      </div>
    );
  }

  if (isLoading) {
    return (
      <div className="mx-auto max-w-2xl space-y-6">
        <div className="text-center">
          <Skeleton className="mx-auto h-8 w-80" />
          <Skeleton className="mx-auto mt-2 h-5 w-60" />
        </div>
        <Card>
          <CardContent className="p-6 space-y-4">
            {[1, 2, 3, 4].map((i) => (
              <div key={i} className="flex items-center gap-4">
                <Skeleton className="h-8 w-8 rounded-full" />
                <div className="flex-1 space-y-2">
                  <Skeleton className="h-4 w-48" />
                  <Skeleton className="h-3 w-64" />
                </div>
              </div>
            ))}
          </CardContent>
        </Card>
      </div>
    );
  }

  if (isError || !session) {
    return (
      <div className="mx-auto max-w-2xl space-y-6">
        <Card>
          <CardContent className="flex flex-col items-center justify-center p-12 text-center">
            <XCircle className="h-12 w-12 text-red-500 mb-4" />
            <h3 className="text-lg font-medium">Unable to load session</h3>
            <p className="text-sm text-muted-foreground mt-1">
              Could not retrieve the onboarding session. It may have expired or
              the ID may be invalid.
            </p>
            <Link href="/onboarding" className="mt-4">
              <Button>
                <RotateCcw className="mr-2 h-4 w-4" />
                Try Again
              </Button>
            </Link>
          </CardContent>
        </Card>
      </div>
    );
  }

  const stepsCompleted: string[] = Array.isArray(
    (session.progress as Record<string, unknown>)?.steps_completed
  )
    ? ((session.progress as Record<string, unknown>)
        .steps_completed as string[])
    : [];

  const currentStepKey: string =
    ((session.progress as Record<string, unknown>)?.current_step as string) ||
    "";

  const isCompleted = session.status === "completed";
  const isFailed = session.status === "failed";
  const isRunning = !isCompleted && !isFailed;

  const errorMessage =
    ((session.progress as Record<string, unknown>)?.error as string) || "";

  const results = (session.results as Record<string, unknown>) || {};
  const controlsCount = (results.controls_count as number) || 0;
  const policiesCount = (results.policies_count as number) || 0;
  const evidenceCount = (results.evidence_count as number) || 0;

  function getStepStatus(
    stepKey: string
  ): "completed" | "current" | "pending" {
    if (stepsCompleted.includes(stepKey)) return "completed";
    if (currentStepKey === stepKey && isRunning) return "current";

    // If no explicit current_step, determine based on completion order
    const stepIndex = PROGRESS_STEPS.findIndex((s) => s.key === stepKey);
    const lastCompletedIndex = PROGRESS_STEPS.reduce(
      (max, s, idx) =>
        stepsCompleted.includes(s.key) ? Math.max(max, idx) : max,
      -1
    );

    if (
      isRunning &&
      !currentStepKey &&
      stepIndex === lastCompletedIndex + 1
    ) {
      return "current";
    }

    return "pending";
  }

  return (
    <div className="mx-auto max-w-2xl space-y-6">
      {/* Header */}
      <div className="text-center">
        <h1 className="text-3xl font-bold">
          {isCompleted
            ? "Setup Complete!"
            : isFailed
            ? "Setup Failed"
            : "Setting Up Your Compliance Program"}
        </h1>
        <p className="text-muted-foreground mt-1">
          {isCompleted
            ? "Your compliance program is ready to go"
            : isFailed
            ? "An error occurred during setup"
            : "This may take a few minutes. Please wait..."}
        </p>
      </div>

      {/* Progress Steps */}
      <Card>
        <CardHeader>
          <CardTitle className="text-lg">Progress</CardTitle>
          <CardDescription>
            {isCompleted
              ? "All steps completed successfully"
              : isFailed
              ? "Setup encountered an error"
              : "Working through setup steps..."}
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-1">
            {PROGRESS_STEPS.map((step, idx) => {
              const status = getStepStatus(step.key);

              return (
                <div key={step.key}>
                  <div
                    className={`flex items-center gap-4 rounded-lg p-3 transition-colors ${
                      status === "current"
                        ? "bg-blue-50 dark:bg-blue-950/30"
                        : status === "completed"
                        ? "bg-green-50/50 dark:bg-green-950/20"
                        : ""
                    }`}
                  >
                    {/* Status Icon */}
                    <div className="shrink-0">
                      {status === "completed" ? (
                        <CheckCircle className="h-6 w-6 text-green-600 dark:text-green-400" />
                      ) : status === "current" ? (
                        <Loader2 className="h-6 w-6 text-blue-600 dark:text-blue-400 animate-spin" />
                      ) : (
                        <Circle className="h-6 w-6 text-muted-foreground/40" />
                      )}
                    </div>

                    {/* Step Text */}
                    <div className="flex-1 min-w-0">
                      <div
                        className={`text-sm font-medium ${
                          status === "current"
                            ? "text-blue-700 dark:text-blue-300"
                            : status === "completed"
                            ? "text-green-700 dark:text-green-300"
                            : "text-muted-foreground"
                        }`}
                      >
                        {step.label}
                      </div>
                      <div className="text-xs text-muted-foreground mt-0.5">
                        {step.description}
                      </div>
                    </div>

                    {/* Status Badge */}
                    <div className="shrink-0">
                      {status === "completed" && (
                        <Badge variant="success">Done</Badge>
                      )}
                      {status === "current" && (
                        <Badge variant="default">In Progress</Badge>
                      )}
                    </div>
                  </div>

                  {/* Connector Line */}
                  {idx < PROGRESS_STEPS.length - 1 && (
                    <div className="ml-6 h-2 border-l-2 border-muted-foreground/20" />
                  )}
                </div>
              );
            })}
          </div>
        </CardContent>
      </Card>

      {/* Success State */}
      {isCompleted && (
        <Card className="border-green-200 bg-green-50/50 dark:border-green-800 dark:bg-green-950/20">
          <CardContent className="p-6">
            <div className="text-center space-y-4">
              <div className="relative inline-block">
                <PartyPopper className="h-12 w-12 text-green-600 dark:text-green-400" />
                <div className="absolute -top-1 -right-1 h-4 w-4 rounded-full bg-yellow-400 animate-bounce" />
                <div className="absolute -bottom-1 -left-1 h-3 w-3 rounded-full bg-blue-400 animate-bounce delay-100" />
              </div>

              <div>
                <h3 className="text-xl font-bold text-green-800 dark:text-green-200">
                  Your compliance program is ready!
                </h3>
                <p className="text-sm text-green-700 dark:text-green-300 mt-1">
                  We have set up everything you need to get started.
                </p>
              </div>

              {/* Results Summary */}
              <div className="grid grid-cols-3 gap-4 pt-2">
                <div className="rounded-lg bg-white dark:bg-background border p-4 text-center">
                  <div className="text-2xl font-bold text-primary">
                    {controlsCount}
                  </div>
                  <div className="text-xs text-muted-foreground mt-1">
                    Controls Created
                  </div>
                </div>
                <div className="rounded-lg bg-white dark:bg-background border p-4 text-center">
                  <div className="text-2xl font-bold text-primary">
                    {policiesCount}
                  </div>
                  <div className="text-xs text-muted-foreground mt-1">
                    Policies Drafted
                  </div>
                </div>
                <div className="rounded-lg bg-white dark:bg-background border p-4 text-center">
                  <div className="text-2xl font-bold text-primary">
                    {evidenceCount}
                  </div>
                  <div className="text-xs text-muted-foreground mt-1">
                    Evidence Items
                  </div>
                </div>
              </div>

              {/* Navigation Links */}
              <div className="flex flex-wrap items-center justify-center gap-3 pt-2">
                <Link href="/dashboard">
                  <Button>
                    <LayoutDashboard className="mr-2 h-4 w-4" />
                    View Dashboard
                  </Button>
                </Link>
                <Link href="/controls">
                  <Button variant="outline">
                    <ListChecks className="mr-2 h-4 w-4" />
                    View Controls
                  </Button>
                </Link>
                <Link href="/policies">
                  <Button variant="outline">
                    <FileText className="mr-2 h-4 w-4" />
                    View Policies
                  </Button>
                </Link>
              </div>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Failed State */}
      {isFailed && (
        <Card className="border-red-200 bg-red-50/50 dark:border-red-800 dark:bg-red-950/20">
          <CardContent className="p-6">
            <div className="text-center space-y-4">
              <XCircle className="mx-auto h-12 w-12 text-red-500" />

              <div>
                <h3 className="text-xl font-bold text-red-800 dark:text-red-200">
                  Setup encountered an error
                </h3>
                {errorMessage && (
                  <p className="text-sm text-red-700 dark:text-red-300 mt-2 rounded-md bg-red-100 dark:bg-red-900/50 p-3 font-mono">
                    {errorMessage}
                  </p>
                )}
              </div>

              <Link href="/onboarding">
                <Button variant="destructive">
                  <RotateCcw className="mr-2 h-4 w-4" />
                  Try Again
                </Button>
              </Link>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Running indicator */}
      {isRunning && (
        <div className="flex items-center justify-center gap-2 text-sm text-muted-foreground">
          <Loader2 className="h-4 w-4 animate-spin" />
          <span>Auto-refreshing every 3 seconds...</span>
        </div>
      )}
    </div>
  );
}

export default function OnboardingProgressPage() {
  return (
    <Suspense
      fallback={
        <div className="mx-auto max-w-2xl space-y-6">
          <div className="text-center">
            <Skeleton className="mx-auto h-8 w-80" />
            <Skeleton className="mx-auto mt-2 h-5 w-60" />
          </div>
          <Card>
            <CardContent className="p-6 space-y-4">
              {[1, 2, 3, 4].map((i) => (
                <div key={i} className="flex items-center gap-4">
                  <Skeleton className="h-8 w-8 rounded-full" />
                  <div className="flex-1 space-y-2">
                    <Skeleton className="h-4 w-48" />
                    <Skeleton className="h-3 w-64" />
                  </div>
                </div>
              ))}
            </CardContent>
          </Card>
        </div>
      }
    >
      <OnboardingProgressContent />
    </Suspense>
  );
}

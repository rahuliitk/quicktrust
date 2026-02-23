"use client";

import Link from "next/link";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Skeleton } from "@/components/ui/skeleton";
import { useRiskMatrix } from "@/hooks/use-api";
import { ArrowLeft } from "lucide-react";
import type { RiskMatrixCell } from "@/lib/types";

const DEMO_ORG_ID = "00000000-0000-0000-0000-000000000000";

function getCellColor(likelihood: number, impact: number): string {
  const score = likelihood * impact;
  if (score >= 20) return "bg-red-500 text-white";
  if (score >= 12) return "bg-orange-400 text-white";
  if (score >= 5) return "bg-yellow-400 text-yellow-950";
  return "bg-green-400 text-green-950";
}

function getCellHoverColor(likelihood: number, impact: number): string {
  const score = likelihood * impact;
  if (score >= 20) return "hover:bg-red-600";
  if (score >= 12) return "hover:bg-orange-500";
  if (score >= 5) return "hover:bg-yellow-500";
  return "hover:bg-green-500";
}

const LIKELIHOOD_LABELS: Record<number, string> = {
  5: "Almost Certain",
  4: "Likely",
  3: "Possible",
  2: "Unlikely",
  1: "Rare",
};

const IMPACT_LABELS: Record<number, string> = {
  1: "Negligible",
  2: "Minor",
  3: "Moderate",
  4: "Major",
  5: "Severe",
};

export default function RiskMatrixPage() {
  const { data, isLoading } = useRiskMatrix(DEMO_ORG_ID);

  // Build a lookup map from cells array
  const cellMap = new Map<string, RiskMatrixCell>();
  if (data?.cells) {
    for (const cell of data.cells) {
      cellMap.set(`${cell.likelihood}-${cell.impact}`, cell);
    }
  }

  return (
    <div className="space-y-6">
      {/* Back link */}
      <Link
        href="/risks"
        className="inline-flex items-center gap-1 text-sm text-muted-foreground hover:text-foreground transition-colors"
      >
        <ArrowLeft className="h-4 w-4" />
        Back to Risk Register
      </Link>

      <div>
        <h1 className="text-3xl font-bold">Risk Matrix</h1>
        <p className="text-muted-foreground">
          5&times;5 likelihood vs impact heat map
        </p>
      </div>

      {isLoading ? (
        <Skeleton className="h-[480px] w-full rounded-xl" />
      ) : (
        <Card>
          <CardHeader>
            <CardTitle>Heat Map</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="overflow-x-auto">
              <div className="min-w-[600px]">
                {/* Grid layout: label column + 5 impact columns */}
                <div className="flex">
                  {/* Y-axis label */}
                  <div className="flex flex-col items-center justify-center w-12 mr-2">
                    <span className="text-xs font-medium text-muted-foreground -rotate-90 whitespace-nowrap">
                      LIKELIHOOD
                    </span>
                  </div>

                  <div className="flex-1">
                    {/* Rows: likelihood 5 (top) down to 1 (bottom) */}
                    {[5, 4, 3, 2, 1].map((likelihood) => (
                      <div key={likelihood} className="flex items-stretch">
                        {/* Row label */}
                        <div className="flex items-center justify-end w-28 pr-3 shrink-0">
                          <div className="text-right">
                            <div className="text-sm font-semibold">
                              {likelihood}
                            </div>
                            <div className="text-xs text-muted-foreground">
                              {LIKELIHOOD_LABELS[likelihood]}
                            </div>
                          </div>
                        </div>

                        {/* Cells: impact 1 to 5 */}
                        <div className="flex-1 grid grid-cols-5 gap-1">
                          {[1, 2, 3, 4, 5].map((impact) => {
                            const cell = cellMap.get(
                              `${likelihood}-${impact}`
                            );
                            const count = cell?.count || 0;
                            const score = likelihood * impact;

                            return (
                              <div
                                key={impact}
                                className={`
                                  flex flex-col items-center justify-center
                                  rounded-md p-3 min-h-[72px]
                                  transition-colors cursor-default
                                  ${getCellColor(likelihood, impact)}
                                  ${getCellHoverColor(likelihood, impact)}
                                `}
                                title={`Likelihood: ${likelihood}, Impact: ${impact}, Score: ${score}, Risks: ${count}`}
                              >
                                <div className="text-lg font-bold">
                                  {count}
                                </div>
                                <div className="text-xs opacity-80">
                                  {score}
                                </div>
                              </div>
                            );
                          })}
                        </div>
                      </div>
                    ))}

                    {/* Impact column headers */}
                    <div className="flex mt-1">
                      <div className="w-28 shrink-0" />
                      <div className="flex-1 grid grid-cols-5 gap-1">
                        {[1, 2, 3, 4, 5].map((impact) => (
                          <div key={impact} className="text-center pt-2">
                            <div className="text-sm font-semibold">
                              {impact}
                            </div>
                            <div className="text-xs text-muted-foreground">
                              {IMPACT_LABELS[impact]}
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>

                    {/* X-axis label */}
                    <div className="flex mt-2">
                      <div className="w-28 shrink-0" />
                      <div className="flex-1 text-center">
                        <span className="text-xs font-medium text-muted-foreground">
                          IMPACT
                        </span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            {/* Legend */}
            <div className="mt-6 flex items-center justify-center gap-6">
              <div className="flex items-center gap-2">
                <div className="h-4 w-4 rounded bg-green-400" />
                <span className="text-xs text-muted-foreground">
                  Low (1-4)
                </span>
              </div>
              <div className="flex items-center gap-2">
                <div className="h-4 w-4 rounded bg-yellow-400" />
                <span className="text-xs text-muted-foreground">
                  Medium (5-11)
                </span>
              </div>
              <div className="flex items-center gap-2">
                <div className="h-4 w-4 rounded bg-orange-400" />
                <span className="text-xs text-muted-foreground">
                  High (12-19)
                </span>
              </div>
              <div className="flex items-center gap-2">
                <div className="h-4 w-4 rounded bg-red-500" />
                <span className="text-xs text-muted-foreground">
                  Critical (20-25)
                </span>
              </div>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
}

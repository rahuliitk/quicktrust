"use client";

import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Progress } from "@/components/ui/progress";
import { Skeleton } from "@/components/ui/skeleton";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import {
  useFrameworks,
  useGapAnalysis,
  useCrossFrameworkMatrix,
} from "@/hooks/use-api";
import { useOrgId } from "@/hooks/use-org-id";
import {
  BarChart3,
  CheckCircle,
  AlertTriangle,
  XCircle,
  GitBranch,
} from "lucide-react";

export default function GapAnalysisPage() {
  const orgId = useOrgId();
  const [selectedFramework, setSelectedFramework] = useState<string>("");
  const { data: frameworks, isLoading: fwLoading } = useFrameworks();
  const { data: gapData, isLoading: gapLoading } = useGapAnalysis(
    orgId,
    selectedFramework
  );
  const { data: matrix, isLoading: matrixLoading } =
    useCrossFrameworkMatrix(orgId);

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold">Gap Analysis</h1>
        <p className="text-muted-foreground">
          Identify compliance gaps and cross-framework control coverage
        </p>
      </div>

      <Tabs defaultValue="framework">
        <TabsList>
          <TabsTrigger value="framework">Framework Gap Analysis</TabsTrigger>
          <TabsTrigger value="cross">Cross-Framework Matrix</TabsTrigger>
        </TabsList>

        <TabsContent value="framework" className="space-y-4">
          {/* Framework selector */}
          <div className="flex flex-wrap gap-2">
            {fwLoading ? (
              <Skeleton className="h-9 w-40" />
            ) : (
              frameworks?.map((fw: any) => (
                <Button
                  key={fw.id}
                  size="sm"
                  variant={selectedFramework === fw.id ? "default" : "outline"}
                  onClick={() => setSelectedFramework(fw.id)}
                >
                  {fw.name}
                </Button>
              ))
            )}
          </div>

          {!selectedFramework ? (
            <Card>
              <CardContent className="flex flex-col items-center justify-center p-12">
                <BarChart3 className="h-12 w-12 text-muted-foreground mb-4" />
                <p className="text-muted-foreground">
                  Select a framework to view gap analysis
                </p>
              </CardContent>
            </Card>
          ) : gapLoading ? (
            <Skeleton className="h-64 w-full" />
          ) : gapData ? (
            <>
              {/* Summary */}
              <div className="grid gap-4 md:grid-cols-4">
                <Card>
                  <CardContent className="p-4">
                    <div className="text-2xl font-bold">
                      {gapData.total_requirements}
                    </div>
                    <p className="text-xs text-muted-foreground">
                      Total Requirements
                    </p>
                  </CardContent>
                </Card>
                <Card>
                  <CardContent className="p-4">
                    <div className="text-2xl font-bold text-green-600">
                      {gapData.covered_count}
                    </div>
                    <p className="text-xs text-muted-foreground">
                      Fully Covered
                    </p>
                  </CardContent>
                </Card>
                <Card>
                  <CardContent className="p-4">
                    <div className="text-2xl font-bold text-yellow-600">
                      {gapData.partial_count}
                    </div>
                    <p className="text-xs text-muted-foreground">
                      Partially Covered
                    </p>
                  </CardContent>
                </Card>
                <Card>
                  <CardContent className="p-4">
                    <div className="text-2xl font-bold text-red-600">
                      {gapData.gap_count}
                    </div>
                    <p className="text-xs text-muted-foreground">Gaps</p>
                  </CardContent>
                </Card>
              </div>

              <Card>
                <CardContent className="p-4">
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-sm font-medium">Coverage</span>
                    <span className="text-sm font-bold">
                      {gapData.coverage_percentage}%
                    </span>
                  </div>
                  <Progress value={gapData.coverage_percentage} />
                </CardContent>
              </Card>

              {/* Gaps */}
              {gapData.gaps?.length > 0 && (
                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center gap-2 text-red-600">
                      <XCircle className="h-5 w-5" />
                      Gaps ({gapData.gaps.length})
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-2">
                      {gapData.gaps.map((g: any) => (
                        <div
                          key={g.requirement_id}
                          className="flex items-center justify-between rounded-lg border border-red-200 bg-red-50 p-3"
                        >
                          <div>
                            <span className="font-mono text-sm mr-2">
                              {g.code}
                            </span>
                            <span className="text-sm">{g.title}</span>
                          </div>
                          <Badge variant="destructive">No Controls</Badge>
                        </div>
                      ))}
                    </div>
                  </CardContent>
                </Card>
              )}

              {/* Partial */}
              {gapData.partial?.length > 0 && (
                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center gap-2 text-yellow-600">
                      <AlertTriangle className="h-5 w-5" />
                      Partially Covered ({gapData.partial.length})
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-2">
                      {gapData.partial.map((p: any) => (
                        <div
                          key={p.requirement_id}
                          className="rounded-lg border border-yellow-200 bg-yellow-50 p-3"
                        >
                          <div className="flex items-center justify-between">
                            <div>
                              <span className="font-mono text-sm mr-2">
                                {p.code}
                              </span>
                              <span className="text-sm">{p.title}</span>
                            </div>
                            <Badge className="bg-yellow-100 text-yellow-800">
                              {p.controls?.length} control(s)
                            </Badge>
                          </div>
                          <div className="mt-2 flex flex-wrap gap-1">
                            {p.controls?.map((c: any) => (
                              <Badge key={c.id} variant="outline" className="text-xs">
                                {c.title} ({c.status})
                              </Badge>
                            ))}
                          </div>
                        </div>
                      ))}
                    </div>
                  </CardContent>
                </Card>
              )}

              {/* Covered */}
              {gapData.covered?.length > 0 && (
                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center gap-2 text-green-600">
                      <CheckCircle className="h-5 w-5" />
                      Fully Covered ({gapData.covered.length})
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-1">
                      {gapData.covered.map((c: any) => (
                        <div
                          key={c.requirement_id}
                          className="flex items-center justify-between rounded p-2 hover:bg-muted/50"
                        >
                          <div>
                            <span className="font-mono text-sm mr-2">
                              {c.code}
                            </span>
                            <span className="text-sm">{c.title}</span>
                          </div>
                          <Badge variant="default">
                            {c.controls?.length} control(s)
                          </Badge>
                        </div>
                      ))}
                    </div>
                  </CardContent>
                </Card>
              )}
            </>
          ) : null}
        </TabsContent>

        <TabsContent value="cross" className="space-y-4">
          {matrixLoading ? (
            <Skeleton className="h-64 w-full" />
          ) : matrix ? (
            <>
              <div className="grid gap-4 md:grid-cols-3">
                <Card>
                  <CardContent className="p-4">
                    <div className="text-2xl font-bold">
                      {matrix.total_controls}
                    </div>
                    <p className="text-xs text-muted-foreground">
                      Total Controls
                    </p>
                  </CardContent>
                </Card>
                <Card>
                  <CardContent className="p-4">
                    <div className="text-2xl font-bold text-purple-600">
                      {matrix.multi_framework_controls}
                    </div>
                    <p className="text-xs text-muted-foreground">
                      Multi-Framework Controls
                    </p>
                  </CardContent>
                </Card>
                <Card>
                  <CardContent className="p-4">
                    <div className="text-2xl font-bold text-blue-600">
                      {matrix.deduplication_opportunity}
                    </div>
                    <p className="text-xs text-muted-foreground">
                      Dedup Opportunities
                    </p>
                  </CardContent>
                </Card>
              </div>

              {/* Framework coverage comparison */}
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <GitBranch className="h-5 w-5" />
                    Framework Coverage Comparison
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  {matrix.frameworks?.map((fw: any) => (
                    <div key={fw.framework_id} className="space-y-1">
                      <div className="flex items-center justify-between text-sm">
                        <span className="font-medium">{fw.framework_name}</span>
                        <span className="text-muted-foreground">
                          {fw.implemented_controls}/{fw.total_requirements}{" "}
                          requirements ({fw.coverage_pct}%)
                        </span>
                      </div>
                      <Progress value={fw.coverage_pct} />
                    </div>
                  ))}
                </CardContent>
              </Card>
            </>
          ) : (
            <Card>
              <CardContent className="flex flex-col items-center justify-center p-12">
                <GitBranch className="h-12 w-12 text-muted-foreground mb-4" />
                <p className="text-muted-foreground">
                  No cross-framework data available
                </p>
              </CardContent>
            </Card>
          )}
        </TabsContent>
      </Tabs>
    </div>
  );
}

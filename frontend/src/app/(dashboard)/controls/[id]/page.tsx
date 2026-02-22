"use client";

import { useParams } from "next/navigation";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Skeleton } from "@/components/ui/skeleton";
import { useControl } from "@/hooks/use-api";

const DEMO_ORG_ID = "00000000-0000-0000-0000-000000000000";

export default function ControlDetailPage() {
  const params = useParams();
  const { data: control, isLoading } = useControl(
    DEMO_ORG_ID,
    params.id as string
  );

  if (isLoading) {
    return (
      <div className="space-y-4">
        <Skeleton className="h-10 w-64" />
        <Skeleton className="h-64 w-full" />
      </div>
    );
  }

  if (!control) return <p>Control not found.</p>;

  return (
    <div className="space-y-6">
      <div>
        <div className="flex items-center gap-3">
          <h1 className="text-3xl font-bold">{control.title}</h1>
          <Badge>{control.status.replace(/_/g, " ")}</Badge>
        </div>
        <p className="mt-1 text-muted-foreground">
          Automation: {control.automation_level} &middot; Created{" "}
          {new Date(control.created_at).toLocaleDateString()}
        </p>
      </div>

      <Tabs defaultValue="overview">
        <TabsList>
          <TabsTrigger value="overview">Overview</TabsTrigger>
          <TabsTrigger value="mappings">Framework Mappings</TabsTrigger>
          <TabsTrigger value="evidence">Evidence</TabsTrigger>
          <TabsTrigger value="testing">Test History</TabsTrigger>
        </TabsList>

        <TabsContent value="overview">
          <Card>
            <CardHeader>
              <CardTitle>Description</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="whitespace-pre-wrap">
                {control.description || "No description provided."}
              </p>
            </CardContent>
          </Card>

          {control.implementation_details && (
            <Card className="mt-4">
              <CardHeader>
                <CardTitle>Implementation Details</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="whitespace-pre-wrap">
                  {control.implementation_details}
                </p>
              </CardContent>
            </Card>
          )}

          {control.test_procedure && (
            <Card className="mt-4">
              <CardHeader>
                <CardTitle>Test Procedure</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="whitespace-pre-wrap">{control.test_procedure}</p>
              </CardContent>
            </Card>
          )}
        </TabsContent>

        <TabsContent value="mappings">
          <Card>
            <CardContent className="p-6">
              <p className="text-sm text-muted-foreground">
                Framework mappings will be displayed here once loaded.
              </p>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="evidence">
          <Card>
            <CardContent className="p-6">
              <p className="text-sm text-muted-foreground">
                Evidence items linked to this control will appear here.
              </p>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="testing">
          <Card>
            <CardContent className="p-6">
              {control.last_test_date ? (
                <div>
                  <p>
                    Last tested: {new Date(control.last_test_date).toLocaleDateString()}
                  </p>
                  <p>Result: {control.last_test_result || "N/A"}</p>
                </div>
              ) : (
                <p className="text-sm text-muted-foreground">
                  No tests have been run for this control yet.
                </p>
              )}
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
}

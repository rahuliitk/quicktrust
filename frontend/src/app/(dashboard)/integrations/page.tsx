"use client";

import Link from "next/link";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Skeleton } from "@/components/ui/skeleton";
import { useProviders, useIntegrations } from "@/hooks/use-api";
import { Plug, Unplug, Cable } from "lucide-react";

const DEMO_ORG_ID = "00000000-0000-0000-0000-000000000000";

const statusVariant: Record<string, "success" | "secondary" | "destructive"> = {
  connected: "success",
  disconnected: "secondary",
  error: "destructive",
};

export default function IntegrationsPage() {
  const { data: providers, isLoading: providersLoading } = useProviders(DEMO_ORG_ID);
  const { data: integrationsData, isLoading: integrationsLoading } =
    useIntegrations(DEMO_ORG_ID);

  const integrations = integrationsData?.items || [];

  return (
    <div className="space-y-8">
      {/* Page header */}
      <div>
        <h1 className="text-3xl font-bold">Integrations</h1>
        <p className="text-muted-foreground">
          Connect your tools for automated evidence collection
        </p>
      </div>

      {/* Available Providers */}
      <section className="space-y-4">
        <h2 className="text-xl font-semibold">Available Providers</h2>

        {providersLoading ? (
          <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
            {[1, 2, 3].map((i) => (
              <Skeleton key={i} className="h-44 w-full rounded-xl" />
            ))}
          </div>
        ) : providers && providers.length > 0 ? (
          <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
            {providers.map((provider) => (
              <Card key={provider.provider} className="flex flex-col">
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Plug className="h-5 w-5 text-primary" />
                    {provider.name}
                  </CardTitle>
                  <CardDescription>{provider.description}</CardDescription>
                </CardHeader>
                <CardContent className="mt-auto flex items-center justify-between">
                  <span className="text-xs text-muted-foreground">
                    {provider.collector_types.length}{" "}
                    {provider.collector_types.length === 1
                      ? "collector"
                      : "collectors"}
                  </span>
                  <Button size="sm">
                    <Cable className="mr-2 h-4 w-4" />
                    Connect
                  </Button>
                </CardContent>
              </Card>
            ))}
          </div>
        ) : (
          <Card>
            <CardContent className="flex flex-col items-center justify-center p-12 text-center">
              <Plug className="h-12 w-12 text-muted-foreground mb-4" />
              <h3 className="text-lg font-medium">No providers available</h3>
              <p className="text-sm text-muted-foreground mt-1">
                Integration providers have not been configured yet.
              </p>
            </CardContent>
          </Card>
        )}
      </section>

      {/* Connected Integrations */}
      <section className="space-y-4">
        <h2 className="text-xl font-semibold">Connected Integrations</h2>

        {integrationsLoading ? (
          <div className="space-y-3">
            {[1, 2, 3].map((i) => (
              <Skeleton key={i} className="h-20 w-full rounded-xl" />
            ))}
          </div>
        ) : integrations.length > 0 ? (
          <div className="space-y-3">
            {integrations.map((integration) => (
              <Link
                key={integration.id}
                href={`/integrations/${integration.id}`}
              >
                <Card className="transition-colors hover:bg-accent/50">
                  <CardContent className="flex items-center gap-4 p-4">
                    <Plug className="h-8 w-8 text-muted-foreground shrink-0" />
                    <div className="flex-1 min-w-0">
                      <div className="font-medium">{integration.name}</div>
                      <div className="mt-1 flex items-center gap-2 text-xs text-muted-foreground">
                        <span className="capitalize">{integration.provider}</span>
                        {integration.last_sync_at && (
                          <>
                            <span>&middot;</span>
                            <span>
                              Last synced{" "}
                              {new Date(
                                integration.last_sync_at
                              ).toLocaleDateString()}
                            </span>
                          </>
                        )}
                      </div>
                    </div>
                    <Badge
                      variant={statusVariant[integration.status] || "secondary"}
                    >
                      {integration.status}
                    </Badge>
                  </CardContent>
                </Card>
              </Link>
            ))}
          </div>
        ) : (
          <Card>
            <CardContent className="flex flex-col items-center justify-center p-12 text-center">
              <Unplug className="h-12 w-12 text-muted-foreground mb-4" />
              <h3 className="text-lg font-medium">No integrations connected</h3>
              <p className="text-sm text-muted-foreground mt-1">
                Connect a provider above to start collecting evidence
                automatically.
              </p>
            </CardContent>
          </Card>
        )}
      </section>
    </div>
  );
}

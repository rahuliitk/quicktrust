"use client";

import { useState } from "react";
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
import {
  useProviders,
  useIntegrations,
  useCreateIntegration,
} from "@/hooks/use-api";
import { useOrgId } from "@/hooks/use-org-id";
import { Plug, Unplug, Cable, Loader2, X, CheckCircle2 } from "lucide-react";

const statusVariant: Record<string, "success" | "secondary" | "destructive"> = {
  connected: "success",
  disconnected: "secondary",
  error: "destructive",
};

const CREDENTIAL_FIELDS: Record<string, { label: string; placeholder: string; type?: string }[]> = {
  aws: [
    { label: "AWS Access Key ID", placeholder: "AKIA..." },
    { label: "AWS Secret Access Key", placeholder: "wJalr...", type: "password" },
    { label: "AWS Region", placeholder: "us-east-1" },
  ],
  github: [
    { label: "GitHub Token", placeholder: "ghp_...", type: "password" },
    { label: "Repository (owner/repo)", placeholder: "acme/backend" },
  ],
  okta: [
    { label: "Okta Domain", placeholder: "your-org.okta.com" },
    { label: "API Token", placeholder: "00...", type: "password" },
  ],
};

export default function IntegrationsPage() {
  const orgId = useOrgId();
  const { data: providers, isLoading: providersLoading } = useProviders(orgId);
  const { data: integrationsData, isLoading: integrationsLoading } =
    useIntegrations(orgId);
  const createIntegration = useCreateIntegration(orgId);

  const integrations = integrationsData?.items || [];

  const [connectProvider, setConnectProvider] = useState<string | null>(null);
  const [connectName, setConnectName] = useState("");
  const [credFields, setCredFields] = useState<Record<string, string>>({});
  const [connectSuccess, setConnectSuccess] = useState(false);

  function openConnectModal(providerKey: string) {
    setConnectProvider(providerKey);
    setConnectName("");
    setCredFields({});
    setConnectSuccess(false);
  }

  function handleConnect() {
    if (!connectProvider || !connectName.trim()) return;

    const config: Record<string, unknown> = {};
    const fields = CREDENTIAL_FIELDS[connectProvider] || [];
    for (const f of fields) {
      if (credFields[f.label]) {
        config[f.label.toLowerCase().replace(/\s+/g, "_")] = credFields[f.label];
      }
    }

    createIntegration.mutate(
      { provider: connectProvider, name: connectName, config },
      {
        onSuccess: () => {
          setConnectSuccess(true);
          setTimeout(() => {
            setConnectProvider(null);
            setConnectSuccess(false);
          }, 1500);
        },
      }
    );
  }

  const selectedProvider = providers?.find(
    (p) => p.provider === connectProvider
  );

  return (
    <div className="space-y-8">
      {/* Page header */}
      <div>
        <h1 className="text-3xl font-bold">Integrations</h1>
        <p className="text-muted-foreground">
          Connect your tools for automated evidence collection
        </p>
      </div>

      {/* Connect Modal */}
      {connectProvider && selectedProvider && (
        <Card className="border-primary">
          <CardHeader>
            <div className="flex items-center justify-between">
              <CardTitle className="flex items-center gap-2">
                <Cable className="h-5 w-5" />
                Connect {selectedProvider.name}
              </CardTitle>
              <Button
                size="sm"
                variant="ghost"
                onClick={() => setConnectProvider(null)}
              >
                <X className="h-4 w-4" />
              </Button>
            </div>
            <CardDescription>{selectedProvider.description}</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            {connectSuccess ? (
              <div className="flex flex-col items-center py-6 text-center">
                <CheckCircle2 className="h-12 w-12 text-green-500 mb-3" />
                <p className="font-medium text-green-700 dark:text-green-400">
                  Connected successfully!
                </p>
              </div>
            ) : (
              <>
                <div>
                  <label className="text-sm font-medium">
                    Connection Name
                  </label>
                  <input
                    type="text"
                    className="mt-1 w-full rounded-md border bg-background p-2 text-sm"
                    placeholder={`My ${selectedProvider.name} Connection`}
                    value={connectName}
                    onChange={(e) => setConnectName(e.target.value)}
                  />
                </div>

                {(CREDENTIAL_FIELDS[connectProvider] || []).map((field) => (
                  <div key={field.label}>
                    <label className="text-sm font-medium">{field.label}</label>
                    <input
                      type={field.type || "text"}
                      className="mt-1 w-full rounded-md border bg-background p-2 text-sm"
                      placeholder={field.placeholder}
                      value={credFields[field.label] || ""}
                      onChange={(e) =>
                        setCredFields((prev) => ({
                          ...prev,
                          [field.label]: e.target.value,
                        }))
                      }
                    />
                  </div>
                ))}

                <div className="flex gap-2 pt-2">
                  <Button
                    onClick={handleConnect}
                    disabled={
                      !connectName.trim() || createIntegration.isPending
                    }
                  >
                    {createIntegration.isPending ? (
                      <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                    ) : (
                      <Cable className="mr-2 h-4 w-4" />
                    )}
                    Connect
                  </Button>
                  <Button
                    variant="ghost"
                    onClick={() => setConnectProvider(null)}
                  >
                    Cancel
                  </Button>
                </div>
              </>
            )}
          </CardContent>
        </Card>
      )}

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
                  <Button
                    size="sm"
                    onClick={() => openConnectModal(provider.provider)}
                  >
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
                        <span className="capitalize">
                          {integration.provider}
                        </span>
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
              <h3 className="text-lg font-medium">
                No integrations connected
              </h3>
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

"use client";

import { useState, useEffect } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Skeleton } from "@/components/ui/skeleton";
import { useOrganization, useUpdateOrganization } from "@/hooks/use-api";
import { useOrgId } from "@/hooks/use-org-id";
import { Loader2, Save, Building, AlertTriangle } from "lucide-react";

export default function SettingsPage() {
  const orgId = useOrgId();
  const { data: org, isLoading, error } = useOrganization(orgId);
  const updateOrg = useUpdateOrganization(orgId);

  const [form, setForm] = useState({
    name: "",
    industry: "",
    company_size: "",
    cloud_providers: "",
    tech_stack: "",
  });
  const [dirty, setDirty] = useState(false);

  // Populate form when organization data loads
  useEffect(() => {
    if (org) {
      const cloudProviders = org.cloud_providers
        ? Array.isArray(org.cloud_providers)
          ? (org.cloud_providers as string[]).join(", ")
          : typeof org.cloud_providers === "object"
          ? Object.keys(org.cloud_providers).join(", ")
          : String(org.cloud_providers)
        : "";
      const techStack = org.tech_stack
        ? Array.isArray(org.tech_stack)
          ? (org.tech_stack as string[]).join(", ")
          : typeof org.tech_stack === "object"
          ? Object.keys(org.tech_stack).join(", ")
          : String(org.tech_stack)
        : "";

      setForm({
        name: org.name || "",
        industry: org.industry || "",
        company_size: org.company_size || "",
        cloud_providers: cloudProviders,
        tech_stack: techStack,
      });
    }
  }, [org]);

  function updateField(field: string, value: string) {
    setForm((prev) => ({ ...prev, [field]: value }));
    setDirty(true);
  }

  function handleSave() {
    const cloudProvidersArray = form.cloud_providers
      .split(",")
      .map((s) => s.trim())
      .filter(Boolean);
    const techStackArray = form.tech_stack
      .split(",")
      .map((s) => s.trim())
      .filter(Boolean);

    updateOrg.mutate(
      {
        name: form.name,
        industry: form.industry || null,
        company_size: form.company_size || null,
        cloud_providers: cloudProvidersArray as any,
        tech_stack: techStackArray as any,
      },
      { onSuccess: () => setDirty(false) }
    );
  }

  if (isLoading) {
    return (
      <div className="space-y-4">
        <Skeleton className="h-10 w-48" />
        <Skeleton className="h-64 w-full" />
      </div>
    );
  }

  if (error) {
    return (
      <div className="space-y-6">
        <div>
          <h1 className="text-3xl font-bold">Settings</h1>
          <p className="text-muted-foreground">Manage your organization settings</p>
        </div>
        <Card className="border-destructive">
          <CardContent className="flex flex-col items-center justify-center p-12 text-center">
            <AlertTriangle className="h-12 w-12 text-destructive mb-4" />
            <h3 className="text-lg font-semibold">Failed to load settings</h3>
            <p className="text-sm text-muted-foreground mt-2">
              {error.message || "An unexpected error occurred. Please try again later."}
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
      <div>
        <h1 className="text-3xl font-bold">Settings</h1>
        <p className="text-muted-foreground">
          Manage your organization settings
        </p>
      </div>

      <Card>
        <CardHeader>
          <div className="flex items-center gap-2">
            <Building className="h-5 w-5 text-muted-foreground" />
            <CardTitle>Organization Information</CardTitle>
          </div>
        </CardHeader>
        <CardContent className="space-y-4">
          <div>
            <label className="text-sm font-medium">Organization Name</label>
            <input
              type="text"
              className="mt-1 w-full rounded-md border bg-background p-2 text-sm"
              placeholder="Your company name"
              value={form.name}
              onChange={(e) => updateField("name", e.target.value)}
            />
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="text-sm font-medium">Industry</label>
              <input
                type="text"
                className="mt-1 w-full rounded-md border bg-background p-2 text-sm"
                placeholder="e.g. Technology, Healthcare, Finance"
                value={form.industry}
                onChange={(e) => updateField("industry", e.target.value)}
              />
            </div>

            <div>
              <label className="text-sm font-medium">Company Size</label>
              <select
                className="mt-1 w-full rounded-md border bg-background p-2 text-sm"
                value={form.company_size}
                onChange={(e) => updateField("company_size", e.target.value)}
              >
                <option value="">Select size</option>
                <option value="1-10">1-10</option>
                <option value="11-50">11-50</option>
                <option value="51-200">51-200</option>
                <option value="201-1000">201-1000</option>
                <option value="1000+">1000+</option>
              </select>
            </div>
          </div>

          <div>
            <label className="text-sm font-medium">
              Cloud Providers (comma-separated)
            </label>
            <input
              type="text"
              className="mt-1 w-full rounded-md border bg-background p-2 text-sm"
              placeholder="AWS, GCP, Azure"
              value={form.cloud_providers}
              onChange={(e) => updateField("cloud_providers", e.target.value)}
            />
            <p className="mt-1 text-xs text-muted-foreground">
              Separate multiple providers with commas
            </p>
          </div>

          <div>
            <label className="text-sm font-medium">
              Tech Stack (comma-separated)
            </label>
            <input
              type="text"
              className="mt-1 w-full rounded-md border bg-background p-2 text-sm"
              placeholder="React, Python, PostgreSQL, Docker"
              value={form.tech_stack}
              onChange={(e) => updateField("tech_stack", e.target.value)}
            />
            <p className="mt-1 text-xs text-muted-foreground">
              Separate multiple technologies with commas
            </p>
          </div>

          {dirty && (
            <div className="flex items-center gap-2 pt-2">
              <Button onClick={handleSave} disabled={updateOrg.isPending}>
                {updateOrg.isPending ? (
                  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                ) : (
                  <Save className="mr-2 h-4 w-4" />
                )}
                Save Changes
              </Button>
              <Button
                variant="outline"
                onClick={() => {
                  if (org) {
                    const cloudProviders = org.cloud_providers
                      ? Array.isArray(org.cloud_providers)
                        ? (org.cloud_providers as string[]).join(", ")
                        : typeof org.cloud_providers === "object"
                        ? Object.keys(org.cloud_providers).join(", ")
                        : String(org.cloud_providers)
                      : "";
                    const techStack = org.tech_stack
                      ? Array.isArray(org.tech_stack)
                        ? (org.tech_stack as string[]).join(", ")
                        : typeof org.tech_stack === "object"
                        ? Object.keys(org.tech_stack).join(", ")
                        : String(org.tech_stack)
                      : "";
                    setForm({
                      name: org.name || "",
                      industry: org.industry || "",
                      company_size: org.company_size || "",
                      cloud_providers: cloudProviders,
                      tech_stack: techStack,
                    });
                  }
                  setDirty(false);
                }}
              >
                Cancel
              </Button>
            </div>
          )}

          {updateOrg.isSuccess && !dirty && (
            <p className="text-sm text-green-600">
              Settings saved successfully.
            </p>
          )}
        </CardContent>
      </Card>
    </div>
  );
}

"use client";

import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Skeleton } from "@/components/ui/skeleton";
import { useControlTemplates } from "@/hooks/use-api";
import { FileStack } from "lucide-react";

const DOMAINS = [
  "Access Control",
  "Network Security",
  "Data Protection",
  "Change Management",
  "Logging & Monitoring",
  "Incident Response",
  "Endpoint Security",
  "HR Security",
];

export default function ControlTemplatesPage() {
  const [domainFilter, setDomainFilter] = useState<string | undefined>();
  const { data, isLoading } = useControlTemplates({ domain: domainFilter });

  const templates = data?.items || [];

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold">Control Templates</h1>
        <p className="text-muted-foreground">
          Browse the control template library
        </p>
      </div>

      <div className="flex flex-wrap gap-2">
        <Button
          variant={!domainFilter ? "default" : "outline"}
          size="sm"
          onClick={() => setDomainFilter(undefined)}
        >
          All
        </Button>
        {DOMAINS.map((d) => (
          <Button
            key={d}
            variant={domainFilter === d ? "default" : "outline"}
            size="sm"
            onClick={() => setDomainFilter(d)}
          >
            {d}
          </Button>
        ))}
      </div>

      {isLoading ? (
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {[1, 2, 3, 4, 5, 6].map((i) => (
            <Skeleton key={i} className="h-36 w-full rounded-xl" />
          ))}
        </div>
      ) : templates.length > 0 ? (
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {templates.map((template) => (
            <Card key={template.id}>
              <CardHeader className="pb-3">
                <div className="flex items-center justify-between">
                  <Badge variant="outline">{template.template_code}</Badge>
                  <Badge variant="secondary">{template.automation_level}</Badge>
                </div>
                <CardTitle className="mt-2 text-base">{template.title}</CardTitle>
              </CardHeader>
              <CardContent>
                <Badge>{template.domain}</Badge>
              </CardContent>
            </Card>
          ))}
        </div>
      ) : (
        <Card>
          <CardContent className="p-12 text-center">
            <FileStack className="mx-auto h-12 w-12 text-muted-foreground" />
            <h3 className="mt-4 text-lg font-semibold">No templates loaded</h3>
            <p className="mt-2 text-sm text-muted-foreground">
              Run the seed script to load control templates.
            </p>
          </CardContent>
        </Card>
      )}
    </div>
  );
}

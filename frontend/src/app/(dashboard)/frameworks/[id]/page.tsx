"use client";

import { useParams } from "next/navigation";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Skeleton } from "@/components/ui/skeleton";
import { useFramework } from "@/hooks/use-api";
import { ChevronDown, ChevronRight } from "lucide-react";
import { useState } from "react";

export default function FrameworkDetailPage() {
  const params = useParams();
  const { data: framework, isLoading } = useFramework(params.id as string);

  if (isLoading) {
    return (
      <div className="space-y-4">
        <Skeleton className="h-10 w-64" />
        {[1, 2, 3].map((i) => (
          <Skeleton key={i} className="h-24 w-full" />
        ))}
      </div>
    );
  }

  if (!framework) {
    return <p>Framework not found.</p>;
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold">{framework.name}</h1>
        <p className="text-muted-foreground">
          Version {framework.version} &middot; {framework.category}
        </p>
        {framework.description && (
          <p className="mt-2 text-sm">{framework.description}</p>
        )}
      </div>

      <div className="space-y-3">
        {framework.domains?.map((domain) => (
          <DomainCard key={domain.id} domain={domain} />
        ))}
      </div>
    </div>
  );
}

function DomainCard({ domain }: { domain: any }) {
  const [expanded, setExpanded] = useState(false);

  return (
    <Card>
      <CardHeader
        className="cursor-pointer"
        onClick={() => setExpanded(!expanded)}
      >
        <div className="flex items-center gap-3">
          {expanded ? (
            <ChevronDown className="h-4 w-4" />
          ) : (
            <ChevronRight className="h-4 w-4" />
          )}
          <div className="flex-1">
            <CardTitle className="text-base">
              {domain.code} — {domain.name}
            </CardTitle>
            {domain.description && (
              <p className="mt-1 text-sm text-muted-foreground">
                {domain.description}
              </p>
            )}
          </div>
          <Badge variant="outline">
            {domain.requirements?.length || 0} requirements
          </Badge>
        </div>
      </CardHeader>
      {expanded && (
        <CardContent>
          <div className="space-y-3">
            {domain.requirements?.map((req: any) => (
              <div key={req.id} className="rounded-lg border p-3">
                <div className="font-medium text-sm">
                  {req.code}: {req.title}
                </div>
                {req.description && (
                  <p className="mt-1 text-xs text-muted-foreground">
                    {req.description}
                  </p>
                )}
                {req.objectives && req.objectives.length > 0 && (
                  <div className="mt-2 space-y-1 pl-4 border-l-2">
                    {req.objectives.map((obj: any) => (
                      <div key={obj.id} className="text-xs text-muted-foreground">
                        {obj.code}: {obj.title}
                      </div>
                    ))}
                  </div>
                )}
              </div>
            ))}
          </div>
        </CardContent>
      )}
    </Card>
  );
}

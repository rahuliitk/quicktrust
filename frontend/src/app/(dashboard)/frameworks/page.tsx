"use client";

import Link from "next/link";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Skeleton } from "@/components/ui/skeleton";
import { useFrameworks } from "@/hooks/use-api";
import { Shield } from "lucide-react";

export default function FrameworksPage() {
  const { data: frameworks, isLoading } = useFrameworks();

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold">Frameworks</h1>
        <p className="text-muted-foreground">Compliance frameworks and their requirements</p>
      </div>

      {isLoading ? (
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {[1, 2, 3].map((i) => (
            <Skeleton key={i} className="h-48 w-full rounded-xl" />
          ))}
        </div>
      ) : frameworks && frameworks.length > 0 ? (
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {frameworks.map((fw) => (
            <Link key={fw.id} href={`/frameworks/${fw.id}`}>
              <Card className="cursor-pointer transition-shadow hover:shadow-lg">
                <CardHeader>
                  <div className="flex items-center justify-between">
                    <Shield className="h-8 w-8 text-primary" />
                    <Badge variant={fw.is_active ? "success" : "secondary"}>
                      {fw.is_active ? "Active" : "Inactive"}
                    </Badge>
                  </div>
                  <CardTitle className="mt-2">{fw.name}</CardTitle>
                  <CardDescription>Version {fw.version}</CardDescription>
                </CardHeader>
                <CardContent>
                  <p className="text-sm text-muted-foreground line-clamp-2">
                    {fw.description || "No description available."}
                  </p>
                  {fw.category && (
                    <Badge variant="outline" className="mt-3">
                      {fw.category}
                    </Badge>
                  )}
                </CardContent>
              </Card>
            </Link>
          ))}
        </div>
      ) : (
        <Card>
          <CardContent className="p-12 text-center">
            <Shield className="mx-auto h-12 w-12 text-muted-foreground" />
            <h3 className="mt-4 text-lg font-semibold">No frameworks loaded</h3>
            <p className="mt-2 text-sm text-muted-foreground">
              Run the seed script to load the SOC 2 framework.
            </p>
          </CardContent>
        </Card>
      )}
    </div>
  );
}

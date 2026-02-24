"use client";

import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Skeleton } from "@/components/ui/skeleton";
import { useAuditorMarketplace } from "@/hooks/use-api";
import {
  Search,
  ShieldCheck,
  MapPin,
  Star,
  Briefcase,
  ExternalLink,
} from "lucide-react";

export default function AuditorMarketplacePage() {
  const [specialization, setSpecialization] = useState<string | undefined>();
  const [verifiedOnly, setVerifiedOnly] = useState(false);
  const { data: auditors, isLoading } = useAuditorMarketplace({
    specialization,
    verified_only: verifiedOnly,
  });

  const specializations = [
    "SOC 2",
    "ISO 27001",
    "HIPAA",
    "PCI DSS",
    "GDPR",
    "FedRAMP",
  ];

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold">Auditor Marketplace</h1>
        <p className="text-muted-foreground">
          Find verified auditors for your compliance needs
        </p>
      </div>

      {/* Filters */}
      <div className="flex flex-wrap gap-2 items-center">
        <Search className="h-4 w-4 text-muted-foreground" />
        <Button
          size="sm"
          variant={!specialization ? "default" : "outline"}
          onClick={() => setSpecialization(undefined)}
        >
          All
        </Button>
        {specializations.map((s) => (
          <Button
            key={s}
            size="sm"
            variant={specialization === s ? "default" : "outline"}
            onClick={() => setSpecialization(s)}
          >
            {s}
          </Button>
        ))}
        <span className="border-l mx-2" />
        <Button
          size="sm"
          variant={verifiedOnly ? "default" : "outline"}
          onClick={() => setVerifiedOnly(!verifiedOnly)}
        >
          <ShieldCheck className="h-4 w-4 mr-1" />
          Verified Only
        </Button>
      </div>

      {/* Results */}
      {isLoading ? (
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {[1, 2, 3, 4, 5, 6].map((i) => (
            <Skeleton key={i} className="h-48 w-full" />
          ))}
        </div>
      ) : auditors?.items?.length === 0 ? (
        <Card>
          <CardContent className="flex flex-col items-center justify-center p-12">
            <Search className="h-12 w-12 text-muted-foreground mb-4" />
            <p className="text-muted-foreground">
              No auditors found matching your criteria
            </p>
          </CardContent>
        </Card>
      ) : (
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {auditors?.items?.map((auditor: any) => (
            <Card key={auditor.id} className="hover:shadow-md transition-shadow">
              <CardHeader className="pb-3">
                <div className="flex items-start justify-between">
                  <div>
                    <CardTitle className="text-lg">
                      {auditor.user_name || "Unnamed Auditor"}
                    </CardTitle>
                    {auditor.firm_name && (
                      <p className="text-sm text-muted-foreground">
                        {auditor.firm_name}
                      </p>
                    )}
                  </div>
                  {auditor.is_verified && (
                    <Badge className="bg-green-100 text-green-800">
                      <ShieldCheck className="h-3 w-3 mr-1" />
                      Verified
                    </Badge>
                  )}
                </div>
              </CardHeader>
              <CardContent className="space-y-3">
                {auditor.bio && (
                  <p className="text-sm text-muted-foreground line-clamp-2">
                    {auditor.bio}
                  </p>
                )}
                <div className="flex flex-wrap gap-1">
                  {auditor.specializations?.map((s: string) => (
                    <Badge key={s} variant="outline" className="text-xs">
                      {s}
                    </Badge>
                  ))}
                </div>
                <div className="flex flex-wrap gap-1">
                  {auditor.credentials?.map((c: string) => (
                    <Badge key={c} variant="secondary" className="text-xs">
                      {c}
                    </Badge>
                  ))}
                </div>
                <div className="flex items-center gap-4 text-xs text-muted-foreground">
                  {auditor.location && (
                    <span className="flex items-center gap-1">
                      <MapPin className="h-3 w-3" />
                      {auditor.location}
                    </span>
                  )}
                  {auditor.years_experience && (
                    <span className="flex items-center gap-1">
                      <Briefcase className="h-3 w-3" />
                      {auditor.years_experience}yr exp
                    </span>
                  )}
                  {auditor.rating && (
                    <span className="flex items-center gap-1">
                      <Star className="h-3 w-3" />
                      {auditor.rating.toFixed(1)}
                    </span>
                  )}
                </div>
                <div className="flex items-center justify-between pt-2 border-t">
                  {auditor.hourly_rate ? (
                    <span className="text-sm font-medium">
                      ${auditor.hourly_rate}/hr
                    </span>
                  ) : (
                    <span className="text-sm text-muted-foreground">
                      Contact for pricing
                    </span>
                  )}
                  {auditor.website_url && (
                    <a
                      href={auditor.website_url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-sm text-primary flex items-center gap-1"
                    >
                      Website <ExternalLink className="h-3 w-3" />
                    </a>
                  )}
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
}

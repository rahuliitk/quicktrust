"use client";

import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Skeleton } from "@/components/ui/skeleton";
import { useAuditLogs, useAuditLogStats } from "@/hooks/use-api";
import { useOrgId } from "@/hooks/use-org-id";
import { History, Filter } from "lucide-react";

const actionColors: Record<string, string> = {
  create: "bg-green-100 text-green-800",
  update: "bg-blue-100 text-blue-800",
  delete: "bg-red-100 text-red-800",
  approve: "bg-purple-100 text-purple-800",
  publish: "bg-indigo-100 text-indigo-800",
};

export default function AuditLogPage() {
  const orgId = useOrgId();
  const [entityFilter, setEntityFilter] = useState<string | undefined>();
  const [actionFilter, setActionFilter] = useState<string | undefined>();
  const { data: logs, isLoading } = useAuditLogs(orgId, {
    entity_type: entityFilter,
    action: actionFilter,
  });
  const { data: stats } = useAuditLogStats(orgId);

  const entityTypes = stats?.by_entity_type
    ? Object.keys(stats.by_entity_type)
    : [];
  const actions = stats?.by_action ? Object.keys(stats.by_action) : [];

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold">Audit Log</h1>
        <p className="text-muted-foreground">
          Track all changes across your organization
        </p>
      </div>

      {/* Stats */}
      {stats && (
        <div className="grid gap-4 md:grid-cols-3">
          <Card>
            <CardContent className="p-4">
              <div className="text-2xl font-bold">{stats.total}</div>
              <p className="text-xs text-muted-foreground">Total Events</p>
            </CardContent>
          </Card>
          <Card>
            <CardContent className="p-4">
              <div className="text-2xl font-bold">
                {Object.keys(stats.by_entity_type || {}).length}
              </div>
              <p className="text-xs text-muted-foreground">Entity Types</p>
            </CardContent>
          </Card>
          <Card>
            <CardContent className="p-4">
              <div className="text-2xl font-bold">
                {Object.keys(stats.by_action || {}).length}
              </div>
              <p className="text-xs text-muted-foreground">Action Types</p>
            </CardContent>
          </Card>
        </div>
      )}

      {/* Filters */}
      <div className="flex flex-wrap gap-2">
        <Filter className="h-4 w-4 mt-2 text-muted-foreground" />
        <Button
          size="sm"
          variant={!entityFilter ? "default" : "outline"}
          onClick={() => setEntityFilter(undefined)}
        >
          All Entities
        </Button>
        {entityTypes.map((et) => (
          <Button
            key={et}
            size="sm"
            variant={entityFilter === et ? "default" : "outline"}
            onClick={() => setEntityFilter(et)}
          >
            {et}
          </Button>
        ))}
        <span className="border-l mx-2" />
        <Button
          size="sm"
          variant={!actionFilter ? "default" : "outline"}
          onClick={() => setActionFilter(undefined)}
        >
          All Actions
        </Button>
        {actions.map((a) => (
          <Button
            key={a}
            size="sm"
            variant={actionFilter === a ? "default" : "outline"}
            onClick={() => setActionFilter(a)}
          >
            {a}
          </Button>
        ))}
      </div>

      {/* Log entries */}
      {isLoading ? (
        <div className="space-y-3">
          {[1, 2, 3, 4, 5].map((i) => (
            <Skeleton key={i} className="h-16 w-full" />
          ))}
        </div>
      ) : logs?.items?.length === 0 ? (
        <Card>
          <CardContent className="flex flex-col items-center justify-center p-12">
            <History className="h-12 w-12 text-muted-foreground mb-4" />
            <p className="text-muted-foreground">No audit log entries found</p>
          </CardContent>
        </Card>
      ) : (
        <div className="space-y-2">
          {logs?.items?.map((log: any) => (
            <Card key={log.id}>
              <CardContent className="flex items-center gap-4 p-4">
                <div className="flex-1">
                  <div className="flex items-center gap-2">
                    <Badge
                      className={
                        actionColors[log.action] || "bg-gray-100 text-gray-800"
                      }
                    >
                      {log.action}
                    </Badge>
                    <Badge variant="outline">{log.entity_type}</Badge>
                    <span className="text-sm text-muted-foreground">
                      {log.entity_id}
                    </span>
                  </div>
                  <p className="text-xs text-muted-foreground mt-1">
                    Actor: {log.actor_id} ({log.actor_type}) | IP:{" "}
                    {log.ip_address || "N/A"}
                  </p>
                </div>
                <div className="text-xs text-muted-foreground text-right">
                  {new Date(log.timestamp).toLocaleString()}
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
}

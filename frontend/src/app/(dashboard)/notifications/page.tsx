"use client";

import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Skeleton } from "@/components/ui/skeleton";
import {
  useNotifications,
  useNotificationStats,
  useMarkNotificationRead,
  useMarkAllNotificationsRead,
} from "@/hooks/use-api";
import { useOrgId } from "@/hooks/use-org-id";
import { Bell, CheckCircle, AlertTriangle, AlertCircle, Info } from "lucide-react";

const severityConfig: Record<string, { icon: typeof Info; color: string }> = {
  info: { icon: Info, color: "text-blue-500" },
  warning: { icon: AlertTriangle, color: "text-yellow-500" },
  critical: { icon: AlertCircle, color: "text-red-500" },
};

export default function NotificationsPage() {
  const orgId = useOrgId();
  const [filter, setFilter] = useState<boolean | undefined>(undefined);
  const { data: notifications, isLoading } = useNotifications(orgId, filter);
  const { data: stats } = useNotificationStats(orgId);
  const markRead = useMarkNotificationRead();
  const markAllRead = useMarkAllNotificationsRead();

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold">Notifications</h1>
          <p className="text-muted-foreground">
            Stay updated on compliance events and alerts
          </p>
        </div>
        <div className="flex gap-2">
          <Button
            variant={filter === undefined ? "default" : "outline"}
            size="sm"
            onClick={() => setFilter(undefined)}
          >
            All ({stats?.total || 0})
          </Button>
          <Button
            variant={filter === false ? "default" : "outline"}
            size="sm"
            onClick={() => setFilter(false)}
          >
            Unread ({stats?.unread || 0})
          </Button>
          <Button
            variant="outline"
            size="sm"
            onClick={() => markAllRead.mutate({ orgId })}
          >
            <CheckCircle className="h-4 w-4 mr-1" />
            Mark All Read
          </Button>
        </div>
      </div>

      {/* Stats */}
      {stats && (
        <div className="grid gap-4 md:grid-cols-4">
          <Card>
            <CardContent className="p-4">
              <div className="text-2xl font-bold">{stats.total}</div>
              <p className="text-xs text-muted-foreground">Total</p>
            </CardContent>
          </Card>
          <Card>
            <CardContent className="p-4">
              <div className="text-2xl font-bold text-blue-600">{stats.unread}</div>
              <p className="text-xs text-muted-foreground">Unread</p>
            </CardContent>
          </Card>
          <Card>
            <CardContent className="p-4">
              <div className="text-2xl font-bold text-yellow-600">
                {stats.by_severity?.warning || 0}
              </div>
              <p className="text-xs text-muted-foreground">Warnings</p>
            </CardContent>
          </Card>
          <Card>
            <CardContent className="p-4">
              <div className="text-2xl font-bold text-red-600">
                {stats.by_severity?.critical || 0}
              </div>
              <p className="text-xs text-muted-foreground">Critical</p>
            </CardContent>
          </Card>
        </div>
      )}

      {/* Notification list */}
      {isLoading ? (
        <div className="space-y-3">
          {[1, 2, 3].map((i) => (
            <Skeleton key={i} className="h-20 w-full" />
          ))}
        </div>
      ) : (
        <div className="space-y-2">
          {notifications?.items?.length === 0 && (
            <Card>
              <CardContent className="flex flex-col items-center justify-center p-12">
                <Bell className="h-12 w-12 text-muted-foreground mb-4" />
                <p className="text-muted-foreground">No notifications</p>
              </CardContent>
            </Card>
          )}
          {notifications?.items?.map((n: any) => {
            const config = severityConfig[n.severity] || severityConfig.info;
            const Icon = config.icon;
            return (
              <Card
                key={n.id}
                className={`cursor-pointer transition-colors ${
                  !n.is_read ? "border-primary/30 bg-primary/5" : ""
                }`}
                onClick={() => {
                  if (!n.is_read) {
                    markRead.mutate({ orgId, notificationId: n.id });
                  }
                }}
              >
                <CardContent className="flex items-start gap-4 p-4">
                  <Icon className={`h-5 w-5 mt-0.5 ${config.color}`} />
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2">
                      <span className="font-medium">{n.title}</span>
                      {!n.is_read && (
                        <Badge variant="default" className="text-[10px] px-1.5 py-0">
                          New
                        </Badge>
                      )}
                      <Badge variant="outline" className="text-[10px]">
                        {n.category}
                      </Badge>
                    </div>
                    <p className="text-sm text-muted-foreground mt-1">{n.message}</p>
                    <p className="text-xs text-muted-foreground mt-1">
                      {new Date(n.created_at).toLocaleString()}
                    </p>
                  </div>
                </CardContent>
              </Card>
            );
          })}
        </div>
      )}
    </div>
  );
}

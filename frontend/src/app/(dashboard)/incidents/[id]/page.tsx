"use client";

import { useState } from "react";
import Link from "next/link";
import { useParams, useRouter } from "next/navigation";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Skeleton } from "@/components/ui/skeleton";
import {
  useIncident,
  useUpdateIncident,
  useDeleteIncident,
  useAddTimelineEvent,
  useIncidentTimeline,
} from "@/hooks/use-api";
import {
  ArrowLeft,
  Pencil,
  Trash2,
  Loader2,
  Save,
  X,
  Clock,
  Plus,
} from "lucide-react";

const DEMO_ORG_ID = "00000000-0000-0000-0000-000000000000";

const severityColor: Record<string, string> = {
  P1: "bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-100",
  P2: "bg-orange-100 text-orange-800 dark:bg-orange-900 dark:text-orange-100",
  P3: "bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-100",
  P4: "bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-100",
};

const statusColor: Record<string, string> = {
  open: "bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-100",
  investigating:
    "bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-100",
  resolved:
    "bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-100",
  closed: "bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-100",
};

const eventTypeColor: Record<string, string> = {
  note: "bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-100",
  status_change:
    "bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-100",
  escalation:
    "bg-orange-100 text-orange-800 dark:bg-orange-900 dark:text-orange-100",
  resolution:
    "bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-100",
};

export default function IncidentDetailPage() {
  const params = useParams();
  const router = useRouter();
  const incidentId = params.id as string;

  const { data: incident, isLoading } = useIncident(DEMO_ORG_ID, incidentId);
  const { data: timeline, isLoading: timelineLoading } = useIncidentTimeline(
    DEMO_ORG_ID,
    incidentId
  );
  const updateIncident = useUpdateIncident(DEMO_ORG_ID);
  const deleteIncident = useDeleteIncident(DEMO_ORG_ID);
  const addTimelineEvent = useAddTimelineEvent(DEMO_ORG_ID, incidentId);

  const [editing, setEditing] = useState(false);
  const [form, setForm] = useState({
    title: "",
    description: "",
    severity: "P3",
    status: "open",
    category: "",
    post_mortem_notes: "",
  });

  const [noteText, setNoteText] = useState("");
  const [showAddNote, setShowAddNote] = useState(false);

  function enterEditMode() {
    if (!incident) return;
    setForm({
      title: incident.title || "",
      description: incident.description || "",
      severity: incident.severity || "P3",
      status: incident.status || "open",
      category: incident.category || "",
      post_mortem_notes: incident.post_mortem_notes || "",
    });
    setEditing(true);
  }

  function handleSave() {
    if (!incident) return;
    updateIncident.mutate(
      { incidentId: incident.id, ...form },
      { onSuccess: () => setEditing(false) }
    );
  }

  function handleDelete() {
    if (!incident) return;
    const confirmed = window.confirm(
      `Are you sure you want to delete "${incident.title}"? This action cannot be undone.`
    );
    if (!confirmed) return;
    deleteIncident.mutate(incident.id, {
      onSuccess: () => router.push("/incidents"),
    });
  }

  function handleAddNote() {
    if (!noteText.trim()) return;
    addTimelineEvent.mutate(
      { event_type: "note", description: noteText.trim() },
      {
        onSuccess: () => {
          setNoteText("");
          setShowAddNote(false);
        },
      }
    );
  }

  if (isLoading) {
    return (
      <div className="space-y-4">
        <Skeleton className="h-6 w-32" />
        <Skeleton className="h-10 w-64" />
        <Skeleton className="h-64 w-full" />
      </div>
    );
  }

  if (!incident) return <p>Incident not found.</p>;

  return (
    <div className="space-y-6">
      <Link
        href="/incidents"
        className="inline-flex items-center gap-1 text-sm text-muted-foreground hover:text-foreground transition-colors"
      >
        <ArrowLeft className="h-4 w-4" />
        Back to Incidents
      </Link>

      {/* Header */}
      <div className="flex items-center gap-3">
        <h1 className="text-3xl font-bold">{incident.title}</h1>
        <Badge className={severityColor[incident.severity] || ""}>
          {incident.severity}
        </Badge>
        <Badge className={statusColor[incident.status] || ""}>
          {incident.status}
        </Badge>
        <div className="ml-auto flex items-center gap-2">
          {!editing && (
            <Button variant="outline" size="sm" onClick={enterEditMode}>
              <Pencil className="mr-1 h-4 w-4" />
              Edit
            </Button>
          )}
          <Button
            variant="destructive"
            size="sm"
            onClick={handleDelete}
            disabled={deleteIncident.isPending}
          >
            {deleteIncident.isPending ? (
              <Loader2 className="mr-1 h-4 w-4 animate-spin" />
            ) : (
              <Trash2 className="mr-1 h-4 w-4" />
            )}
            Delete
          </Button>
        </div>
      </div>

      <p className="text-sm text-muted-foreground">
        {incident.category && (
          <span className="capitalize">{incident.category} &middot; </span>
        )}
        Created {new Date(incident.created_at).toLocaleDateString()}
      </p>

      {/* Edit Form */}
      {editing && (
        <Card>
          <CardHeader>
            <CardTitle>Edit Incident</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div>
              <label className="text-sm font-medium">Title</label>
              <input
                type="text"
                className="mt-1 w-full rounded-md border bg-background p-2 text-sm"
                value={form.title}
                onChange={(e) => setForm({ ...form, title: e.target.value })}
              />
            </div>

            <div>
              <label className="text-sm font-medium">Description</label>
              <textarea
                className="mt-1 w-full rounded-md border bg-background p-2 text-sm"
                rows={4}
                value={form.description}
                onChange={(e) =>
                  setForm({ ...form, description: e.target.value })
                }
              />
            </div>

            <div className="grid grid-cols-3 gap-4">
              <div>
                <label className="text-sm font-medium">Severity</label>
                <select
                  className="mt-1 w-full rounded-md border bg-background p-2 text-sm"
                  value={form.severity}
                  onChange={(e) =>
                    setForm({ ...form, severity: e.target.value })
                  }
                >
                  <option value="P1">P1 - Critical</option>
                  <option value="P2">P2 - High</option>
                  <option value="P3">P3 - Medium</option>
                  <option value="P4">P4 - Low</option>
                </select>
              </div>

              <div>
                <label className="text-sm font-medium">Status</label>
                <select
                  className="mt-1 w-full rounded-md border bg-background p-2 text-sm"
                  value={form.status}
                  onChange={(e) =>
                    setForm({ ...form, status: e.target.value })
                  }
                >
                  <option value="open">Open</option>
                  <option value="investigating">Investigating</option>
                  <option value="resolved">Resolved</option>
                  <option value="closed">Closed</option>
                </select>
              </div>

              <div>
                <label className="text-sm font-medium">Category</label>
                <input
                  type="text"
                  className="mt-1 w-full rounded-md border bg-background p-2 text-sm"
                  value={form.category}
                  onChange={(e) =>
                    setForm({ ...form, category: e.target.value })
                  }
                />
              </div>
            </div>

            <div>
              <label className="text-sm font-medium">Post-Mortem Notes</label>
              <textarea
                className="mt-1 w-full rounded-md border bg-background p-2 text-sm"
                rows={4}
                placeholder="Post-mortem analysis and lessons learned..."
                value={form.post_mortem_notes}
                onChange={(e) =>
                  setForm({ ...form, post_mortem_notes: e.target.value })
                }
              />
            </div>

            <div className="flex items-center gap-2">
              <Button
                size="sm"
                onClick={handleSave}
                disabled={updateIncident.isPending}
              >
                {updateIncident.isPending ? (
                  <Loader2 className="mr-1 h-4 w-4 animate-spin" />
                ) : (
                  <Save className="mr-1 h-4 w-4" />
                )}
                Save
              </Button>
              <Button
                variant="outline"
                size="sm"
                onClick={() => setEditing(false)}
                disabled={updateIncident.isPending}
              >
                <X className="mr-1 h-4 w-4" />
                Cancel
              </Button>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Description */}
      {incident.description && !editing && (
        <Card>
          <CardHeader>
            <CardTitle>Description</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="whitespace-pre-wrap">{incident.description}</p>
          </CardContent>
        </Card>
      )}

      {/* Post-mortem */}
      {incident.post_mortem_notes && !editing && (
        <Card>
          <CardHeader>
            <CardTitle>Post-Mortem Notes</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="whitespace-pre-wrap">{incident.post_mortem_notes}</p>
          </CardContent>
        </Card>
      )}

      {/* Timeline */}
      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <CardTitle>Timeline</CardTitle>
            <Button
              size="sm"
              variant="outline"
              onClick={() => setShowAddNote((v) => !v)}
            >
              <Plus className="mr-1 h-4 w-4" />
              Add Note
            </Button>
          </div>
        </CardHeader>
        <CardContent className="space-y-4">
          {showAddNote && (
            <div className="space-y-3 rounded-lg border p-4">
              <textarea
                className="w-full rounded-md border bg-background p-2 text-sm"
                rows={3}
                placeholder="Add a timeline note..."
                value={noteText}
                onChange={(e) => setNoteText(e.target.value)}
              />
              <div className="flex gap-2">
                <Button
                  size="sm"
                  onClick={handleAddNote}
                  disabled={!noteText.trim() || addTimelineEvent.isPending}
                >
                  {addTimelineEvent.isPending && (
                    <Loader2 className="mr-1 h-4 w-4 animate-spin" />
                  )}
                  Add Note
                </Button>
                <Button
                  size="sm"
                  variant="ghost"
                  onClick={() => {
                    setShowAddNote(false);
                    setNoteText("");
                  }}
                >
                  Cancel
                </Button>
              </div>
            </div>
          )}

          {timelineLoading ? (
            <div className="space-y-3">
              {[1, 2, 3].map((i) => (
                <Skeleton key={i} className="h-16 w-full rounded-lg" />
              ))}
            </div>
          ) : timeline && timeline.length > 0 ? (
            <div className="space-y-3">
              {timeline.map((event: any) => (
                <div
                  key={event.id}
                  className="flex items-start gap-3 rounded-lg border p-3"
                >
                  <Clock className="mt-0.5 h-4 w-4 text-muted-foreground shrink-0" />
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2">
                      <Badge
                        className={
                          eventTypeColor[event.event_type] ||
                          "bg-gray-100 text-gray-800"
                        }
                      >
                        {event.event_type?.replace(/_/g, " ")}
                      </Badge>
                      <span className="text-xs text-muted-foreground">
                        {event.created_at &&
                          new Date(event.created_at).toLocaleString()}
                      </span>
                    </div>
                    <p className="mt-1 text-sm">{event.description}</p>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="flex flex-col items-center justify-center py-6 text-center">
              <Clock className="h-10 w-10 text-muted-foreground mb-3" />
              <p className="text-sm text-muted-foreground">
                No timeline events yet.
              </p>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}

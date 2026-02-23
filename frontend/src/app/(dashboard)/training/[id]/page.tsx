"use client";

import { useState } from "react";
import Link from "next/link";
import { useParams, useRouter } from "next/navigation";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Skeleton } from "@/components/ui/skeleton";
import {
  useTrainingCourse,
  useUpdateTrainingCourse,
  useDeleteTrainingCourse,
  useTrainingAssignments,
} from "@/hooks/use-api";
import {
  ArrowLeft,
  Pencil,
  Trash2,
  Loader2,
  Save,
  X,
  GraduationCap,
  Users,
} from "lucide-react";

const DEMO_ORG_ID = "00000000-0000-0000-0000-000000000000";

const assignmentStatusColor: Record<string, string> = {
  assigned: "bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-100",
  in_progress:
    "bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-100",
  completed:
    "bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-100",
  overdue: "bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-100",
};

export default function TrainingCourseDetailPage() {
  const params = useParams();
  const router = useRouter();
  const courseId = params.id as string;

  const { data: course, isLoading } = useTrainingCourse(
    DEMO_ORG_ID,
    courseId
  );
  const { data: assignmentsData, isLoading: assignmentsLoading } =
    useTrainingAssignments(DEMO_ORG_ID, { course_id: courseId });
  const updateCourse = useUpdateTrainingCourse(DEMO_ORG_ID);
  const deleteCourse = useDeleteTrainingCourse(DEMO_ORG_ID);

  const [editing, setEditing] = useState(false);
  const [form, setForm] = useState({
    title: "",
    description: "",
    course_type: "",
    duration_minutes: 30,
    is_required: false,
  });

  function enterEditMode() {
    if (!course) return;
    setForm({
      title: course.title || "",
      description: course.description || "",
      course_type: course.course_type || "security_awareness",
      duration_minutes: course.duration_minutes || 30,
      is_required: course.is_required || false,
    });
    setEditing(true);
  }

  function handleSave() {
    if (!course) return;
    updateCourse.mutate(
      { courseId: course.id, ...form },
      { onSuccess: () => setEditing(false) }
    );
  }

  function handleDelete() {
    if (!course) return;
    const confirmed = window.confirm(
      `Are you sure you want to delete "${course.title}"? This action cannot be undone.`
    );
    if (!confirmed) return;
    deleteCourse.mutate(course.id, {
      onSuccess: () => router.push("/training"),
    });
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

  if (!course) return <p>Course not found.</p>;

  const assignments = assignmentsData?.items || [];

  return (
    <div className="space-y-6">
      <Link
        href="/training"
        className="inline-flex items-center gap-1 text-sm text-muted-foreground hover:text-foreground transition-colors"
      >
        <ArrowLeft className="h-4 w-4" />
        Back to Training
      </Link>

      {/* Header */}
      <div className="flex items-center gap-3">
        <h1 className="text-3xl font-bold">{course.title}</h1>
        <Badge variant="outline" className="capitalize">
          {course.course_type?.replace(/_/g, " ")}
        </Badge>
        {course.is_required && (
          <Badge variant="destructive">Required</Badge>
        )}
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
            disabled={deleteCourse.isPending}
          >
            {deleteCourse.isPending ? (
              <Loader2 className="mr-1 h-4 w-4 animate-spin" />
            ) : (
              <Trash2 className="mr-1 h-4 w-4" />
            )}
            Delete
          </Button>
        </div>
      </div>

      {/* Edit Form */}
      {editing && (
        <Card>
          <CardHeader>
            <CardTitle>Edit Course</CardTitle>
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
                <label className="text-sm font-medium">Course Type</label>
                <select
                  className="mt-1 w-full rounded-md border bg-background p-2 text-sm"
                  value={form.course_type}
                  onChange={(e) =>
                    setForm({ ...form, course_type: e.target.value })
                  }
                >
                  <option value="security_awareness">
                    Security Awareness
                  </option>
                  <option value="compliance">Compliance</option>
                  <option value="privacy">Privacy</option>
                  <option value="phishing">Phishing</option>
                  <option value="custom">Custom</option>
                </select>
              </div>

              <div>
                <label className="text-sm font-medium">
                  Duration (minutes)
                </label>
                <input
                  type="number"
                  min={1}
                  className="mt-1 w-full rounded-md border bg-background p-2 text-sm"
                  value={form.duration_minutes}
                  onChange={(e) =>
                    setForm({
                      ...form,
                      duration_minutes: Number(e.target.value),
                    })
                  }
                />
              </div>

              <div>
                <label className="text-sm font-medium">Required</label>
                <div className="flex items-center gap-2 mt-2">
                  <input
                    type="checkbox"
                    checked={form.is_required}
                    onChange={(e) =>
                      setForm({ ...form, is_required: e.target.checked })
                    }
                    className="h-4 w-4 rounded border"
                  />
                  <span className="text-sm">Required</span>
                </div>
              </div>
            </div>

            <div className="flex items-center gap-2">
              <Button
                size="sm"
                onClick={handleSave}
                disabled={updateCourse.isPending}
              >
                {updateCourse.isPending ? (
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
                disabled={updateCourse.isPending}
              >
                <X className="mr-1 h-4 w-4" />
                Cancel
              </Button>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Course Details */}
      {!editing && (
        <Card>
          <CardHeader>
            <CardTitle>Course Details</CardTitle>
          </CardHeader>
          <CardContent>
            <dl className="space-y-3 text-sm">
              {course.description && (
                <div>
                  <dt className="font-medium text-muted-foreground">
                    Description
                  </dt>
                  <dd className="mt-1 whitespace-pre-wrap">
                    {course.description}
                  </dd>
                </div>
              )}
              <div>
                <dt className="font-medium text-muted-foreground">Duration</dt>
                <dd className="mt-1">{course.duration_minutes} minutes</dd>
              </div>
              <div>
                <dt className="font-medium text-muted-foreground">Created</dt>
                <dd className="mt-1">
                  {new Date(course.created_at).toLocaleDateString()}
                </dd>
              </div>
            </dl>
          </CardContent>
        </Card>
      )}

      {/* Assignments for this course */}
      <Card>
        <CardHeader>
          <CardTitle>
            Assignments{" "}
            {assignments.length > 0 && `(${assignments.length})`}
          </CardTitle>
        </CardHeader>
        <CardContent>
          {assignmentsLoading ? (
            <div className="space-y-3">
              {[1, 2, 3].map((i) => (
                <Skeleton key={i} className="h-16 w-full rounded-lg" />
              ))}
            </div>
          ) : assignments.length > 0 ? (
            <div className="space-y-3">
              {assignments.map((assignment: any) => (
                <div
                  key={assignment.id}
                  className="flex items-center gap-4 rounded-lg border p-3"
                >
                  <Users className="h-5 w-5 text-muted-foreground shrink-0" />
                  <div className="flex-1 min-w-0">
                    <div className="text-sm font-medium">
                      User: {assignment.user_id?.slice(0, 8)}...
                    </div>
                    <div className="mt-1 text-xs text-muted-foreground">
                      {assignment.due_date && (
                        <span>
                          Due:{" "}
                          {new Date(
                            assignment.due_date
                          ).toLocaleDateString()}
                        </span>
                      )}
                      {assignment.completed_at && (
                        <span>
                          {" "}
                          &middot; Completed:{" "}
                          {new Date(
                            assignment.completed_at
                          ).toLocaleDateString()}
                        </span>
                      )}
                    </div>
                  </div>
                  <Badge
                    className={
                      assignmentStatusColor[assignment.status] || ""
                    }
                  >
                    {assignment.status?.replace(/_/g, " ")}
                  </Badge>
                </div>
              ))}
            </div>
          ) : (
            <div className="flex flex-col items-center justify-center py-6 text-center">
              <GraduationCap className="h-10 w-10 text-muted-foreground mb-3" />
              <p className="text-sm text-muted-foreground">
                No assignments for this course yet.
              </p>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}

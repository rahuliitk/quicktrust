"use client";

import { useState } from "react";
import Link from "next/link";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Skeleton } from "@/components/ui/skeleton";
import {
  useTrainingCourses,
  useCreateTrainingCourse,
  useTrainingAssignments,
  useTrainingStats,
} from "@/hooks/use-api";
import { GraduationCap, BookOpen, Users, Plus, Loader2 } from "lucide-react";

const DEMO_ORG_ID = "00000000-0000-0000-0000-000000000000";

type TabValue = "courses" | "assignments";

const ASSIGNMENT_STATUS_FILTERS: { label: string; value: string | undefined }[] = [
  { label: "All", value: undefined },
  { label: "Assigned", value: "assigned" },
  { label: "In Progress", value: "in_progress" },
  { label: "Completed", value: "completed" },
  { label: "Overdue", value: "overdue" },
];

const assignmentStatusColor: Record<string, string> = {
  assigned: "bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-100",
  in_progress:
    "bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-100",
  completed:
    "bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-100",
  overdue: "bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-100",
};

export default function TrainingPage() {
  const [activeTab, setActiveTab] = useState<TabValue>("courses");
  const [assignmentStatusFilter, setAssignmentStatusFilter] = useState<
    string | undefined
  >(undefined);

  const { data: coursesData, isLoading: coursesLoading } =
    useTrainingCourses(DEMO_ORG_ID);
  const { data: assignmentsData, isLoading: assignmentsLoading } =
    useTrainingAssignments(DEMO_ORG_ID, { status: assignmentStatusFilter });
  const { data: stats } = useTrainingStats(DEMO_ORG_ID);

  const [showCreate, setShowCreate] = useState(false);
  const [form, setForm] = useState({
    title: "",
    description: "",
    course_type: "security_awareness",
    duration_minutes: 30,
    is_required: false,
  });
  const createCourse = useCreateTrainingCourse(DEMO_ORG_ID);

  const resetForm = () =>
    setForm({
      title: "",
      description: "",
      course_type: "security_awareness",
      duration_minutes: 30,
      is_required: false,
    });

  const handleCreate = () => {
    createCourse.mutate(form, {
      onSuccess: () => {
        setShowCreate(false);
        resetForm();
      },
    });
  };

  const courses = coursesData?.items || [];
  const assignments = assignmentsData?.items || [];

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold">Training</h1>
          <p className="text-muted-foreground">
            Manage security awareness training courses and assignments
          </p>
        </div>
      </div>

      {/* Stats */}
      {stats && (
        <div className="grid grid-cols-4 gap-4">
          {[
            { label: "Total Courses", value: stats.total_courses ?? 0 },
            { label: "Assignments", value: stats.total_assignments ?? 0 },
            { label: "Completed", value: stats.completed ?? 0 },
            { label: "Overdue", value: stats.overdue ?? 0 },
          ].map((s) => (
            <Card key={s.label}>
              <CardContent className="p-4 text-center">
                <div className="text-2xl font-bold">{s.value}</div>
                <div className="text-xs text-muted-foreground">{s.label}</div>
              </CardContent>
            </Card>
          ))}
        </div>
      )}

      {/* Tab buttons */}
      <div className="flex gap-2 border-b pb-1">
        <Button
          variant={activeTab === "courses" ? "default" : "ghost"}
          size="sm"
          onClick={() => setActiveTab("courses")}
          className="gap-1.5"
        >
          <BookOpen className="h-4 w-4" />
          Courses
        </Button>
        <Button
          variant={activeTab === "assignments" ? "default" : "ghost"}
          size="sm"
          onClick={() => setActiveTab("assignments")}
          className="gap-1.5"
        >
          <Users className="h-4 w-4" />
          Assignments
        </Button>
      </div>

      {/* Courses Tab */}
      {activeTab === "courses" && (
        <div className="space-y-4">
          <div className="flex justify-end">
            <Button
              size="sm"
              onClick={() => setShowCreate((v) => !v)}
              className="gap-1.5"
            >
              <Plus className="h-4 w-4" />
              New Course
            </Button>
          </div>

          {showCreate && (
            <Card>
              <CardContent className="p-4 space-y-4">
                <h2 className="text-lg font-semibold">Create New Course</h2>

                <div className="space-y-1">
                  <label className="text-sm font-medium">Title</label>
                  <input
                    type="text"
                    required
                    className="w-full rounded-md border bg-background p-2 text-sm"
                    placeholder="Course title"
                    value={form.title}
                    onChange={(e) =>
                      setForm({ ...form, title: e.target.value })
                    }
                  />
                </div>

                <div className="space-y-1">
                  <label className="text-sm font-medium">Description</label>
                  <textarea
                    className="w-full rounded-md border bg-background p-2 text-sm"
                    placeholder="Course description"
                    rows={3}
                    value={form.description}
                    onChange={(e) =>
                      setForm({ ...form, description: e.target.value })
                    }
                  />
                </div>

                <div className="grid grid-cols-3 gap-4">
                  <div className="space-y-1">
                    <label className="text-sm font-medium">Course Type</label>
                    <select
                      className="w-full rounded-md border bg-background p-2 text-sm"
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

                  <div className="space-y-1">
                    <label className="text-sm font-medium">
                      Duration (minutes)
                    </label>
                    <input
                      type="number"
                      min={1}
                      className="w-full rounded-md border bg-background p-2 text-sm"
                      value={form.duration_minutes}
                      onChange={(e) =>
                        setForm({
                          ...form,
                          duration_minutes: Number(e.target.value),
                        })
                      }
                    />
                  </div>

                  <div className="space-y-1">
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
                      <span className="text-sm">Mark as required</span>
                    </div>
                  </div>
                </div>

                <div className="flex items-center gap-2 pt-2">
                  <Button
                    onClick={handleCreate}
                    disabled={!form.title.trim() || createCourse.isPending}
                  >
                    {createCourse.isPending && (
                      <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                    )}
                    Create Course
                  </Button>
                  <Button
                    variant="outline"
                    onClick={() => {
                      setShowCreate(false);
                      resetForm();
                    }}
                  >
                    Cancel
                  </Button>
                </div>
              </CardContent>
            </Card>
          )}

          {coursesLoading ? (
            <div className="space-y-3">
              {[1, 2, 3].map((i) => (
                <Skeleton key={i} className="h-24 w-full rounded-xl" />
              ))}
            </div>
          ) : courses.length > 0 ? (
            <div className="space-y-3">
              {courses.map((course: any) => (
                <Link key={course.id} href={`/training/${course.id}`}>
                  <Card className="transition-colors hover:bg-accent/50">
                    <CardContent className="flex items-center gap-4 p-4">
                      <GraduationCap className="h-8 w-8 text-muted-foreground shrink-0" />
                      <div className="flex-1 min-w-0">
                        <div className="font-medium">{course.title}</div>
                        <div className="mt-1 text-xs text-muted-foreground">
                          {course.course_type?.replace(/_/g, " ")} &middot;{" "}
                          {course.duration_minutes} min
                        </div>
                      </div>
                      {course.is_required && (
                        <Badge variant="destructive">Required</Badge>
                      )}
                      <Badge variant="outline" className="capitalize">
                        {course.course_type?.replace(/_/g, " ")}
                      </Badge>
                    </CardContent>
                  </Card>
                </Link>
              ))}
            </div>
          ) : (
            <Card>
              <CardContent className="flex flex-col items-center justify-center p-12 text-center">
                <GraduationCap className="h-12 w-12 text-muted-foreground mb-4" />
                <h3 className="text-lg font-medium">No courses yet</h3>
                <p className="text-sm text-muted-foreground mt-1">
                  Create your first training course to get started.
                </p>
              </CardContent>
            </Card>
          )}
        </div>
      )}

      {/* Assignments Tab */}
      {activeTab === "assignments" && (
        <div className="space-y-4">
          <div className="flex flex-wrap gap-2">
            {ASSIGNMENT_STATUS_FILTERS.map((f) => (
              <Button
                key={f.label}
                variant={
                  assignmentStatusFilter === f.value ? "default" : "outline"
                }
                size="sm"
                onClick={() => setAssignmentStatusFilter(f.value)}
              >
                {f.label}
              </Button>
            ))}
          </div>

          {assignmentsLoading ? (
            <div className="space-y-3">
              {[1, 2, 3].map((i) => (
                <Skeleton key={i} className="h-20 w-full rounded-xl" />
              ))}
            </div>
          ) : assignments.length > 0 ? (
            <div className="space-y-3">
              {assignments.map((assignment: any) => (
                <Card key={assignment.id}>
                  <CardContent className="flex items-center gap-4 p-4">
                    <Users className="h-6 w-6 text-muted-foreground shrink-0" />
                    <div className="flex-1 min-w-0">
                      <div className="text-sm font-medium">
                        Course: {assignment.course_id?.slice(0, 8)}...
                      </div>
                      <div className="mt-1 text-xs text-muted-foreground">
                        User: {assignment.user_id?.slice(0, 8)}...
                        {assignment.due_date && (
                          <>
                            {" "}
                            &middot; Due:{" "}
                            {new Date(
                              assignment.due_date
                            ).toLocaleDateString()}
                          </>
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
                  </CardContent>
                </Card>
              ))}
            </div>
          ) : (
            <Card>
              <CardContent className="flex flex-col items-center justify-center p-12 text-center">
                <Users className="h-12 w-12 text-muted-foreground mb-4" />
                <h3 className="text-lg font-medium">No assignments found</h3>
                <p className="text-sm text-muted-foreground mt-1">
                  No training assignments match the current filters.
                </p>
              </CardContent>
            </Card>
          )}
        </div>
      )}
    </div>
  );
}

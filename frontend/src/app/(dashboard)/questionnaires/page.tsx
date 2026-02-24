"use client";

import { useState } from "react";
import Link from "next/link";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Skeleton } from "@/components/ui/skeleton";
import { Progress } from "@/components/ui/progress";
import {
  useQuestionnaires,
  useCreateQuestionnaire,
  useQuestionnaireStats,
} from "@/hooks/use-api";
import { useOrgId } from "@/hooks/use-org-id";
import { ClipboardList, Plus, Loader2, Trash2 } from "lucide-react";

const STATUS_FILTERS: { label: string; value: string | undefined }[] = [
  { label: "All", value: undefined },
  { label: "Draft", value: "draft" },
  { label: "In Progress", value: "in_progress" },
  { label: "Completed", value: "completed" },
  { label: "Sent", value: "sent" },
];

const statusColor: Record<string, string> = {
  draft: "bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-100",
  in_progress:
    "bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-100",
  completed:
    "bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-100",
  sent: "bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-100",
};

interface QuestionInput {
  question_text: string;
  question_type: string;
}

export default function QuestionnairesPage() {
  const orgId = useOrgId();
  const [statusFilter, setStatusFilter] = useState<string | undefined>(
    undefined
  );
  const { data, isLoading } = useQuestionnaires(orgId, {
    status: statusFilter,
  });
  const { data: stats } = useQuestionnaireStats(orgId);

  const [showCreate, setShowCreate] = useState(false);
  const [form, setForm] = useState({
    title: "",
    source: "",
  });
  const [questions, setQuestions] = useState<QuestionInput[]>([
    { question_text: "", question_type: "text" },
  ]);
  const createQuestionnaire = useCreateQuestionnaire(orgId);

  const resetForm = () => {
    setForm({ title: "", source: "" });
    setQuestions([{ question_text: "", question_type: "text" }]);
  };

  const addQuestion = () => {
    setQuestions([...questions, { question_text: "", question_type: "text" }]);
  };

  const removeQuestion = (index: number) => {
    if (questions.length === 1) return;
    setQuestions(questions.filter((_, i) => i !== index));
  };

  const updateQuestion = (
    index: number,
    field: keyof QuestionInput,
    value: string
  ) => {
    const updated = [...questions];
    updated[index] = { ...updated[index], [field]: value };
    setQuestions(updated);
  };

  const handleCreate = () => {
    const validQuestions = questions.filter(
      (q) => q.question_text.trim() !== ""
    );
    createQuestionnaire.mutate(
      {
        title: form.title,
        source: form.source || undefined,
        questions: validQuestions.length > 0 ? validQuestions as unknown as Record<string, unknown>[] : undefined,
      },
      {
        onSuccess: () => {
          setShowCreate(false);
          resetForm();
        },
      }
    );
  };

  const questionnaires = data?.items || [];

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold">Questionnaires</h1>
          <p className="text-muted-foreground">
            Manage security questionnaires and auto-fill responses
          </p>
        </div>
        <Button onClick={() => setShowCreate((v) => !v)}>
          <Plus className="mr-2 h-4 w-4" />
          New Questionnaire
        </Button>
      </div>

      {/* Stats */}
      {stats && (
        <div className="grid grid-cols-4 gap-4">
          {[
            { label: "Total", value: stats.total ?? 0 },
            { label: "In Progress", value: stats.in_progress ?? 0 },
            { label: "Completed", value: stats.completed ?? 0 },
            { label: "Submitted", value: stats.submitted ?? 0 },
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

      {showCreate && (
        <Card>
          <CardContent className="p-4 space-y-4">
            <h2 className="text-lg font-semibold">Create New Questionnaire</h2>

            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-1">
                <label className="text-sm font-medium">Title</label>
                <input
                  type="text"
                  required
                  className="w-full rounded-md border bg-background p-2 text-sm"
                  placeholder="Questionnaire title"
                  value={form.title}
                  onChange={(e) =>
                    setForm({ ...form, title: e.target.value })
                  }
                />
              </div>
              <div className="space-y-1">
                <label className="text-sm font-medium">Source</label>
                <input
                  type="text"
                  className="w-full rounded-md border bg-background p-2 text-sm"
                  placeholder="e.g. Customer, Vendor"
                  value={form.source}
                  onChange={(e) =>
                    setForm({ ...form, source: e.target.value })
                  }
                />
              </div>
            </div>

            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <label className="text-sm font-medium">Questions</label>
                <Button
                  type="button"
                  size="sm"
                  variant="outline"
                  onClick={addQuestion}
                >
                  <Plus className="mr-1 h-3 w-3" />
                  Add Question
                </Button>
              </div>
              {questions.map((q, index) => (
                <div
                  key={index}
                  className="flex items-start gap-2 rounded-lg border p-3"
                >
                  <span className="mt-2 text-xs font-mono text-muted-foreground">
                    {index + 1}.
                  </span>
                  <div className="flex-1 space-y-2">
                    <input
                      type="text"
                      className="w-full rounded-md border bg-background p-2 text-sm"
                      placeholder="Enter question..."
                      value={q.question_text}
                      onChange={(e) =>
                        updateQuestion(index, "question_text", e.target.value)
                      }
                    />
                    <select
                      className="w-full rounded-md border bg-background p-2 text-sm"
                      value={q.question_type}
                      onChange={(e) =>
                        updateQuestion(index, "question_type", e.target.value)
                      }
                    >
                      <option value="text">Text</option>
                      <option value="yes_no">Yes/No</option>
                      <option value="multiple_choice">Multiple Choice</option>
                      <option value="file_upload">File Upload</option>
                    </select>
                  </div>
                  {questions.length > 1 && (
                    <Button
                      type="button"
                      size="sm"
                      variant="ghost"
                      onClick={() => removeQuestion(index)}
                      className="mt-1"
                    >
                      <Trash2 className="h-4 w-4 text-muted-foreground" />
                    </Button>
                  )}
                </div>
              ))}
            </div>

            <div className="flex items-center gap-2 pt-2">
              <Button
                onClick={handleCreate}
                disabled={
                  !form.title.trim() || createQuestionnaire.isPending
                }
              >
                {createQuestionnaire.isPending && (
                  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                )}
                Create Questionnaire
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

      {/* Filters */}
      <div className="flex flex-wrap gap-2">
        {STATUS_FILTERS.map((f) => (
          <Button
            key={f.label}
            variant={statusFilter === f.value ? "default" : "outline"}
            size="sm"
            onClick={() => setStatusFilter(f.value)}
          >
            {f.label}
          </Button>
        ))}
      </div>

      {isLoading ? (
        <div className="space-y-3">
          {[1, 2, 3].map((i) => (
            <Skeleton key={i} className="h-28 w-full rounded-xl" />
          ))}
        </div>
      ) : questionnaires.length > 0 ? (
        <div className="space-y-3">
          {questionnaires.map((q: any) => {
            const totalQuestions = q.total_questions ?? 0;
            const answeredQuestions = q.answered_questions ?? 0;
            const progressPct =
              totalQuestions > 0
                ? Math.round(
                    (answeredQuestions / totalQuestions) * 100
                  )
                : 0;

            return (
              <Link key={q.id} href={`/questionnaires/${q.id}`}>
                <Card className="transition-colors hover:bg-accent/50">
                  <CardContent className="p-4 space-y-3">
                    <div className="flex items-center gap-4">
                      <ClipboardList className="h-8 w-8 text-muted-foreground shrink-0" />
                      <div className="flex-1 min-w-0">
                        <div className="font-medium">{q.title}</div>
                        <div className="mt-1 text-xs text-muted-foreground">
                          {q.source && <span>From: {q.source}</span>}
                          {q.created_at && (
                            <>
                              <span> &middot; </span>
                              <span>
                                Created{" "}
                                {new Date(
                                  q.created_at
                                ).toLocaleDateString()}
                              </span>
                            </>
                          )}
                        </div>
                      </div>
                      <Badge
                        className={statusColor[q.status] || ""}
                      >
                        {q.status?.replace(/_/g, " ")}
                      </Badge>
                    </div>
                    {totalQuestions > 0 && (
                      <div className="space-y-1">
                        <div className="flex justify-between text-xs text-muted-foreground">
                          <span>
                            {answeredQuestions} / {totalQuestions} answered
                          </span>
                          <span>{progressPct}%</span>
                        </div>
                        <Progress value={progressPct} />
                      </div>
                    )}
                  </CardContent>
                </Card>
              </Link>
            );
          })}
        </div>
      ) : (
        <Card>
          <CardContent className="flex flex-col items-center justify-center p-12 text-center">
            <ClipboardList className="h-12 w-12 text-muted-foreground mb-4" />
            <h3 className="text-lg font-medium">No questionnaires found</h3>
            <p className="text-sm text-muted-foreground mt-1">
              Create a questionnaire to manage security assessment responses.
            </p>
          </CardContent>
        </Card>
      )}

      {data && data.total_pages > 1 && (
        <div className="flex justify-center gap-2 pt-4">
          <p className="text-sm text-muted-foreground">
            Page {data.page} of {data.total_pages} ({data.total} total)
          </p>
        </div>
      )}
    </div>
  );
}

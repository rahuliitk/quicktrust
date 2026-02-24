"use client";

import { useState } from "react";
import Link from "next/link";
import { useParams, useRouter } from "next/navigation";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Skeleton } from "@/components/ui/skeleton";
import {
  useQuestionnaire,
  useUpdateQuestionnaire,
  useDeleteQuestionnaire,
  useAutoFillQuestionnaire,
} from "@/hooks/use-api";
import {
  ArrowLeft,
  Trash2,
  Loader2,
  Save,
  Sparkles,
  ClipboardList,
  CheckCircle,
  ExternalLink,
} from "lucide-react";
import { useOrgId } from "@/hooks/use-org-id";

const statusColor: Record<string, string> = {
  draft: "bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-100",
  in_progress:
    "bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-100",
  completed:
    "bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-100",
  sent: "bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-100",
};

const confidenceColor: Record<string, string> = {
  high: "bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-100",
  medium:
    "bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-100",
  low: "bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-100",
};

export default function QuestionnaireDetailPage() {
  const orgId = useOrgId();
  const params = useParams();
  const router = useRouter();
  const questionnaireId = params.id as string;

  const { data: questionnaire, isLoading } = useQuestionnaire(
    orgId,
    questionnaireId
  );
  const updateQuestionnaire = useUpdateQuestionnaire(orgId);
  const deleteQuestionnaire = useDeleteQuestionnaire(orgId);
  const autoFill = useAutoFillQuestionnaire(orgId);

  // Track answer edits by question index
  const [editedAnswers, setEditedAnswers] = useState<Record<number, string>>(
    {}
  );
  const [approvedResponses, setApprovedResponses] = useState<
    Record<number, boolean>
  >({});

  function handleAutoFill() {
    autoFill.mutate(questionnaireId);
  }

  function handleDelete() {
    if (!questionnaire) return;
    const confirmed = window.confirm(
      `Are you sure you want to delete "${questionnaire.title}"? This action cannot be undone.`
    );
    if (!confirmed) return;
    deleteQuestionnaire.mutate(questionnaire.id, {
      onSuccess: () => router.push("/questionnaires"),
    });
  }

  function handleSaveAnswer(questionIndex: number) {
    if (!questionnaire) return;
    const questions = [...(questionnaire.questions || [])];
    if (questions[questionIndex]) {
      questions[questionIndex] = {
        ...questions[questionIndex],
        answer: editedAnswers[questionIndex],
        is_approved: approvedResponses[questionIndex] ?? questions[questionIndex].is_approved,
      };
    }
    updateQuestionnaire.mutate({
      questionnaireId: questionnaire.id,
      questions,
    });
  }

  function toggleApproval(index: number) {
    setApprovedResponses((prev) => ({
      ...prev,
      [index]: !prev[index],
    }));
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

  if (!questionnaire) return <p>Questionnaire not found.</p>;

  const questions = questionnaire.questions || [];

  return (
    <div className="space-y-6">
      <Link
        href="/questionnaires"
        className="inline-flex items-center gap-1 text-sm text-muted-foreground hover:text-foreground transition-colors"
      >
        <ArrowLeft className="h-4 w-4" />
        Back to Questionnaires
      </Link>

      {/* Header */}
      <div className="flex items-center gap-3">
        <h1 className="text-3xl font-bold">{questionnaire.title}</h1>
        <Badge className={statusColor[questionnaire.status] || ""}>
          {questionnaire.status?.replace(/_/g, " ")}
        </Badge>
        {questionnaire.source && (
          <Badge variant="outline">From: {questionnaire.source}</Badge>
        )}
        <div className="ml-auto flex items-center gap-2">
          <Button
            variant="default"
            size="sm"
            onClick={handleAutoFill}
            disabled={autoFill.isPending}
            className="gap-1.5"
          >
            {autoFill.isPending ? (
              <Loader2 className="h-4 w-4 animate-spin" />
            ) : (
              <Sparkles className="h-4 w-4" />
            )}
            Auto-Fill
          </Button>
          <Button
            variant="destructive"
            size="sm"
            onClick={handleDelete}
            disabled={deleteQuestionnaire.isPending}
          >
            {deleteQuestionnaire.isPending ? (
              <Loader2 className="mr-1 h-4 w-4 animate-spin" />
            ) : (
              <Trash2 className="mr-1 h-4 w-4" />
            )}
            Delete
          </Button>
        </div>
      </div>

      {/* Questions */}
      <div className="space-y-4">
        {questions.length > 0 ? (
          questions.map((q: any, index: number) => {
            const currentAnswer =
              index in editedAnswers
                ? editedAnswers[index]
                : q.answer || "";
            const isApproved =
              index in approvedResponses
                ? approvedResponses[index]
                : q.is_approved || false;

            return (
              <Card key={q.id || index}>
                <CardHeader>
                  <div className="flex items-start justify-between">
                    <CardTitle className="text-base">
                      {index + 1}. {q.question_text}
                    </CardTitle>
                    <div className="flex items-center gap-2 shrink-0">
                      {q.confidence && (
                        <Badge
                          className={
                            confidenceColor[q.confidence] || ""
                          }
                        >
                          {q.confidence} confidence
                        </Badge>
                      )}
                      <Badge variant="outline" className="capitalize">
                        {q.question_type?.replace(/_/g, " ")}
                      </Badge>
                    </div>
                  </div>
                </CardHeader>
                <CardContent className="space-y-3">
                  <textarea
                    className="w-full rounded-md border bg-background p-2 text-sm"
                    rows={3}
                    placeholder="Enter your answer..."
                    value={currentAnswer}
                    onChange={(e) =>
                      setEditedAnswers((prev) => ({
                        ...prev,
                        [index]: e.target.value,
                      }))
                    }
                  />

                  {q.source_link && (
                    <div className="flex items-center gap-1 text-xs text-muted-foreground">
                      <ExternalLink className="h-3 w-3" />
                      <a
                        href={q.source_link}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="hover:underline"
                      >
                        {q.source_link}
                      </a>
                    </div>
                  )}

                  <div className="flex items-center justify-between">
                    <label className="flex items-center gap-2 text-sm">
                      <input
                        type="checkbox"
                        checked={isApproved}
                        onChange={() => toggleApproval(index)}
                        className="h-4 w-4 rounded border"
                      />
                      <CheckCircle
                        className={`h-4 w-4 ${
                          isApproved
                            ? "text-green-500"
                            : "text-muted-foreground"
                        }`}
                      />
                      Approve this response
                    </label>

                    <Button
                      size="sm"
                      variant="outline"
                      onClick={() => handleSaveAnswer(index)}
                      disabled={updateQuestionnaire.isPending}
                    >
                      {updateQuestionnaire.isPending ? (
                        <Loader2 className="mr-1 h-3 w-3 animate-spin" />
                      ) : (
                        <Save className="mr-1 h-3 w-3" />
                      )}
                      Save
                    </Button>
                  </div>
                </CardContent>
              </Card>
            );
          })
        ) : (
          <Card>
            <CardContent className="flex flex-col items-center justify-center p-12 text-center">
              <ClipboardList className="h-12 w-12 text-muted-foreground mb-4" />
              <h3 className="text-lg font-medium">No questions yet</h3>
              <p className="text-sm text-muted-foreground mt-1">
                This questionnaire has no questions. Use Auto-Fill to generate
                responses or edit the questionnaire to add questions.
              </p>
            </CardContent>
          </Card>
        )}
      </div>
    </div>
  );
}

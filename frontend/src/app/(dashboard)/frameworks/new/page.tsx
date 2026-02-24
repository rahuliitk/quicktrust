"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
  CardDescription,
} from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import {
  useCreateFramework,
  useAddFrameworkDomain,
  useAddDomainRequirement,
} from "@/hooks/use-api";
import { Shield, Plus, Trash2, ArrowLeft, ArrowRight, Check, Loader2 } from "lucide-react";

// ---------- Types ----------
interface DomainDraft {
  code: string;
  name: string;
  description: string;
}

interface RequirementDraft {
  code: string;
  title: string;
  description: string;
}

// ---------- Component ----------
export default function NewFrameworkPage() {
  const router = useRouter();

  // --- Step state ---
  const [step, setStep] = useState(1);

  // --- Step 1: framework metadata ---
  const [frameworkName, setFrameworkName] = useState("");
  const [frameworkVersion, setFrameworkVersion] = useState("");
  const [frameworkCategory, setFrameworkCategory] = useState("");
  const [frameworkDescription, setFrameworkDescription] = useState("");

  // --- Step 2: domains ---
  const [domains, setDomains] = useState<DomainDraft[]>([
    { code: "", name: "", description: "" },
  ]);

  // --- Step 3: requirements per domain ---
  const [requirementsByDomain, setRequirementsByDomain] = useState<
    Record<number, RequirementDraft[]>
  >({ 0: [{ code: "", title: "", description: "" }] });

  // --- Submission state ---
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submitError, setSubmitError] = useState<string | null>(null);

  // --- Mutations ---
  const createFramework = useCreateFramework();
  const addDomain = useAddFrameworkDomain();
  const addRequirement = useAddDomainRequirement();

  // ---------- Domain helpers ----------
  function addDomainRow() {
    const idx = domains.length;
    setDomains([...domains, { code: "", name: "", description: "" }]);
    setRequirementsByDomain((prev) => ({
      ...prev,
      [idx]: [{ code: "", title: "", description: "" }],
    }));
  }

  function removeDomainRow(idx: number) {
    if (domains.length <= 1) return;
    const next = domains.filter((_, i) => i !== idx);
    setDomains(next);

    // Rebuild requirements map with new indices
    const newReqs: Record<number, RequirementDraft[]> = {};
    let newIdx = 0;
    for (let i = 0; i < domains.length; i++) {
      if (i === idx) continue;
      newReqs[newIdx] = requirementsByDomain[i] || [
        { code: "", title: "", description: "" },
      ];
      newIdx++;
    }
    setRequirementsByDomain(newReqs);
  }

  function updateDomain(idx: number, field: keyof DomainDraft, value: string) {
    const next = [...domains];
    next[idx] = { ...next[idx], [field]: value };
    setDomains(next);
  }

  // ---------- Requirement helpers ----------
  function addRequirementRow(domainIdx: number) {
    setRequirementsByDomain((prev) => ({
      ...prev,
      [domainIdx]: [
        ...(prev[domainIdx] || []),
        { code: "", title: "", description: "" },
      ],
    }));
  }

  function removeRequirementRow(domainIdx: number, reqIdx: number) {
    setRequirementsByDomain((prev) => {
      const list = prev[domainIdx] || [];
      if (list.length <= 1) return prev;
      return {
        ...prev,
        [domainIdx]: list.filter((_, i) => i !== reqIdx),
      };
    });
  }

  function updateRequirement(
    domainIdx: number,
    reqIdx: number,
    field: keyof RequirementDraft,
    value: string
  ) {
    setRequirementsByDomain((prev) => {
      const list = [...(prev[domainIdx] || [])];
      list[reqIdx] = { ...list[reqIdx], [field]: value };
      return { ...prev, [domainIdx]: list };
    });
  }

  // ---------- Validation ----------
  function canProceedStep1() {
    return frameworkName.trim() !== "" && frameworkVersion.trim() !== "";
  }

  function canProceedStep2() {
    return domains.every((d) => d.code.trim() !== "" && d.name.trim() !== "");
  }

  function canSubmit() {
    return Object.entries(requirementsByDomain).every(([, reqs]) =>
      reqs.every((r) => r.code.trim() !== "" && r.title.trim() !== "")
    );
  }

  // ---------- Submit ----------
  async function handleSubmit() {
    setIsSubmitting(true);
    setSubmitError(null);

    try {
      // 1. Create framework
      const framework = await createFramework.mutateAsync({
        name: frameworkName.trim(),
        version: frameworkVersion.trim(),
        category: frameworkCategory.trim() || undefined,
        description: frameworkDescription.trim() || undefined,
      });

      // 2. Create domains sequentially, collect returned IDs
      const domainIds: string[] = [];
      for (const domain of domains) {
        const created = await addDomain.mutateAsync({
          frameworkId: framework.id,
          code: domain.code.trim(),
          name: domain.name.trim(),
          description: domain.description.trim() || undefined,
        });
        domainIds.push((created as { id: string }).id);
      }

      // 3. Create requirements for each domain sequentially
      for (let dIdx = 0; dIdx < domains.length; dIdx++) {
        const reqs = requirementsByDomain[dIdx] || [];
        for (const req of reqs) {
          await addRequirement.mutateAsync({
            frameworkId: framework.id,
            domainId: domainIds[dIdx],
            code: req.code.trim(),
            title: req.title.trim(),
            description: req.description.trim() || undefined,
          });
        }
      }

      // 4. Redirect
      router.push("/frameworks");
    } catch (err: unknown) {
      const message =
        err instanceof Error ? err.message : "An unexpected error occurred";
      setSubmitError(message);
    } finally {
      setIsSubmitting(false);
    }
  }

  // ---------- Render ----------
  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center gap-4">
        <Button variant="ghost" size="sm" onClick={() => router.push("/frameworks")}>
          <ArrowLeft className="h-4 w-4 mr-1" />
          Back
        </Button>
        <div>
          <h1 className="text-3xl font-bold">Create Custom Framework</h1>
          <p className="text-muted-foreground">
            Build a compliance framework in three steps
          </p>
        </div>
      </div>

      {/* Step indicator */}
      <div className="flex items-center gap-2">
        {[1, 2, 3].map((s) => (
          <div key={s} className="flex items-center gap-2">
            <Badge
              variant={step === s ? "default" : step > s ? "success" : "secondary"}
              className="h-8 w-8 flex items-center justify-center rounded-full"
            >
              {step > s ? <Check className="h-4 w-4" /> : s}
            </Badge>
            <span
              className={`text-sm font-medium ${
                step === s ? "text-foreground" : "text-muted-foreground"
              }`}
            >
              {s === 1 ? "Metadata" : s === 2 ? "Domains" : "Requirements"}
            </span>
            {s < 3 && <div className="w-8 h-px bg-border" />}
          </div>
        ))}
      </div>

      {/* ===================== Step 1: Metadata ===================== */}
      {step === 1 && (
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Shield className="h-5 w-5" />
              Framework Metadata
            </CardTitle>
            <CardDescription>
              Define the basic information for your compliance framework.
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-1">
                <label className="text-sm font-medium">
                  Name <span className="text-destructive">*</span>
                </label>
                <input
                  type="text"
                  required
                  className="w-full rounded-md border bg-background p-2 text-sm"
                  placeholder="e.g. Custom SOC 2 Type II"
                  value={frameworkName}
                  onChange={(e) => setFrameworkName(e.target.value)}
                />
              </div>
              <div className="space-y-1">
                <label className="text-sm font-medium">
                  Version <span className="text-destructive">*</span>
                </label>
                <input
                  type="text"
                  required
                  className="w-full rounded-md border bg-background p-2 text-sm"
                  placeholder="e.g. 1.0"
                  value={frameworkVersion}
                  onChange={(e) => setFrameworkVersion(e.target.value)}
                />
              </div>
            </div>

            <div className="space-y-1">
              <label className="text-sm font-medium">Category</label>
              <input
                type="text"
                className="w-full rounded-md border bg-background p-2 text-sm"
                placeholder="e.g. Security, Privacy, Governance"
                value={frameworkCategory}
                onChange={(e) => setFrameworkCategory(e.target.value)}
              />
            </div>

            <div className="space-y-1">
              <label className="text-sm font-medium">Description</label>
              <textarea
                className="w-full rounded-md border bg-background p-2 text-sm min-h-[80px]"
                placeholder="A brief description of this framework..."
                value={frameworkDescription}
                onChange={(e) => setFrameworkDescription(e.target.value)}
              />
            </div>

            <div className="flex justify-end">
              <Button disabled={!canProceedStep1()} onClick={() => setStep(2)}>
                Next: Add Domains
                <ArrowRight className="h-4 w-4 ml-1" />
              </Button>
            </div>
          </CardContent>
        </Card>
      )}

      {/* ===================== Step 2: Domains ===================== */}
      {step === 2 && (
        <Card>
          <CardHeader>
            <CardTitle>Domains</CardTitle>
            <CardDescription>
              Add control domains to organise requirements. Each domain gets a code
              (e.g. &quot;CC1&quot;) and a name.
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            {domains.map((domain, idx) => (
              <div
                key={idx}
                className="flex items-start gap-3 rounded-lg border p-4"
              >
                <Badge variant="outline" className="mt-1 shrink-0">
                  {idx + 1}
                </Badge>
                <div className="flex-1 grid grid-cols-3 gap-3">
                  <div className="space-y-1">
                    <label className="text-sm font-medium">
                      Code <span className="text-destructive">*</span>
                    </label>
                    <input
                      type="text"
                      className="w-full rounded-md border bg-background p-2 text-sm"
                      placeholder="e.g. CC1"
                      value={domain.code}
                      onChange={(e) => updateDomain(idx, "code", e.target.value)}
                    />
                  </div>
                  <div className="space-y-1">
                    <label className="text-sm font-medium">
                      Name <span className="text-destructive">*</span>
                    </label>
                    <input
                      type="text"
                      className="w-full rounded-md border bg-background p-2 text-sm"
                      placeholder="e.g. Control Environment"
                      value={domain.name}
                      onChange={(e) => updateDomain(idx, "name", e.target.value)}
                    />
                  </div>
                  <div className="space-y-1">
                    <label className="text-sm font-medium">Description</label>
                    <input
                      type="text"
                      className="w-full rounded-md border bg-background p-2 text-sm"
                      placeholder="Optional description"
                      value={domain.description}
                      onChange={(e) =>
                        updateDomain(idx, "description", e.target.value)
                      }
                    />
                  </div>
                </div>
                <Button
                  variant="ghost"
                  size="sm"
                  className="mt-6 text-destructive"
                  disabled={domains.length <= 1}
                  onClick={() => removeDomainRow(idx)}
                >
                  <Trash2 className="h-4 w-4" />
                </Button>
              </div>
            ))}

            <Button variant="outline" onClick={addDomainRow}>
              <Plus className="h-4 w-4 mr-1" />
              Add Domain
            </Button>

            <div className="flex justify-between pt-4 border-t">
              <Button variant="ghost" onClick={() => setStep(1)}>
                <ArrowLeft className="h-4 w-4 mr-1" />
                Back
              </Button>
              <Button disabled={!canProceedStep2()} onClick={() => setStep(3)}>
                Next: Add Requirements
                <ArrowRight className="h-4 w-4 ml-1" />
              </Button>
            </div>
          </CardContent>
        </Card>
      )}

      {/* ===================== Step 3: Requirements ===================== */}
      {step === 3 && (
        <div className="space-y-6">
          {domains.map((domain, dIdx) => (
            <Card key={dIdx}>
              <CardHeader>
                <CardTitle className="text-lg">
                  <Badge variant="outline" className="mr-2">
                    {domain.code}
                  </Badge>
                  {domain.name}
                </CardTitle>
                <CardDescription>
                  Add requirements for this domain.
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-3">
                {(requirementsByDomain[dIdx] || []).map((req, rIdx) => (
                  <div
                    key={rIdx}
                    className="flex items-start gap-3 rounded-lg border p-3"
                  >
                    <Badge variant="secondary" className="mt-1 shrink-0 text-xs">
                      {rIdx + 1}
                    </Badge>
                    <div className="flex-1 grid grid-cols-3 gap-3">
                      <div className="space-y-1">
                        <label className="text-sm font-medium">
                          Code <span className="text-destructive">*</span>
                        </label>
                        <input
                          type="text"
                          className="w-full rounded-md border bg-background p-2 text-sm"
                          placeholder="e.g. CC1.1"
                          value={req.code}
                          onChange={(e) =>
                            updateRequirement(dIdx, rIdx, "code", e.target.value)
                          }
                        />
                      </div>
                      <div className="space-y-1">
                        <label className="text-sm font-medium">
                          Title <span className="text-destructive">*</span>
                        </label>
                        <input
                          type="text"
                          className="w-full rounded-md border bg-background p-2 text-sm"
                          placeholder="Requirement title"
                          value={req.title}
                          onChange={(e) =>
                            updateRequirement(dIdx, rIdx, "title", e.target.value)
                          }
                        />
                      </div>
                      <div className="space-y-1">
                        <label className="text-sm font-medium">Description</label>
                        <input
                          type="text"
                          className="w-full rounded-md border bg-background p-2 text-sm"
                          placeholder="Optional"
                          value={req.description}
                          onChange={(e) =>
                            updateRequirement(
                              dIdx,
                              rIdx,
                              "description",
                              e.target.value
                            )
                          }
                        />
                      </div>
                    </div>
                    <Button
                      variant="ghost"
                      size="sm"
                      className="mt-6 text-destructive"
                      disabled={
                        (requirementsByDomain[dIdx] || []).length <= 1
                      }
                      onClick={() => removeRequirementRow(dIdx, rIdx)}
                    >
                      <Trash2 className="h-4 w-4" />
                    </Button>
                  </div>
                ))}
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => addRequirementRow(dIdx)}
                >
                  <Plus className="h-4 w-4 mr-1" />
                  Add Requirement
                </Button>
              </CardContent>
            </Card>
          ))}

          {submitError && (
            <Card className="border-destructive">
              <CardContent className="p-4 text-sm text-destructive">
                {submitError}
              </CardContent>
            </Card>
          )}

          <div className="flex justify-between">
            <Button variant="ghost" onClick={() => setStep(2)}>
              <ArrowLeft className="h-4 w-4 mr-1" />
              Back
            </Button>
            <Button
              disabled={!canSubmit() || isSubmitting}
              onClick={handleSubmit}
            >
              {isSubmitting ? (
                <>
                  <Loader2 className="h-4 w-4 mr-1 animate-spin" />
                  Creating Framework...
                </>
              ) : (
                <>
                  <Check className="h-4 w-4 mr-1" />
                  Create Framework
                </>
              )}
            </Button>
          </div>
        </div>
      )}
    </div>
  );
}

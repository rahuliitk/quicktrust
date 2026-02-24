"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
  CardDescription,
} from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Skeleton } from "@/components/ui/skeleton";
import { useFrameworks, useStartOnboarding } from "@/hooks/use-api";
import {
  Building2,
  Cpu,
  Shield,
  ClipboardCheck,
  ChevronRight,
  ChevronLeft,
  Rocket,
  Loader2,
  CheckCircle,
} from "lucide-react";
import type { OnboardingSession } from "@/lib/types";
import { useOrgId } from "@/hooks/use-org-id";

const STEPS = [
  { number: 1, title: "Company Info", icon: Building2 },
  { number: 2, title: "Tech Stack", icon: Cpu },
  { number: 3, title: "Frameworks", icon: Shield },
  { number: 4, title: "Review & Launch", icon: ClipboardCheck },
];

const INDUSTRIES = [
  "Technology",
  "Healthcare",
  "Finance",
  "Retail",
  "Manufacturing",
  "Education",
  "Government",
  "Other",
];

const COMPANY_SIZES = ["1-10", "11-50", "51-200", "201-1000", "1001+"];

const CLOUD_PROVIDERS = ["AWS", "Azure", "GCP", "None"];

const TECH_STACK_OPTIONS = [
  "Node.js",
  "Python",
  "Java",
  "Go",
  "React",
  "Next.js",
  "PostgreSQL",
  "MongoDB",
  "Redis",
  "Docker",
  "Kubernetes",
];

const DEPARTMENTS = [
  "Engineering",
  "Security",
  "Compliance",
  "HR",
  "Finance",
  "Legal",
  "Operations",
];

const TIMELINE_OPTIONS = [
  { label: "30 days", value: "30_days" },
  { label: "60 days", value: "60_days" },
  { label: "90 days", value: "90_days" },
  { label: "6 months", value: "6_months" },
];

interface WizardFormState {
  company_name: string;
  industry: string;
  company_size: string;
  cloud_providers: string[];
  tech_stack: string[];
  departments: string[];
  target_framework_ids: string[];
  compliance_timeline: string;
  special_requirements: string;
}

export default function OnboardingPage() {
  const orgId = useOrgId();
  const router = useRouter();
  const [currentStep, setCurrentStep] = useState(1);
  const [submitError, setSubmitError] = useState<string | null>(null);

  const [form, setForm] = useState<WizardFormState>({
    company_name: "",
    industry: "",
    company_size: "",
    cloud_providers: [],
    tech_stack: [],
    departments: [],
    target_framework_ids: [],
    compliance_timeline: "90_days",
    special_requirements: "",
  });

  const { data: frameworks, isLoading: frameworksLoading } = useFrameworks();
  const startOnboarding = useStartOnboarding(orgId);

  function toggleMultiSelect(
    field: "cloud_providers" | "tech_stack" | "departments" | "target_framework_ids",
    value: string
  ) {
    setForm((prev) => {
      const current = prev[field];
      const next = current.includes(value)
        ? current.filter((v) => v !== value)
        : [...current, value];
      return { ...prev, [field]: next };
    });
  }

  function canProceed(): boolean {
    switch (currentStep) {
      case 1:
        return (
          form.company_name.trim().length > 0 &&
          form.industry.length > 0 &&
          form.company_size.length > 0
        );
      case 2:
        return (
          form.cloud_providers.length > 0 &&
          form.tech_stack.length > 0 &&
          form.departments.length > 0
        );
      case 3:
        return form.target_framework_ids.length > 0;
      case 4:
        return true;
      default:
        return false;
    }
  }

  function handleNext() {
    if (currentStep < 4 && canProceed()) {
      setCurrentStep((s) => s + 1);
    }
  }

  function handleBack() {
    if (currentStep > 1) {
      setCurrentStep((s) => s - 1);
    }
  }

  function handleLaunch() {
    setSubmitError(null);
    startOnboarding.mutate(
      {
        company_name: form.company_name,
        industry: form.industry,
        company_size: form.company_size,
        cloud_providers: form.cloud_providers,
        tech_stack: form.tech_stack,
        departments: form.departments,
        target_framework_ids: form.target_framework_ids,
        compliance_timeline: form.compliance_timeline,
        special_requirements: form.special_requirements || undefined,
      },
      {
        onSuccess: (data: OnboardingSession) => {
          router.push(`/onboarding/progress?session=${data.id}`);
        },
        onError: (error: Error) => {
          setSubmitError(error.message || "Failed to start onboarding. Please try again.");
        },
      }
    );
  }

  function getFrameworkName(id: string): string {
    const fw = frameworks?.find((f) => f.id === id);
    return fw ? `${fw.name} (v${fw.version})` : id;
  }

  return (
    <div className="mx-auto max-w-3xl space-y-6">
      {/* Header */}
      <div className="text-center">
        <h1 className="text-3xl font-bold">Quick Start</h1>
        <p className="text-muted-foreground mt-1">
          Set up your compliance program in minutes
        </p>
      </div>

      {/* Step Indicator */}
      <div className="flex items-center justify-center gap-1">
        {STEPS.map((step, idx) => {
          const StepIcon = step.icon;
          const isActive = currentStep === step.number;
          const isCompleted = currentStep > step.number;

          return (
            <div key={step.number} className="flex items-center">
              <div
                className={`flex items-center gap-2 rounded-lg px-3 py-2 text-sm font-medium transition-colors ${
                  isActive
                    ? "bg-primary text-primary-foreground"
                    : isCompleted
                    ? "bg-primary/10 text-primary"
                    : "bg-muted text-muted-foreground"
                }`}
              >
                {isCompleted ? (
                  <CheckCircle className="h-4 w-4" />
                ) : (
                  <StepIcon className="h-4 w-4" />
                )}
                <span className="hidden sm:inline">{step.title}</span>
                <span className="sm:hidden">{step.number}</span>
              </div>
              {idx < STEPS.length - 1 && (
                <ChevronRight className="mx-1 h-4 w-4 text-muted-foreground" />
              )}
            </div>
          );
        })}
      </div>

      {/* Step Content */}
      <Card>
        <CardHeader>
          <CardTitle>
            {STEPS[currentStep - 1].title}
          </CardTitle>
          <CardDescription>
            {currentStep === 1 && "Tell us about your organization"}
            {currentStep === 2 && "Select your technology infrastructure and departments"}
            {currentStep === 3 && "Choose the compliance frameworks you want to target"}
            {currentStep === 4 && "Review your selections and launch the setup"}
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-6">
          {/* Step 1: Company Info */}
          {currentStep === 1 && (
            <>
              <div>
                <label className="text-sm font-medium">
                  Company Name <span className="text-red-500">*</span>
                </label>
                <input
                  type="text"
                  className="mt-1 w-full rounded-md border bg-background p-2 text-sm"
                  placeholder="Enter your company name"
                  value={form.company_name}
                  onChange={(e) =>
                    setForm({ ...form, company_name: e.target.value })
                  }
                />
              </div>

              <div>
                <label className="text-sm font-medium">
                  Industry <span className="text-red-500">*</span>
                </label>
                <select
                  className="mt-1 w-full rounded-md border bg-background p-2 text-sm"
                  value={form.industry}
                  onChange={(e) =>
                    setForm({ ...form, industry: e.target.value })
                  }
                >
                  <option value="">Select an industry...</option>
                  {INDUSTRIES.map((ind) => (
                    <option key={ind} value={ind}>
                      {ind}
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label className="text-sm font-medium">
                  Company Size <span className="text-red-500">*</span>
                </label>
                <select
                  className="mt-1 w-full rounded-md border bg-background p-2 text-sm"
                  value={form.company_size}
                  onChange={(e) =>
                    setForm({ ...form, company_size: e.target.value })
                  }
                >
                  <option value="">Select company size...</option>
                  {COMPANY_SIZES.map((size) => (
                    <option key={size} value={size}>
                      {size} employees
                    </option>
                  ))}
                </select>
              </div>
            </>
          )}

          {/* Step 2: Tech Stack */}
          {currentStep === 2 && (
            <>
              <div>
                <label className="text-sm font-medium">
                  Cloud Providers <span className="text-red-500">*</span>
                </label>
                <p className="text-xs text-muted-foreground mb-2">
                  Select all that apply
                </p>
                <div className="grid grid-cols-2 gap-2 sm:grid-cols-4">
                  {CLOUD_PROVIDERS.map((provider) => (
                    <label
                      key={provider}
                      className={`flex cursor-pointer items-center gap-2 rounded-lg border p-3 text-sm transition-colors ${
                        form.cloud_providers.includes(provider)
                          ? "border-primary bg-primary/5 ring-1 ring-primary"
                          : "hover:bg-accent/50"
                      }`}
                    >
                      <input
                        type="checkbox"
                        className="h-4 w-4"
                        checked={form.cloud_providers.includes(provider)}
                        onChange={() =>
                          toggleMultiSelect("cloud_providers", provider)
                        }
                      />
                      {provider}
                    </label>
                  ))}
                </div>
              </div>

              <div>
                <label className="text-sm font-medium">
                  Tech Stack <span className="text-red-500">*</span>
                </label>
                <p className="text-xs text-muted-foreground mb-2">
                  Select all technologies you use
                </p>
                <div className="grid grid-cols-2 gap-2 sm:grid-cols-3">
                  {TECH_STACK_OPTIONS.map((tech) => (
                    <label
                      key={tech}
                      className={`flex cursor-pointer items-center gap-2 rounded-lg border p-3 text-sm transition-colors ${
                        form.tech_stack.includes(tech)
                          ? "border-primary bg-primary/5 ring-1 ring-primary"
                          : "hover:bg-accent/50"
                      }`}
                    >
                      <input
                        type="checkbox"
                        className="h-4 w-4"
                        checked={form.tech_stack.includes(tech)}
                        onChange={() => toggleMultiSelect("tech_stack", tech)}
                      />
                      {tech}
                    </label>
                  ))}
                </div>
              </div>

              <div>
                <label className="text-sm font-medium">
                  Departments <span className="text-red-500">*</span>
                </label>
                <p className="text-xs text-muted-foreground mb-2">
                  Select departments involved in compliance
                </p>
                <div className="grid grid-cols-2 gap-2 sm:grid-cols-3">
                  {DEPARTMENTS.map((dept) => (
                    <label
                      key={dept}
                      className={`flex cursor-pointer items-center gap-2 rounded-lg border p-3 text-sm transition-colors ${
                        form.departments.includes(dept)
                          ? "border-primary bg-primary/5 ring-1 ring-primary"
                          : "hover:bg-accent/50"
                      }`}
                    >
                      <input
                        type="checkbox"
                        className="h-4 w-4"
                        checked={form.departments.includes(dept)}
                        onChange={() => toggleMultiSelect("departments", dept)}
                      />
                      {dept}
                    </label>
                  ))}
                </div>
              </div>
            </>
          )}

          {/* Step 3: Frameworks */}
          {currentStep === 3 && (
            <div>
              <label className="text-sm font-medium">
                Target Frameworks <span className="text-red-500">*</span>
              </label>
              <p className="text-xs text-muted-foreground mb-3">
                Select the compliance frameworks you want to implement
              </p>

              {frameworksLoading ? (
                <div className="grid gap-3 md:grid-cols-2">
                  {[1, 2, 3].map((i) => (
                    <Skeleton key={i} className="h-32 w-full rounded-xl" />
                  ))}
                </div>
              ) : frameworks && frameworks.length > 0 ? (
                <div className="grid gap-3 md:grid-cols-2">
                  {frameworks.map((fw) => {
                    const isSelected = form.target_framework_ids.includes(
                      fw.id
                    );
                    return (
                      <div
                        key={fw.id}
                        onClick={() =>
                          toggleMultiSelect("target_framework_ids", fw.id)
                        }
                        className={`cursor-pointer rounded-xl border p-4 transition-all ${
                          isSelected
                            ? "border-primary bg-primary/5 ring-2 ring-primary shadow-sm"
                            : "hover:border-primary/50 hover:shadow-sm"
                        }`}
                      >
                        <div className="flex items-start justify-between">
                          <div className="flex-1">
                            <div className="flex items-center gap-2">
                              <Shield className="h-5 w-5 text-primary" />
                              <span className="font-medium">{fw.name}</span>
                            </div>
                            <Badge
                              variant="outline"
                              className="mt-1 text-xs"
                            >
                              v{fw.version}
                            </Badge>
                          </div>
                          <div
                            className={`flex h-5 w-5 items-center justify-center rounded-full border-2 transition-colors ${
                              isSelected
                                ? "border-primary bg-primary text-primary-foreground"
                                : "border-muted-foreground/30"
                            }`}
                          >
                            {isSelected && (
                              <CheckCircle className="h-3 w-3" />
                            )}
                          </div>
                        </div>
                        {fw.description && (
                          <p className="mt-2 text-xs text-muted-foreground line-clamp-2">
                            {fw.description}
                          </p>
                        )}
                        {fw.category && (
                          <Badge variant="secondary" className="mt-2 text-xs">
                            {fw.category}
                          </Badge>
                        )}
                      </div>
                    );
                  })}
                </div>
              ) : (
                <Card>
                  <CardContent className="flex flex-col items-center justify-center p-8 text-center">
                    <Shield className="h-10 w-10 text-muted-foreground mb-3" />
                    <p className="text-sm text-muted-foreground">
                      No frameworks available. Please seed the database first.
                    </p>
                  </CardContent>
                </Card>
              )}

              {form.target_framework_ids.length > 0 && (
                <div className="mt-3 flex items-center gap-2">
                  <Badge variant="default">
                    {form.target_framework_ids.length} selected
                  </Badge>
                </div>
              )}
            </div>
          )}

          {/* Step 4: Review & Launch */}
          {currentStep === 4 && (
            <>
              {/* Summary */}
              <div className="space-y-4">
                <div className="rounded-lg border p-4 space-y-3">
                  <h3 className="text-sm font-semibold text-muted-foreground uppercase tracking-wider">
                    Company Information
                  </h3>
                  <div className="grid grid-cols-2 gap-3 text-sm">
                    <div>
                      <span className="text-muted-foreground">Name:</span>{" "}
                      <span className="font-medium">{form.company_name}</span>
                    </div>
                    <div>
                      <span className="text-muted-foreground">Industry:</span>{" "}
                      <span className="font-medium">{form.industry}</span>
                    </div>
                    <div>
                      <span className="text-muted-foreground">Size:</span>{" "}
                      <span className="font-medium">
                        {form.company_size} employees
                      </span>
                    </div>
                  </div>
                </div>

                <div className="rounded-lg border p-4 space-y-3">
                  <h3 className="text-sm font-semibold text-muted-foreground uppercase tracking-wider">
                    Technology & Teams
                  </h3>
                  <div className="space-y-2 text-sm">
                    <div>
                      <span className="text-muted-foreground">
                        Cloud Providers:
                      </span>
                      <div className="mt-1 flex flex-wrap gap-1">
                        {form.cloud_providers.map((p) => (
                          <Badge key={p} variant="secondary">
                            {p}
                          </Badge>
                        ))}
                      </div>
                    </div>
                    <div>
                      <span className="text-muted-foreground">
                        Tech Stack:
                      </span>
                      <div className="mt-1 flex flex-wrap gap-1">
                        {form.tech_stack.map((t) => (
                          <Badge key={t} variant="secondary">
                            {t}
                          </Badge>
                        ))}
                      </div>
                    </div>
                    <div>
                      <span className="text-muted-foreground">
                        Departments:
                      </span>
                      <div className="mt-1 flex flex-wrap gap-1">
                        {form.departments.map((d) => (
                          <Badge key={d} variant="secondary">
                            {d}
                          </Badge>
                        ))}
                      </div>
                    </div>
                  </div>
                </div>

                <div className="rounded-lg border p-4 space-y-3">
                  <h3 className="text-sm font-semibold text-muted-foreground uppercase tracking-wider">
                    Target Frameworks
                  </h3>
                  <div className="flex flex-wrap gap-1">
                    {form.target_framework_ids.map((id) => (
                      <Badge key={id} variant="default">
                        {getFrameworkName(id)}
                      </Badge>
                    ))}
                  </div>
                </div>
              </div>

              {/* Compliance Timeline */}
              <div>
                <label className="text-sm font-medium">
                  Compliance Timeline
                </label>
                <select
                  className="mt-1 w-full rounded-md border bg-background p-2 text-sm"
                  value={form.compliance_timeline}
                  onChange={(e) =>
                    setForm({
                      ...form,
                      compliance_timeline: e.target.value,
                    })
                  }
                >
                  {TIMELINE_OPTIONS.map((opt) => (
                    <option key={opt.value} value={opt.value}>
                      {opt.label}
                    </option>
                  ))}
                </select>
              </div>

              {/* Special Requirements */}
              <div>
                <label className="text-sm font-medium">
                  Special Requirements{" "}
                  <span className="text-muted-foreground font-normal">
                    (optional)
                  </span>
                </label>
                <textarea
                  className="mt-1 w-full rounded-md border bg-background p-2 text-sm min-h-[80px] resize-y"
                  placeholder="Any specific compliance requirements, regulatory constraints, or notes..."
                  value={form.special_requirements}
                  onChange={(e) =>
                    setForm({
                      ...form,
                      special_requirements: e.target.value,
                    })
                  }
                />
              </div>

              {/* Error Message */}
              {submitError && (
                <div className="rounded-lg border border-red-200 bg-red-50 p-3 text-sm text-red-800 dark:border-red-800 dark:bg-red-950 dark:text-red-200">
                  {submitError}
                </div>
              )}
            </>
          )}
        </CardContent>
      </Card>

      {/* Navigation Buttons */}
      <div className="flex items-center justify-between">
        <div>
          {currentStep > 1 ? (
            <Button variant="outline" onClick={handleBack}>
              <ChevronLeft className="mr-1 h-4 w-4" />
              Back
            </Button>
          ) : (
            <Link href="/dashboard">
              <Button variant="ghost">Cancel</Button>
            </Link>
          )}
        </div>

        <div>
          {currentStep < 4 ? (
            <Button onClick={handleNext} disabled={!canProceed()}>
              Next
              <ChevronRight className="ml-1 h-4 w-4" />
            </Button>
          ) : (
            <Button
              onClick={handleLaunch}
              disabled={startOnboarding.isPending}
              size="lg"
            >
              {startOnboarding.isPending ? (
                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
              ) : (
                <Rocket className="mr-2 h-4 w-4" />
              )}
              Launch Setup
            </Button>
          )}
        </div>
      </div>
    </div>
  );
}

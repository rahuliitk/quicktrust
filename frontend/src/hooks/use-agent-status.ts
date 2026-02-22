"use client";

import { useEffect, useState } from "react";
import { useAgentRun } from "./use-api";
import type { AgentRun } from "@/lib/types";

export function useAgentStatus(orgId: string, runId: string | null) {
  const [polling, setPolling] = useState(false);
  const [elapsed, setElapsed] = useState(0);

  const { data, refetch } = useAgentRun(orgId, runId || "");

  useEffect(() => {
    if (!runId || !data) return;

    const isActive = data.status === "pending" || data.status === "running";
    setPolling(isActive);

    if (!isActive) return;

    const interval = setInterval(() => {
      refetch();
      setElapsed((prev) => prev + 3);
    }, 3000);

    return () => clearInterval(interval);
  }, [runId, data, refetch]);

  return {
    run: data || null,
    polling,
    elapsed,
    isComplete: data?.status === "completed",
    isFailed: data?.status === "failed",
  };
}

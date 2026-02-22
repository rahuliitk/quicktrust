"use client";

import { useEffect } from "react";
import { login } from "@/lib/auth";

export default function LoginPage() {
  useEffect(() => {
    login();
  }, []);

  return (
    <div className="flex min-h-screen items-center justify-center">
      <p className="text-muted-foreground">Redirecting to login...</p>
    </div>
  );
}

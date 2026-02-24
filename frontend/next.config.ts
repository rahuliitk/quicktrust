import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // 'standalone' output requires symlink permissions on Windows.
  // Enable only in Docker/CI builds via NEXT_OUTPUT_STANDALONE env var.
  ...(process.env.NEXT_OUTPUT_STANDALONE === "true" ? { output: "standalone" as const } : {}),
};

export default nextConfig;

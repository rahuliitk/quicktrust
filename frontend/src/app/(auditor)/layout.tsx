import { Shield } from "lucide-react";

export default function AuditorLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="min-h-screen bg-background">
      <header className="border-b">
        <div className="container mx-auto flex h-14 items-center px-6">
          <Shield className="h-6 w-6 text-primary mr-2" />
          <span className="font-bold text-lg">QuickTrust</span>
          <span className="ml-2 text-sm text-muted-foreground">
            Auditor Portal
          </span>
        </div>
      </header>
      <main className="container mx-auto p-6">{children}</main>
    </div>
  );
}

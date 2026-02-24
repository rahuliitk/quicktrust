"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { cn } from "@/lib/utils";
import { useAuth } from "@/providers/auth-provider";
import {
  LayoutDashboard,
  Shield,
  ListChecks,
  FileText,
  FileStack,
  FileCheck,
  Bot,
  AlertTriangle,
  Plug,
  ClipboardCheck,
  Rocket,
  AlertCircle,
  Building2,
  GraduationCap,
  UserCheck,
  Activity,
  MessageSquare,
  Globe,
  BarChart3,
  Settings,
} from "lucide-react";

// Role constants matching backend
const ADMIN_ROLES = ["super_admin", "admin"];
const COMPLIANCE_ROLES = ["super_admin", "admin", "compliance_manager"];
const INTERNAL_ROLES = ["super_admin", "admin", "compliance_manager", "control_owner", "employee", "executive", "auditor_internal"];

interface NavItem {
  href: string;
  label: string;
  icon: React.ComponentType<{ className?: string }>;
  section: string;
  allowedRoles?: string[];
}

const navItems: NavItem[] = [
  // Overview
  { href: "/onboarding", label: "Quick Start", icon: Rocket, section: "Overview" },
  { href: "/dashboard", label: "Dashboard", icon: LayoutDashboard, section: "Overview" },
  // Compliance
  { href: "/frameworks", label: "Frameworks", icon: Shield, section: "Compliance" },
  { href: "/controls", label: "Controls", icon: ListChecks, section: "Compliance" },
  { href: "/evidence", label: "Evidence", icon: FileCheck, section: "Compliance" },
  { href: "/policies", label: "Policies", icon: FileText, section: "Compliance" },
  // Operations
  { href: "/risks", label: "Risk Register", icon: AlertTriangle, section: "Operations" },
  { href: "/incidents", label: "Incidents", icon: AlertCircle, section: "Operations" },
  { href: "/vendors", label: "Vendor Risk", icon: Building2, section: "Operations" },
  { href: "/monitoring", label: "Monitoring", icon: Activity, section: "Operations" },
  // People
  { href: "/training", label: "Training", icon: GraduationCap, section: "People" },
  { href: "/access-reviews", label: "Access Reviews", icon: UserCheck, section: "People" },
  // Trust
  { href: "/questionnaires", label: "Questionnaires", icon: MessageSquare, section: "Trust" },
  { href: "/trust-center", label: "Trust Center", icon: Globe, section: "Trust" },
  { href: "/audits", label: "Audits", icon: ClipboardCheck, section: "Trust" },
  // Insights
  { href: "/reports", label: "Reports", icon: BarChart3, section: "Insights" },
  { href: "/integrations", label: "Integrations", icon: Plug, section: "Insights", allowedRoles: COMPLIANCE_ROLES },
  // Config
  { href: "/control-templates", label: "Templates", icon: FileStack, section: "Config", allowedRoles: COMPLIANCE_ROLES },
  { href: "/agents", label: "AI Agents", icon: Bot, section: "Config", allowedRoles: COMPLIANCE_ROLES },
  { href: "/settings", label: "Settings", icon: Settings, section: "Config", allowedRoles: ADMIN_ROLES },
];

export function AppSidebar() {
  const pathname = usePathname();
  const { userInfo } = useAuth();
  const userRole = userInfo?.role;

  // Filter nav items based on user role
  const filteredItems = navItems.filter((item) => {
    if (!item.allowedRoles) return true; // No restriction
    if (!userRole) return true; // Dev mode fallback: show all
    return item.allowedRoles.includes(userRole);
  });

  // Group items by section
  const sections: { name: string; items: NavItem[] }[] = [];
  let currentSection = "";
  for (const item of filteredItems) {
    if (item.section !== currentSection) {
      currentSection = item.section;
      sections.push({ name: currentSection, items: [] });
    }
    sections[sections.length - 1].items.push(item);
  }

  return (
    <aside className="flex h-screen w-64 flex-col border-r bg-sidebar text-sidebar-foreground">
      <div className="flex h-14 items-center border-b px-6">
        <Link href="/dashboard" className="flex items-center gap-2 font-bold text-lg">
          <Shield className="h-6 w-6 text-primary" />
          <span>QuickTrust</span>
        </Link>
      </div>
      <nav className="flex-1 overflow-y-auto p-4">
        {sections.map((section) => (
          <div key={section.name} className="mb-3">
            <div className="mb-1 px-3 text-[10px] font-semibold uppercase tracking-wider text-sidebar-foreground/40">
              {section.name}
            </div>
            <div className="space-y-0.5">
              {section.items.map((item) => {
                const isActive = pathname === item.href || pathname.startsWith(item.href + "/");
                return (
                  <Link
                    key={item.href}
                    href={item.href}
                    className={cn(
                      "flex items-center gap-3 rounded-lg px-3 py-1.5 text-sm font-medium transition-colors",
                      isActive
                        ? "bg-sidebar-accent text-sidebar-accent-foreground"
                        : "text-sidebar-foreground/70 hover:bg-sidebar-accent/50 hover:text-sidebar-foreground"
                    )}
                  >
                    <item.icon className="h-4 w-4" />
                    {item.label}
                  </Link>
                );
              })}
            </div>
          </div>
        ))}
      </nav>
      <div className="border-t p-4 text-xs text-muted-foreground">
        QuickTrust v0.4.0
      </div>
    </aside>
  );
}

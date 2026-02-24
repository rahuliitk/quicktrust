"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import { Shield, FileText, ExternalLink, CheckCircle2, Lock } from "lucide-react";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

interface TrustCenterDoc {
  id: string;
  title: string;
  document_type: string;
  description?: string;
  url?: string;
  is_public: boolean;
  requires_nda: boolean;
}

interface TrustCenterData {
  headline: string;
  description: string;
  certifications: string[];
  contact_email: string;
  documents: TrustCenterDoc[];
}

export default function PublicTrustCenterPage() {
  const params = useParams();
  const slug = params.slug as string;
  const [data, setData] = useState<TrustCenterData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function fetchTrustCenter() {
      try {
        const res = await fetch(`${API_URL}/api/v1/trust/${slug}`);
        if (!res.ok) {
          if (res.status === 404) {
            setError("Trust center not found or not published.");
          } else {
            setError("Failed to load trust center.");
          }
          return;
        }
        const json = await res.json();
        setData(json);
      } catch {
        setError("Failed to connect to the server.");
      } finally {
        setLoading(false);
      }
    }
    fetchTrustCenter();
  }, [slug]);

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50 dark:bg-gray-950">
        <div className="animate-pulse space-y-4 text-center">
          <Shield className="h-16 w-16 mx-auto text-gray-300" />
          <p className="text-gray-400">Loading trust center...</p>
        </div>
      </div>
    );
  }

  if (error || !data) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50 dark:bg-gray-950">
        <div className="text-center space-y-4">
          <Shield className="h-16 w-16 mx-auto text-gray-400" />
          <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
            {error || "Trust center not available"}
          </h1>
          <p className="text-gray-500">
            This trust center may not be published yet.
          </p>
        </div>
      </div>
    );
  }

  const publicDocs = data.documents.filter((d) => d.is_public);
  const ndaDocs = data.documents.filter((d) => d.requires_nda && !d.is_public);

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-950">
      {/* Hero */}
      <header className="bg-white dark:bg-gray-900 border-b">
        <div className="mx-auto max-w-4xl px-6 py-16 text-center">
          <Shield className="h-12 w-12 mx-auto text-blue-600 mb-4" />
          <h1 className="text-4xl font-bold tracking-tight text-gray-900 dark:text-white">
            {data.headline || "Security & Compliance"}
          </h1>
          {data.description && (
            <p className="mt-4 text-lg text-gray-600 dark:text-gray-300 max-w-2xl mx-auto">
              {data.description}
            </p>
          )}
        </div>
      </header>

      <main className="mx-auto max-w-4xl px-6 py-12 space-y-12">
        {/* Certifications */}
        {data.certifications.length > 0 && (
          <section>
            <h2 className="text-2xl font-semibold text-gray-900 dark:text-white mb-6">
              Certifications & Compliance
            </h2>
            <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
              {data.certifications.map((cert) => (
                <div
                  key={cert}
                  className="flex items-center gap-3 rounded-lg border bg-white dark:bg-gray-900 p-4"
                >
                  <CheckCircle2 className="h-6 w-6 text-green-500 shrink-0" />
                  <span className="font-medium text-gray-900 dark:text-white">
                    {cert}
                  </span>
                </div>
              ))}
            </div>
          </section>
        )}

        {/* Public Documents */}
        {publicDocs.length > 0 && (
          <section>
            <h2 className="text-2xl font-semibold text-gray-900 dark:text-white mb-6">
              Resources
            </h2>
            <div className="space-y-3">
              {publicDocs.map((doc) => (
                <div
                  key={doc.id}
                  className="flex items-center gap-4 rounded-lg border bg-white dark:bg-gray-900 p-4"
                >
                  <FileText className="h-6 w-6 text-blue-500 shrink-0" />
                  <div className="flex-1 min-w-0">
                    <div className="font-medium text-gray-900 dark:text-white">
                      {doc.title}
                    </div>
                    {doc.description && (
                      <p className="text-sm text-gray-500 mt-1">
                        {doc.description}
                      </p>
                    )}
                  </div>
                  <span className="text-xs capitalize px-2 py-1 rounded-full bg-gray-100 dark:bg-gray-800 text-gray-600 dark:text-gray-300">
                    {doc.document_type}
                  </span>
                  {doc.url && (
                    <a
                      href={doc.url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-blue-600 hover:text-blue-800"
                    >
                      <ExternalLink className="h-5 w-5" />
                    </a>
                  )}
                </div>
              ))}
            </div>
          </section>
        )}

        {/* NDA-Required Documents */}
        {ndaDocs.length > 0 && (
          <section>
            <h2 className="text-2xl font-semibold text-gray-900 dark:text-white mb-6">
              NDA-Required Documents
            </h2>
            <div className="space-y-3">
              {ndaDocs.map((doc) => (
                <div
                  key={doc.id}
                  className="flex items-center gap-4 rounded-lg border bg-white dark:bg-gray-900 p-4 opacity-75"
                >
                  <Lock className="h-6 w-6 text-amber-500 shrink-0" />
                  <div className="flex-1 min-w-0">
                    <div className="font-medium text-gray-900 dark:text-white">
                      {doc.title}
                    </div>
                    <p className="text-sm text-amber-600 mt-1">
                      Requires NDA — contact us for access
                    </p>
                  </div>
                  <span className="text-xs capitalize px-2 py-1 rounded-full bg-gray-100 dark:bg-gray-800 text-gray-600 dark:text-gray-300">
                    {doc.document_type}
                  </span>
                </div>
              ))}
            </div>
          </section>
        )}

        {/* Contact */}
        {data.contact_email && (
          <section className="text-center rounded-lg border bg-white dark:bg-gray-900 p-8">
            <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-2">
              Questions?
            </h2>
            <p className="text-gray-600 dark:text-gray-300">
              Contact our security team at{" "}
              <a
                href={`mailto:${data.contact_email}`}
                className="text-blue-600 hover:underline"
              >
                {data.contact_email}
              </a>
            </p>
          </section>
        )}
      </main>

      <footer className="border-t py-6 text-center text-sm text-gray-500">
        Powered by QuickTrust
      </footer>
    </div>
  );
}

"use client";

import { useState } from "react";
import { HeroSection } from "../components/hero-section";
import {
  BuildModesSection,
  DocsSection,
  FeatureSection,
  TrustStrip,
  WorkflowSection
} from "../components/product-sections";
import { QueryComposer } from "../components/query-composer";
import { ResultPanel } from "../components/result-panel";
import { SiteHeader } from "../components/site-header";
import { runPolicyQuery } from "../lib/client/query-client";
import type { PipelineResult } from "../lib/types";

export default function Home() {
  const [query, setQuery] = useState("");
  const [result, setResult] = useState<PipelineResult | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  async function submit(nextQuery = query) {
    const trimmed = nextQuery.trim();
    if (!trimmed || loading) {
      return;
    }

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      setResult(await runPolicyQuery(trimmed));
    } catch (requestError) {
      setError(
        requestError instanceof Error
          ? requestError.message
          : "Request failed."
      );
    } finally {
      setLoading(false);
    }
  }

  function handleSampleSelect(sample: string) {
    setQuery(sample);
    void submit(sample);
  }

  return (
    <main>
      <SiteHeader />
      <HeroSection />
      <TrustStrip />

      <section className="console-section" id="console">
        <div className="console-heading">
          <p className="eyebrow">Live Console</p>
          <h2>Run the governed retrieval flow.</h2>
          <p>
            Use a sample or ask your own question. The response shows status,
            verdict, confidence, cited documents, and grounding signals.
          </p>
        </div>

        <div className="console-grid">
          <aside className="sample-panel">
            <p>Samples</p>
            {[
              "How do I request a refund?",
              "Can support override the refund deadline?",
              "My account was hacked and I see unauthorized access.",
              "What is the account closure process?"
            ].map((sample) => (
              <button
                key={sample}
                type="button"
                onClick={() => handleSampleSelect(sample)}
              >
                {sample}
              </button>
            ))}
          </aside>

          <section className="main-panel">
            <QueryComposer
              query={query}
              loading={loading}
              onQueryChange={setQuery}
              onSubmit={() => void submit()}
            />
            <ResultPanel result={result} error={error} loading={loading} />
          </section>
        </div>
      </section>

      <BuildModesSection />
      <WorkflowSection />
      <FeatureSection />
      <DocsSection />
    </main>
  );
}

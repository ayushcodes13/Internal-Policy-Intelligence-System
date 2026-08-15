"use client";

import { useState } from "react";
import { QueryComposer } from "../components/query-composer";
import { ResultPanel } from "../components/result-panel";
import { Sidebar } from "../components/sidebar";
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
    <main className="shell">
      <section className="workspace">
        <Sidebar onSampleSelect={handleSampleSelect} />
        <section className="main-panel">
          <QueryComposer
            query={query}
            loading={loading}
            onQueryChange={setQuery}
            onSubmit={() => void submit()}
          />
          <ResultPanel result={result} error={error} loading={loading} />
        </section>
      </section>
    </main>
  );
}

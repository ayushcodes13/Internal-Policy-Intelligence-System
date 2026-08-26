import { useMutation } from "@tanstack/react-query";
import { FileText, Loader2, Quote, SendHorizontal } from "lucide-react";
import { useState } from "react";
import { fetchPolicyQuery } from "../lib/api";
import { productConfig } from "../lib/product";
import type { PipelineResult } from "../lib/types";
import { Button } from "../components/ui/button";

export function QueryConsole() {
  const [query, setQuery] = useState("");
  const mutation = useMutation<PipelineResult, Error, string>({
    mutationFn: fetchPolicyQuery
  });

  function submit(nextQuery = query) {
    const trimmed = nextQuery.trim();
    if (!trimmed || mutation.isPending) {
      return;
    }
    mutation.mutate(trimmed);
  }

  return (
    <section id="console" className="mx-auto w-[min(1120px,calc(100%-32px))] scroll-mt-28 py-20">
      <div className="motion-rise max-w-3xl">
        <p className="eyebrow">Live Console</p>
        <h2 className="section-title">Run the governed retrieval flow.</h2>
        <p className="mt-4 text-lg leading-8 text-[var(--muted)]">
          Use a sample or ask your own question. The response shows status,
          verdict, confidence, cited documents, and grounding signals.
        </p>
      </div>

      <div className="mt-8 grid grid-cols-[300px_minmax(0,1fr)] gap-5 max-lg:grid-cols-1">
        <aside className="card motion-rise self-start p-4">
          <p className="mb-3 text-xs font-black uppercase text-[var(--muted)]">Samples</p>
          <div className="grid gap-2">
            {productConfig.sampleQueries.map((sample) => (
              <button
                className="rounded-2xl bg-white p-4 text-left leading-6 transition hover:-translate-y-0.5 hover:ring-2 hover:ring-[var(--ink)]"
                key={sample}
                type="button"
                onClick={() => {
                  setQuery(sample);
                  submit(sample);
                }}
              >
                {sample}
              </button>
            ))}
          </div>
        </aside>

        <section className="min-w-0">
          <form
            className="card motion-rise motion-delay-1 mb-4 p-4"
            onSubmit={(event) => {
              event.preventDefault();
              submit();
            }}
          >
            <label className="mb-2 block text-xs font-black uppercase text-[var(--muted)]" htmlFor="policy-query">
              Policy Query
            </label>
            <div className="grid grid-cols-[minmax(0,1fr)_112px] gap-3 max-sm:grid-cols-1">
              <input
                id="policy-query"
                className="min-h-12 min-w-0 rounded-2xl border border-[var(--line)] bg-[var(--soft)] px-4 outline-none focus:border-violet-700 focus:bg-white"
                value={query}
                onChange={(event) => setQuery(event.target.value)}
                placeholder="Ask about refunds, account closure, access, security, or support process."
              />
              <Button type="submit" disabled={mutation.isPending || !query.trim()}>
                {mutation.isPending ? <Loader2 className="h-4 w-4 animate-spin" /> : <SendHorizontal className="h-4 w-4" />}
                Run
              </Button>
            </div>
          </form>

          <ResultPanel result={mutation.data} error={mutation.error?.message} loading={mutation.isPending} />
        </section>
      </div>
    </section>
  );
}

function ResultPanel({
  result,
  error,
  loading
}: {
  result?: PipelineResult;
  error?: string;
  loading: boolean;
}) {
  if (loading) {
    return (
      <div className="result-zone motion-fade grid place-items-center text-[var(--muted)]">
        <span className="inline-flex items-center gap-3">
          <span className="status-pulse h-2.5 w-2.5 rounded-full bg-emerald-500" />
          Running Python governance pipeline...
        </span>
      </div>
    );
  }

  if (error) {
    return (
      <div className="result-zone motion-fade border-rose-300 bg-rose-50">
        <h3 className="text-xl font-black text-rose-900">Request failed</h3>
        <p className="mt-2 text-rose-800">{error}</p>
      </div>
    );
  }

  if (!result) {
    return (
      <div className="result-zone motion-fade grid place-items-center text-center text-[var(--muted)]">
        <div>
          <h3 className="text-xl font-black text-[var(--ink)]">Ready</h3>
          <p className="mt-2">Submit a policy question to run the governance pipeline.</p>
        </div>
      </div>
    );
  }

  return (
    <div className="result-zone motion-fade">
      <div className="grid grid-cols-4 gap-3 max-md:grid-cols-2">
        {[
          ["Status", result.status],
          ["Verdict", result.verdict],
          ["Confidence", result.confidence],
          ["Context", String(result.context_used)]
        ].map(([label, value]) => (
          <div className="motion-rise rounded-2xl border border-[var(--line)] bg-[var(--soft)] p-4" key={label}>
            <span className="block text-xs font-black uppercase text-[var(--muted)]">{label}</span>
            <strong className="mt-2 block break-words">{value}</strong>
          </div>
        ))}
      </div>

      <article className="mt-4 min-w-0 rounded-2xl border border-[var(--line)] bg-white p-5">
        <h3 className="text-lg font-black">Response</h3>
        <p className="mt-3 whitespace-pre-wrap break-words leading-7 text-[var(--muted)]">
          {result.answer || result.message || "No answer returned."}
        </p>
      </article>

      <div className="mt-4 grid grid-cols-2 gap-4 max-lg:grid-cols-1">
        <article className="min-w-0 rounded-2xl border border-[var(--line)] bg-white p-5">
          <h3 className="text-lg font-black">Sources</h3>
          <div className="mt-3 grid gap-2">
            {result.sources.length ? (
              result.sources.map((source) => <SourceRow key={source} source={source} />)
            ) : (
              <EmptyResultLine>No cited source.</EmptyResultLine>
            )}
          </div>
        </article>
        <article className="min-w-0 rounded-2xl border border-[var(--line)] bg-white p-5">
          <h3 className="text-lg font-black">Supporting clauses</h3>
          <div className="mt-3 grid gap-2">
            {result.supporting_clauses.length ? (
              result.supporting_clauses.map((clause) => <ClauseRow key={clause} clause={clause} />)
            ) : (
              <EmptyResultLine>No supporting clauses returned.</EmptyResultLine>
            )}
          </div>
        </article>
      </div>
    </div>
  );
}

function SourceRow({ source }: { source: string }) {
  const label = source.split("/").at(-1) || source;

  return (
    <div className="min-w-0 rounded-xl border border-[var(--line)] bg-[var(--soft)] p-3">
      <div className="flex min-w-0 items-start gap-2.5">
        <FileText className="mt-0.5 h-4 w-4 shrink-0 text-[var(--muted)]" />
        <div className="min-w-0">
          <p className="break-words text-sm font-black leading-5 text-[var(--ink)]">{label}</p>
          <p className="mt-1 break-all font-mono text-[11px] leading-5 text-[var(--muted)]">{source}</p>
        </div>
      </div>
    </div>
  );
}

function ClauseRow({ clause }: { clause: string }) {
  return (
    <div className="min-w-0 rounded-xl border border-[var(--line)] bg-[var(--soft)] p-3">
      <div className="flex min-w-0 items-start gap-2.5">
        <Quote className="mt-1 h-4 w-4 shrink-0 text-[var(--muted)]" />
        <p className="min-w-0 whitespace-pre-wrap break-words text-sm leading-6 text-[var(--muted)]">{clause}</p>
      </div>
    </div>
  );
}

function EmptyResultLine({ children }: { children: React.ReactNode }) {
  return (
    <p className="rounded-xl border border-dashed border-[var(--line)] bg-[var(--soft)] p-3 text-sm leading-6 text-[var(--muted)]">
      {children}
    </p>
  );
}

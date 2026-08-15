import type { PipelineResult } from "../lib/types";
import { StatusMetrics } from "./status-metrics";

type ResultPanelProps = {
  result: PipelineResult | null;
  error: string | null;
  loading: boolean;
};

export function ResultPanel({ result, error, loading }: ResultPanelProps) {
  const statusTone = getStatusTone(result);

  return (
    <section className={`result-zone ${statusTone}`} aria-live="polite">
      {!result && !error && !loading ? (
        <EmptyState
          title="Ready"
          message="Submit a policy question to run the governance pipeline."
        />
      ) : null}

      {loading ? (
        <EmptyState
          title="Analyzing"
          message="Intent, retrieval, governance, and grounding checks are running."
        />
      ) : null}

      {error ? (
        <article className="error-box">
          <h2>Configuration Error</h2>
          <p>{error}</p>
        </article>
      ) : null}

      {result ? (
        <>
          <StatusMetrics result={result} />
          <AnswerBlock result={result} />
          <GroundingWarning result={result} />
          <EvidenceGrid result={result} />
        </>
      ) : null}
    </section>
  );
}

function EmptyState({ title, message }: { title: string; message: string }) {
  return (
    <div className="empty-state">
      <h2>{title}</h2>
      <p>{message}</p>
    </div>
  );
}

function AnswerBlock({ result }: { result: PipelineResult }) {
  return (
    <article className="answer-block">
      <h2>
        {result.status === "SAFE"
          ? "Answer"
          : result.status === "ESCALATED"
            ? "Escalation"
            : "Refusal"}
      </h2>
      <p>{result.answer || result.message || "No answer was generated."}</p>
    </article>
  );
}

function GroundingWarning({ result }: { result: PipelineResult }) {
  if (!result.hallucination_detected) {
    return null;
  }

  return (
    <article className="warning-block">
      <h2>Grounding Warning</h2>
      <ul>
        {(result.unsupported_clauses || []).map((clause) => (
          <li key={clause}>{clause}</li>
        ))}
      </ul>
    </article>
  );
}

function EvidenceGrid({ result }: { result: PipelineResult }) {
  return (
    <section className="evidence-grid">
      <EvidenceList
        title="Sources"
        emptyText="No specific documents cited."
        items={result.sources}
      />
      <EvidenceList
        title="Supporting Clauses"
        emptyText="No exact clauses quoted."
        items={result.supporting_clauses}
      />
    </section>
  );
}

function EvidenceList({
  title,
  emptyText,
  items
}: {
  title: string;
  emptyText: string;
  items: string[];
}) {
  return (
    <article>
      <h2>{title}</h2>
      {items.length ? (
        <ul>
          {items.map((item) => (
            <li key={item}>{item}</li>
          ))}
        </ul>
      ) : (
        <p>{emptyText}</p>
      )}
    </article>
  );
}

function getStatusTone(result: PipelineResult | null) {
  if (!result) {
    return "idle";
  }
  if (result.status === "SAFE") {
    return "safe";
  }
  if (result.status === "ESCALATED") {
    return "escalated";
  }
  return "refused";
}

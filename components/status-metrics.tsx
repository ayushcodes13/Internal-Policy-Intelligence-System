import type { PipelineResult } from "../lib/types";

type StatusMetricsProps = {
  result: PipelineResult;
};

export function StatusMetrics({ result }: StatusMetricsProps) {
  const metrics = [
    ["Status", result.status],
    ["Verdict", result.verdict],
    ["Confidence", result.confidence.toUpperCase()],
    ["Sources", String(result.context_used)]
  ];

  return (
    <div className="metrics">
      {metrics.map(([label, value]) => (
        <div className="metric" key={label}>
          <span>{label}</span>
          <strong>{value}</strong>
        </div>
      ))}
    </div>
  );
}

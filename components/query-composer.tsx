import { FormEvent } from "react";

type QueryComposerProps = {
  query: string;
  loading: boolean;
  onQueryChange: (query: string) => void;
  onSubmit: () => void;
};

export function QueryComposer({
  query,
  loading,
  onQueryChange,
  onSubmit
}: QueryComposerProps) {
  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    onSubmit();
  }

  return (
    <form onSubmit={handleSubmit} className="query-form">
      <label htmlFor="query">Policy Query</label>
      <div className="query-row">
        <input
          id="query"
          value={query}
          onChange={(event) => onQueryChange(event.target.value)}
          placeholder="Ask about refunds, account closure, access, security, or support process."
          maxLength={1000}
        />
        <button type="submit" disabled={loading || !query.trim()}>
          {loading ? "Running" : "Run"}
        </button>
      </div>
    </form>
  );
}

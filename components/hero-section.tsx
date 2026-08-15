import { productConfig } from "../config/product";

export function HeroSection() {
  return (
    <section className="hero-section" id="top">
      <div className="hero-copy">
        <div className="release-pill">
          <span>New</span>
          Gemini embeddings are now wired for Vercel
        </div>
        <h1>{productConfig.tagline}</h1>
        <p>{productConfig.description}</p>

        <div className="hero-actions">
          <a className="primary-action" href="#console">
            Run a policy query
          </a>
          <a className="secondary-action" href="#architecture">
            View architecture
          </a>
        </div>

        <div className="prompt-strip" aria-label="Example prompt shortcuts">
          {productConfig.heroChips.map((chip) => (
            <span key={chip}>{chip}</span>
          ))}
        </div>
      </div>

      <div className="hero-visual" aria-label="CANON governance preview">
        <div className="terminal-window">
          <div className="terminal-topbar">
            <span />
            <span />
            <span />
            <strong>policy.query</strong>
          </div>
          <pre>{`POST /api/query

intent: refund_query
owners: finance
retrieval: billing_and_refund_policy_v2.md
verdict: SAFE
grounding: passed

answer.format = {
  "sources": ["data/raw_docs/..."],
  "confidence": "high"
}`}</pre>
        </div>
      </div>
    </section>
  );
}

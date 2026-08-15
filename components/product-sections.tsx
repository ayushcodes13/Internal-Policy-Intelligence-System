import { productConfig } from "../config/product";

export function TrustStrip() {
  return (
    <section className="trust-strip" aria-label="CANON operating promises">
      <span>Built for teams that cannot afford guesswork</span>
      <span>Source citations</span>
      <span>Structured verdicts</span>
      <span>Serverless-ready retrieval</span>
    </section>
  );
}

export function BuildModesSection() {
  return (
    <section className="section-band" id="product">
      <div className="section-heading">
        <p className="eyebrow">Product</p>
        <h2>One policy brain with two surfaces.</h2>
      </div>

      <div className="mode-grid">
        <article className="mode-card">
          <div className="code-card">
            <pre>{`const response = await fetch("/api/query", {
  method: "POST",
  body: JSON.stringify({
    query: "Can support override a refund deadline?"
  })
});`}</pre>
          </div>
          <h3>Policy API</h3>
          <p>
            Call the governed pipeline from your own frontend, Slackbot,
            internal portal, or ticket workflow.
          </p>
        </article>

        <article className="mode-card">
          <div className="playground-card">
            <div className="mini-toolbar">
              <span>SAFE</span>
              <span>HIGH</span>
              <span>5 sources</span>
            </div>
            <div className="mini-answer">
              Refund requests are routed to Finance and answered only from the
              latest approved policy.
            </div>
          </div>
          <h3>Policy Playground</h3>
          <p>
            A clean interface for testing policy questions, verifying sources,
            and debugging governance decisions.
          </p>
        </article>
      </div>
    </section>
  );
}

export function WorkflowSection() {
  return (
    <section className="section-band split-band" id="workflow">
      <div className="section-heading">
        <p className="eyebrow">Workflow</p>
        <h2>Ask anything. Answer only when the evidence is good.</h2>
        <p>
          CANON separates routing, retrieval, governance, generation, and
          grounding so every response has an audit trail.
        </p>
      </div>

      <div className="workflow-steps">
        {[
          "Detect intent",
          "Scope owners",
          "Retrieve latest policies",
          "Apply constraints",
          "Resolve verdict",
          "Ground answer"
        ].map((step, index) => (
          <div className="workflow-step" key={step}>
            <span>{String(index + 1).padStart(2, "0")}</span>
            <strong>{step}</strong>
          </div>
        ))}
      </div>
    </section>
  );
}

export function FeatureSection() {
  return (
    <section className="section-band" id="architecture">
      <div className="section-heading">
        <p className="eyebrow">Architecture</p>
        <h2>Productionized for Vercel without the local ML weight.</h2>
      </div>

      <div className="feature-grid">
        {productConfig.features.map((feature) => (
          <article className="feature-card" key={feature.title}>
            <h3>{feature.title}</h3>
            <p>{feature.body}</p>
          </article>
        ))}
      </div>

      <div className="stats-row">
        {productConfig.stats.map((stat) => (
          <div key={stat.label}>
            <strong>{stat.value}</strong>
            <span>{stat.label}</span>
          </div>
        ))}
      </div>
    </section>
  );
}

export function DocsSection() {
  return (
    <section className="section-band docs-band" id="docs">
      <div>
        <p className="eyebrow">Docs</p>
        <h2>Readable structure for future debugging.</h2>
      </div>
      <p>
        The README and architecture notes now document the production folder
        layout, environment variables, indexing workflow, deploy flow, and the
        legacy Streamlit boundary.
      </p>
    </section>
  );
}

import { ArrowUpRight, BrainCircuit, FileCheck2, GitBranch, Github, LockKeyhole, Server, ShieldCheck } from "lucide-react";
import { QueryConsole } from "../sections/query-console";
import { Button } from "../components/ui/button";
import { productConfig } from "../lib/product";

const decisionTrace = [
  {
    label: "Intent",
    value: "refund_query",
    body: "Groq classifies what the user is asking before retrieval starts."
  },
  {
    label: "Owner",
    value: "Finance",
    body: "The router narrows the answer space to the policy owner that controls the rule."
  },
  {
    label: "Evidence",
    value: "v2 policy",
    body: "Gemini embeddings retrieve approved markdown chunks from the static search index."
  },
  {
    label: "Verdict",
    value: "SAFE",
    body: "The governance gate decides safe, refuse, invalid, or escalate before generation."
  }
];

const architectureFlow = [
  {
    title: "Query intake",
    detail: "React sends the policy question to the Python FastAPI endpoint at POST /api/query.",
    icon: BrainCircuit
  },
  {
    title: "Intent and owner routing",
    detail: "Groq classifies intent while deterministic routing scopes the request to Finance, Operations, Security, or Support.",
    icon: GitBranch
  },
  {
    title: "Embedding retrieval",
    detail: "Gemini embeds the query and searches the prebuilt JSON index created from markdown policy documents.",
    icon: FileCheck2
  },
  {
    title: "Canonical version filter",
    detail: "The pipeline prefers the newest approved policy version, so stale documents do not override current rules.",
    icon: LockKeyhole
  },
  {
    title: "Governance verdict",
    detail: "The system returns SAFE, REFUSE_POLICY, REFUSE_INVALID, or ESCALATE before answer generation is allowed.",
    icon: ShieldCheck
  },
  {
    title: "Grounded response",
    detail: "The final answer includes sources, supporting clauses, confidence, context count, and grounding status.",
    icon: Server
  }
];

const controlPoints = [
  ["Source of truth", "Only approved files in data/raw_docs become retrievable evidence."],
  ["Version priority", "Current policy versions beat older matches during retrieval and ranking."],
  ["Refusal path", "Invalid or disallowed requests are stopped before the model writes an answer."],
  ["Audit payload", "Every response exposes verdict, sources, clauses, confidence, and grounding."]
];

const footerColumns = [
  {
    title: "Product",
    links: [
      ["Live console", "#console"],
      ["Workflow", "#workflow"],
      ["Architecture", "#architecture"]
    ]
  },
  {
    title: "AI Runtime",
    links: [
      ["Python API", "#architecture"],
      ["Gemini embeddings", "#architecture"],
      ["Groq inference", "#architecture"]
    ]
  },
  {
    title: "Project",
    links: [
      ["README", "https://github.com/ayushcodes13/canon#readme"],
      ["Source code", "https://github.com/ayushcodes13/canon"],
      ["Run locally", "https://github.com/ayushcodes13/canon#run-locally"]
    ]
  }
];

export function HomePage() {
  return (
    <main className="min-h-screen bg-[var(--bg)] text-[var(--ink)]">
      <header className="motion-fade sticky top-3 z-30 mx-auto grid w-[min(1120px,calc(100%-32px))] grid-cols-[1fr_auto_1fr] items-center rounded-2xl border border-[var(--line)] bg-white/90 p-2 shadow-lg shadow-black/5 backdrop-blur max-md:grid-cols-[1fr_auto]">
        <a className="flex items-center gap-3 font-black" href="#top" aria-label="CANON home">
          <span className="grid h-11 w-11 place-items-center rounded-2xl border border-[#d8c58a]/50 bg-[#0b0f14] shadow-md">
            <img src="/canon-logo.svg" alt="" className="h-9 w-9 rounded-xl" />
          </span>
          <span className="leading-tight">
            <span className="block">{productConfig.name}</span>
            <span className="block text-xs font-bold text-[var(--muted)] max-sm:hidden">Policy-governed AI</span>
          </span>
        </a>
        <nav className="flex rounded-full border border-[var(--line)] bg-[var(--soft)] p-1 text-sm font-bold text-[var(--muted)] max-md:hidden">
          {productConfig.navItems.map((item) => (
            <a className="rounded-full px-4 py-2 hover:bg-white hover:text-[var(--ink)]" href={`#${item.toLowerCase()}`} key={item}>
              {item}
            </a>
          ))}
        </nav>
        <Button asChild className="justify-self-end">
          <a href="#console">Try console</a>
        </Button>
      </header>

      <section id="top" className="mx-auto flex w-[min(1120px,calc(100%-32px))] scroll-mt-28 flex-col items-center gap-7 py-12">
        <div className="flex max-w-5xl flex-col items-center text-center">
          <div className="motion-rise inline-flex items-center gap-3 rounded-full border border-[var(--line)] bg-[var(--soft)] px-3 py-2 text-sm font-bold text-[var(--muted)]">
            <img src="/canon-logo.svg" alt="" className="h-6 w-6 rounded-lg" />
            <span className="status-pulse rounded-full bg-emerald-100 px-2 py-1 text-xs uppercase text-emerald-700">New</span>
            Python AI backend with a TanStack frontend
          </div>
          <h1 className="motion-rise motion-delay-1 mt-5 max-w-5xl text-7xl font-black leading-[0.95] tracking-normal text-balance max-lg:text-6xl max-sm:text-5xl">
            {productConfig.tagline}
          </h1>
          <p className="motion-rise motion-delay-2 mt-5 max-w-3xl text-xl leading-8 text-[var(--muted)]">
            {productConfig.description}
          </p>
          <div className="motion-rise motion-delay-3 mt-7 flex flex-wrap justify-center gap-3">
            <Button asChild size="lg">
              <a href="#console">Run a policy query</a>
            </Button>
            <Button asChild variant="outline" size="lg">
              <a href="#architecture">View architecture</a>
            </Button>
          </div>
          <div className="motion-rise motion-delay-4 mt-6 flex flex-wrap justify-center gap-2">
            {productConfig.heroChips.map((chip) => (
              <span className="rounded-full border border-[var(--line)] bg-white px-4 py-2 text-sm font-medium text-[var(--muted)]" key={chip}>
                {chip}
              </span>
            ))}
          </div>
        </div>
        <div className="motion-rise motion-delay-4 terminal-preview w-full max-w-4xl rounded-3xl border border-[var(--line)] bg-white shadow-xl shadow-black/10">
          <div className="flex items-center gap-2 border-b border-[var(--line)] px-5 py-4">
            <span className="h-3 w-3 rounded-full bg-rose-500" />
            <span className="h-3 w-3 rounded-full bg-amber-500" />
            <span className="h-3 w-3 rounded-full bg-emerald-600" />
            <span className="ml-auto font-mono text-xs text-[var(--muted)]">policy.query</span>
          </div>
          <pre className="min-h-[340px] overflow-auto p-7 font-mono text-sm leading-7 text-[var(--ink)]">{`POST /api/query

intent: refund_query
owners: finance
retrieval: billing_and_refund_policy_v2.md
verdict: SAFE
runtime: python

answer.format = {
  "sources": ["data/raw_docs/..."],
  "confidence": "high"
}`}</pre>
        </div>
      </section>

      <section className="motion-rise mx-auto grid w-[min(1120px,calc(100%-32px))] grid-cols-[1.4fr_repeat(3,auto)] gap-4 border-y border-[var(--line)] py-5 text-sm text-[var(--muted)] max-lg:grid-cols-1">
        <strong className="text-[var(--ink)]">Built for teams that cannot afford guesswork</strong>
        <span>Python AI pipeline</span>
        <span>TanStack frontend</span>
        <span>Serverless static UI</span>
      </section>

      <QueryConsole />

      <section id="product" className="mx-auto w-[min(1120px,calc(100%-32px))] scroll-mt-28 py-20">
        <p className="eyebrow">Product</p>
        <h2 className="section-title">A policy engine that decides before it answers.</h2>
        <div className="mt-8 grid grid-cols-2 gap-5 max-lg:grid-cols-1">
          <article className="card motion-rise p-5">
            <div className="rounded-2xl border border-[var(--line)] bg-white p-5">
              <p className="text-xs font-black uppercase text-[var(--muted)]">Decision trace</p>
              <div className="mt-4 grid gap-3">
                {decisionTrace.map((item, index) => (
                  <div className="grid grid-cols-[44px_minmax(0,1fr)] gap-3 rounded-2xl border border-[var(--line)] bg-[var(--soft)] p-3" key={item.label}>
                    <span className="grid h-10 w-10 place-items-center rounded-xl bg-white font-mono text-xs font-black text-violet-700">{String(index + 1).padStart(2, "0")}</span>
                    <div>
                      <div className="flex flex-wrap items-center gap-2">
                        <strong>{item.label}</strong>
                        <span className="rounded-full bg-white px-2 py-1 font-mono text-xs text-[var(--muted)]">{item.value}</span>
                      </div>
                      <p className="mt-1 text-sm leading-6 text-[var(--muted)]">{item.body}</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
            <h3 className="mt-5 text-xl font-black">Readable execution path</h3>
            <p className="mt-2 text-[var(--muted)]">Each answer can be debugged by following the intent, owner, evidence, verdict, and final grounded response.</p>
          </article>
          <article className="card motion-rise motion-delay-1 p-5">
            <div className="grid rounded-2xl border border-[var(--line)] bg-white p-5">
              <p className="text-xs font-black uppercase text-[var(--muted)]">Response contract</p>
              <div className="mt-4 grid grid-cols-2 gap-3">
                {[
                  ["status", "SAFE"],
                  ["owner", "finance"],
                  ["source", "billing_policy_v2.md"],
                  ["grounding", "passed"]
                ].map(([label, value]) => (
                  <div className="rounded-2xl bg-[var(--soft)] p-4" key={label}>
                    <span className="block text-xs font-black uppercase text-[var(--muted)]">{label}</span>
                    <strong className="mt-2 block break-words font-mono text-sm">{value}</strong>
                  </div>
                ))}
              </div>
              <pre className="mt-4 overflow-auto rounded-2xl bg-[var(--ink)] p-5 font-mono text-xs leading-6 text-white">{`{
  "sources": [...],
  "supporting_clauses": [...],
  "confidence": "medium",
  "hallucination_detected": false
}`}</pre>
            </div>
            <h3 className="mt-5 text-xl font-black">Audit-ready output</h3>
            <p className="mt-2 text-[var(--muted)]">The API returns the evidence and governance metadata needed to inspect why an answer was allowed, refused, or escalated.</p>
          </article>
        </div>
      </section>

      <section id="workflow" className="mx-auto grid w-[min(1120px,calc(100%-32px))] scroll-mt-28 grid-cols-[0.9fr_1.1fr] gap-10 py-20 max-lg:grid-cols-1">
        <div>
          <p className="eyebrow">Workflow</p>
          <h2 className="section-title">Ask anything. Answer only when the evidence is good.</h2>
          <p className="mt-4 text-lg leading-8 text-[var(--muted)]">CANON separates routing, retrieval, governance, generation, and grounding so every response has an audit trail.</p>
        </div>
        <div className="grid grid-cols-2 gap-3 max-sm:grid-cols-1">
          {[
            ["Detect intent", BrainCircuit],
            ["Scope owners", GitBranch],
            ["Retrieve latest policies", FileCheck2],
            ["Apply constraints", LockKeyhole],
            ["Resolve verdict", ShieldCheck],
            ["Ground answer", FileCheck2]
          ].map(([step, Icon], index) => (
            <div className="card motion-rise flex items-center gap-4 p-4" key={String(step)}>
              <span className="grid h-12 w-12 place-items-center rounded-2xl bg-white font-mono text-sm text-violet-700">{String(index + 1).padStart(2, "0")}</span>
              <Icon className="h-5 w-5 text-[var(--muted)]" />
              <strong>{String(step)}</strong>
            </div>
          ))}
        </div>
      </section>

      <section id="architecture" className="mx-auto w-[min(1120px,calc(100%-32px))] scroll-mt-28 py-20">
        <p className="eyebrow">Architecture</p>
        <h2 className="section-title">Inside the governed answer path.</h2>
        <p className="mt-4 max-w-3xl text-lg leading-8 text-[var(--muted)]">
          The codebase is organized around a policy pipeline, not a generic chatbot loop. A response is only produced after routing, retrieval, versioning, governance, and grounding checks finish.
        </p>
        <div className="mt-8 grid grid-cols-3 gap-4 max-lg:grid-cols-2 max-sm:grid-cols-1">
          {architectureFlow.map((stage, index) => {
            const Icon = stage.icon;

            return (
              <article className="card p-5" key={stage.title}>
                <div className="flex items-center justify-between gap-4">
                  <span className="grid h-11 w-11 place-items-center rounded-2xl bg-white font-mono text-sm font-black text-violet-700">{String(index + 1).padStart(2, "0")}</span>
                  <Icon className="h-5 w-5 text-[var(--muted)]" />
                </div>
                <h3 className="mt-5 text-xl font-black">{stage.title}</h3>
                <p className="mt-3 leading-7 text-[var(--muted)]">{stage.detail}</p>
              </article>
            );
          })}
        </div>
        <div className="mt-5 rounded-3xl bg-[var(--ink)] p-5 text-white">
          <div className="grid grid-cols-[0.9fr_1.1fr] gap-6 max-lg:grid-cols-1">
            <div>
              <p className="text-xs font-black uppercase text-[#d8c58a]">Control layer</p>
              <h3 className="mt-3 max-w-md text-3xl font-black leading-tight">The model is downstream from policy authority.</h3>
              <p className="mt-3 leading-7 text-white/65">
                CANON first decides what rules apply and whether the request is allowed. The LLM only writes after the retrieved evidence and verdict are available.
              </p>
            </div>
            <div className="grid grid-cols-2 gap-3 max-sm:grid-cols-1">
              {controlPoints.map(([label, detail]) => (
                <div className="rounded-2xl bg-white/10 p-4" key={label}>
                  <strong className="block">{label}</strong>
                  <span className="mt-2 block text-sm leading-6 text-white/65">{detail}</span>
                </div>
              ))}
            </div>
          </div>
          <pre className="mt-5 overflow-auto rounded-2xl bg-black/25 p-5 font-mono text-xs leading-6 text-white/75">{`query -> intent -> owner scope -> Gemini vector search
      -> newest approved policy -> verdict gate
      -> grounded answer/refusal/escalation JSON`}</pre>
        </div>
      </section>

      <footer id="docs" className="mt-10 scroll-mt-28 bg-[var(--ink)] text-white">
        <div className="mx-auto w-[min(1120px,calc(100%-32px))] py-16">
          <div className="grid grid-cols-[1.25fr_0.9fr_1.1fr] gap-8 max-lg:grid-cols-1">
            <div>
              <div className="flex items-center gap-3">
                <span className="grid h-12 w-12 place-items-center rounded-2xl border border-[#d8c58a]/60 bg-[#0b0f14] shadow-lg shadow-black/20">
                  <img src="/canon-logo.svg" alt="" className="h-10 w-10 rounded-xl" />
                </span>
                <div>
                  <strong className="block text-xl">{productConfig.name}</strong>
                  <span className="text-sm font-bold text-white/55">Policy-governed intelligence</span>
                </div>
              </div>
              <p className="mt-5 max-w-md text-base leading-7 text-white/65">
                CANON routes policy questions through ownership, retrieval, governance, and grounding before any model response is allowed back to the user.
              </p>
              <div className="mt-6 flex flex-wrap gap-2">
                {["SAFE", "REFUSE", "ESCALATE", "GROUNDED"].map((item) => (
                  <span className="rounded-full border border-white/10 bg-white/8 px-3 py-1 text-xs font-black text-white/70" key={item}>
                    {item}
                  </span>
                ))}
              </div>
            </div>

            <div className="rounded-3xl border border-white/10 bg-white/[0.04] p-5">
              <p className="text-xs font-black uppercase text-[#d8c58a]">System Path</p>
              <div className="mt-4 grid gap-3 text-sm text-white/70">
                {[
                  ["Query", BrainCircuit],
                  ["Policy owner", GitBranch],
                  ["Evidence", FileCheck2],
                  ["Verdict", ShieldCheck],
                  ["Python API", Server]
                ].map(([label, Icon]) => (
                  <div className="flex items-center gap-3" key={String(label)}>
                    <Icon className="h-4 w-4 text-[#d8c58a]" />
                    <span>{String(label)}</span>
                  </div>
                ))}
              </div>
            </div>

            <div className="grid grid-cols-3 gap-6 max-sm:grid-cols-1">
              {footerColumns.map((column) => (
                <div key={column.title}>
                  <h3 className="text-sm font-black uppercase text-white/45">{column.title}</h3>
                  <ul className="mt-4 grid gap-3 text-sm font-bold text-white/75">
                    {column.links.map(([label, href]) => (
                      <li key={label}>
                        <a className="inline-flex items-center gap-1.5 hover:text-white" href={href}>
                          {label}
                          {href.startsWith("http") ? <ArrowUpRight className="h-3.5 w-3.5" /> : null}
                        </a>
                      </li>
                    ))}
                  </ul>
                </div>
              ))}
            </div>
          </div>

          <div className="mt-12 flex flex-wrap items-center justify-between gap-4 border-t border-white/10 pt-6 text-sm text-white/50">
            <span>Built for source-backed policy decisions.</span>
            <a className="inline-flex items-center gap-2 rounded-full border border-white/10 px-4 py-2 font-black text-white hover:bg-white/10" href="https://github.com/ayushcodes13/canon">
              <Github className="h-4 w-4" />
              ayushcodes13/canon
            </a>
          </div>
        </div>
      </footer>
    </main>
  );
}

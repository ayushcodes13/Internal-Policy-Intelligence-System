import { Bar, BarChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import { BrainCircuit, FileCheck2, GitBranch, LockKeyhole, ShieldCheck } from "lucide-react";
import { QueryConsole } from "../sections/query-console";
import { Button } from "../components/ui/button";
import { productConfig } from "../lib/product";

const metricData = [
  { label: "Verdicts", value: 4 },
  { label: "Domains", value: 4 },
  { label: "Node AI", value: 0 }
];

export function HomePage() {
  return (
    <main className="min-h-screen bg-[var(--bg)] text-[var(--ink)]">
      <header className="sticky top-3 z-30 mx-auto grid w-[min(1120px,calc(100%-32px))] grid-cols-[1fr_auto_1fr] items-center rounded-2xl border border-[var(--line)] bg-white/90 p-2 shadow-lg shadow-black/5 backdrop-blur max-md:grid-cols-[1fr_auto]">
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
          <div className="inline-flex items-center gap-3 rounded-full border border-[var(--line)] bg-[var(--soft)] px-3 py-2 text-sm font-bold text-[var(--muted)]">
            <img src="/canon-logo.svg" alt="" className="h-6 w-6 rounded-lg" />
            <span className="rounded-full bg-emerald-100 px-2 py-1 text-xs uppercase text-emerald-700">New</span>
            Python AI backend with a TanStack frontend
          </div>
          <h1 className="mt-5 max-w-5xl text-7xl font-black leading-[0.95] tracking-normal text-balance max-lg:text-6xl max-sm:text-5xl">
            {productConfig.tagline}
          </h1>
          <p className="mt-5 max-w-3xl text-xl leading-8 text-[var(--muted)]">
            {productConfig.description}
          </p>
          <div className="mt-7 flex flex-wrap justify-center gap-3">
            <Button asChild size="lg">
              <a href="#console">Run a policy query</a>
            </Button>
            <Button asChild variant="outline" size="lg">
              <a href="#architecture">View architecture</a>
            </Button>
          </div>
          <div className="mt-6 flex flex-wrap justify-center gap-2">
            {productConfig.heroChips.map((chip) => (
              <span className="rounded-full border border-[var(--line)] bg-white px-4 py-2 text-sm font-medium text-[var(--muted)]" key={chip}>
                {chip}
              </span>
            ))}
          </div>
        </div>
        <div className="w-full max-w-4xl rounded-3xl border border-[var(--line)] bg-white shadow-xl shadow-black/10">
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

      <section className="mx-auto grid w-[min(1120px,calc(100%-32px))] grid-cols-[1.4fr_repeat(3,auto)] gap-4 border-y border-[var(--line)] py-5 text-sm text-[var(--muted)] max-lg:grid-cols-1">
        <strong className="text-[var(--ink)]">Built for teams that cannot afford guesswork</strong>
        <span>Python AI pipeline</span>
        <span>TanStack frontend</span>
        <span>Serverless static UI</span>
      </section>

      <QueryConsole />

      <section id="product" className="mx-auto w-[min(1120px,calc(100%-32px))] py-20">
        <p className="eyebrow">Product</p>
        <h2 className="section-title">One policy brain with two clean surfaces.</h2>
        <div className="mt-8 grid grid-cols-2 gap-5 max-lg:grid-cols-1">
          <article className="card p-5">
            <pre className="rounded-2xl border border-[var(--line)] bg-white p-5 font-mono text-sm leading-7">{`const response = await fetch("/api/query", {
  method: "POST",
  body: JSON.stringify({
    query: "Can support override a refund deadline?"
  })
});`}</pre>
            <h3 className="mt-5 text-xl font-black">React policy console</h3>
            <p className="mt-2 text-[var(--muted)]">TanStack Query owns request state, retries, loading, and error display.</p>
          </article>
          <article className="card p-5">
            <div className="rounded-2xl border border-[var(--line)] bg-white p-5">
              <ResponsiveContainer width="100%" height={180}>
                <BarChart data={metricData}>
                  <XAxis dataKey="label" tickLine={false} axisLine={false} />
                  <YAxis hide />
                  <Tooltip cursor={{ fill: "rgba(27,27,24,0.04)" }} />
                  <Bar dataKey="value" radius={[8, 8, 0, 0]} fill="#1b1b18" />
                </BarChart>
              </ResponsiveContainer>
            </div>
            <h3 className="mt-5 text-xl font-black">Audit-ready signals</h3>
            <p className="mt-2 text-[var(--muted)]">Recharts visualizes verdict, domain, and runtime signals without adding backend complexity.</p>
          </article>
        </div>
      </section>

      <section id="workflow" className="mx-auto grid w-[min(1120px,calc(100%-32px))] grid-cols-[0.9fr_1.1fr] gap-10 py-20 max-lg:grid-cols-1">
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
            <div className="card flex items-center gap-4 p-4" key={String(step)}>
              <span className="grid h-12 w-12 place-items-center rounded-2xl bg-white font-mono text-sm text-violet-700">{String(index + 1).padStart(2, "0")}</span>
              <Icon className="h-5 w-5 text-[var(--muted)]" />
              <strong>{String(step)}</strong>
            </div>
          ))}
        </div>
      </section>

      <section id="architecture" className="mx-auto w-[min(1120px,calc(100%-32px))] py-20">
        <p className="eyebrow">Architecture</p>
        <h2 className="section-title">Vite frontend. Python intelligence runtime.</h2>
        <div className="mt-8 grid grid-cols-3 gap-5 max-lg:grid-cols-1">
          {productConfig.features.map((feature) => (
            <article className="card p-6" key={feature.title}>
              <h3 className="text-xl font-black">{feature.title}</h3>
              <p className="mt-3 leading-7 text-[var(--muted)]">{feature.body}</p>
            </article>
          ))}
        </div>
        <div className="mt-5 grid grid-cols-3 gap-4 rounded-3xl bg-[var(--ink)] p-5 text-white max-md:grid-cols-1">
          {productConfig.stats.map((stat) => (
            <div className="rounded-2xl bg-white/10 p-5" key={stat.label}>
              <strong className="block text-4xl">{stat.value}</strong>
              <span className="text-white/75">{stat.label}</span>
            </div>
          ))}
        </div>
      </section>
    </main>
  );
}

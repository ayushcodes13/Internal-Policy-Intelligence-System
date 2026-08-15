import { productConfig } from "../config/product";

type SidebarProps = {
  onSampleSelect: (query: string) => void;
};

export function Sidebar({ onSampleSelect }: SidebarProps) {
  return (
    <aside className="sidebar">
      <div className="brand-lockup">
        <div className="brand-mark" aria-hidden="true">
          PL
        </div>
        <div>
          <p className="eyebrow">{productConfig.name}</p>
          <h1>{productConfig.tagline}</h1>
        </div>
      </div>

      <p className="sidebar-copy">{productConfig.description}</p>

      <div className="domain-list" aria-label="Active domains">
        {productConfig.domains.map((domain) => (
          <span key={domain}>{domain}</span>
        ))}
      </div>

      <div className="samples">
        <p>Sample Queries</p>
        {productConfig.sampleQueries.map((sample) => (
          <button
            key={sample}
            type="button"
            onClick={() => onSampleSelect(sample)}
          >
            {sample}
          </button>
        ))}
      </div>
    </aside>
  );
}

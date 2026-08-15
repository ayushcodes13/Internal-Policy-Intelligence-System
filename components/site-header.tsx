import { productConfig } from "../config/product";

export function SiteHeader() {
  return (
    <header className="site-header">
      <a className="brand" href="#top" aria-label={`${productConfig.name} home`}>
        <span className="brand-symbol">PL</span>
        <span>{productConfig.name}</span>
      </a>

      <nav className="nav-links" aria-label="Main navigation">
        {productConfig.navItems.map((item) => (
          <a key={item} href={`#${item.toLowerCase()}`}>
            {item}
          </a>
        ))}
      </nav>

      <a className="header-action" href="#console">
        Try console
      </a>
    </header>
  );
}

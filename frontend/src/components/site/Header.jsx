import { CONTACT_PHONE, NAV_LINKS } from "../../siteLinks";
import "./Header.css";

export default function Header() {
  return (
    <header className="header">
      <div className="container header__inner">
        <a href="/" className="header__logo">פרשקובסקי</a>
        <nav className="header__nav">
          {NAV_LINKS.map((link) => (
            <a key={link.label} href={link.href} target="_blank" rel="noreferrer">
              {link.label}
            </a>
          ))}
        </nav>
        <a href={`tel:${CONTACT_PHONE}`} className="header__phone">{CONTACT_PHONE}</a>
      </div>
    </header>
  );
}

import { CONTACT_PHONE, SITE_URL } from "../../siteLinks";
import "./Footer.css";

export default function Footer() {
  return (
    <footer className="footer">
      <div className="container footer__inner">
        <div>
          <div className="footer__logo">פרשקובסקי</div>
          <p>
            יצירת קשר: <a href={`tel:${CONTACT_PHONE}`} className="footer__phone">{CONTACT_PHONE}</a>
          </p>
        </div>
        <p className="footer__note">
          דמו פנימי. התוכן והתמונות שייכים לפרשקובסקי -{" "}
          <a href={SITE_URL} target="_blank" rel="noreferrer">לאתר המקורי</a>
        </p>
      </div>
    </footer>
  );
}

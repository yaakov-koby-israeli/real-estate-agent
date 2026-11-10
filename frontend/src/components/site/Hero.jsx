import "./Hero.css";

export default function Hero({ onOpenChat }) {
  return (
    <section className="hero">
      <div className="container">
        <h1 className="hero__title">הבית הבא שלך מתחיל כאן</h1>
        <p className="hero__subtitle">
          עשרות פרויקטים למגורים, להשכרה ולהתחדשות עירונית ברחבי הארץ - בחתימת האיכות של פרשקובסקי.
        </p>
        <div className="hero__actions">
          <button className="button" onClick={onOpenChat}>💬 דברו עם הסוכן הווירטואלי</button>
          <a href="#projects" className="button button--outline">לפרויקטים שלנו</a>
        </div>
      </div>
    </section>
  );
}

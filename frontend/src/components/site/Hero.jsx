import "./Hero.css";

export default function Hero() {
  return (
    <section className="hero">
      <div className="container">
        <h1 className="hero__title">הבית הבא שלך מתחיל כאן</h1>
        <p className="hero__subtitle">
          עשרות פרויקטים למגורים, להשכרה ולהתחדשות עירונית ברחבי הארץ - בחתימת האיכות של פרשקובסקי.
        </p>
        <a href="#projects" className="button">לפרויקטים שלנו</a>
      </div>
    </section>
  );
}

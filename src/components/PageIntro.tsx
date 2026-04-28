export function PageIntro({
  kicker,
  title,
  support,
}: {
  kicker?: string | null;
  title: string;
  support?: string | null;
}) {
  return (
    <section className="page-intro">
      {kicker ? <p className="page-intro__kicker">{kicker}</p> : null}
      <h2 className="page-intro__title">{title}</h2>
      {support ? <p className="page-intro__support">{support}</p> : null}
    </section>
  );
}

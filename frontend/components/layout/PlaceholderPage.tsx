/**
 * Provides a consistent temporary layout for feature routes not yet connected.
 * It keeps navigation usable while the MVP grows in working vertical slices.
 */
type PlaceholderPageProps = {
  eyebrow: string;
  title: string;
  description: string;
};

export function PlaceholderPage({ eyebrow, title, description }: PlaceholderPageProps) {
  /** Render explanatory content for one planned feature page. */
  return (
    <section>
      <p className="eyebrow">{eyebrow}</p>
      <h1>{title}</h1>
      <p className="lede">{description}</p>
      <div className="emptyState">This module will be connected in its MVP phase.</div>
    </section>
  );
}

/**
 * Renders the high-level job-search dashboard.
 * Placeholder values establish the summary layout before workflows supply real data.
 */
const summaries = [
  ["New high-fit jobs", "—"],
  ["Active applications", "—"],
  ["Interviews", "—"],
  ["Blocking failures", "0"],
] as const;

export default function DashboardPage() {
  /** Present the application's most important job-search signals at a glance. */
  return (
    <section>
      <p className="eyebrow">Dashboard</p>
      <h1>Your job search, in one place.</h1>
      <p className="lede">
        The project foundation is ready. Job discovery and application data will appear here as
        the workflows are connected.
      </p>
      <div className="summaryGrid">
        {summaries.map(([label, value]) => (
          <article className="card" key={label}>
            <span>{label}</span>
            <strong>{value}</strong>
          </article>
        ))}
      </div>
    </section>
  );
}

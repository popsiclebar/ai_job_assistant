/**
 * Defines the Jobs route used for discovery, filtering, and fit inspection.
 * The route will become the first frontend consumer of normalized JobTech results.
 */
import { PlaceholderPage } from "@/components/layout/PlaceholderPage";

export default function JobsPage() {
  /** Render the Jobs feature boundary until live search results are connected. */
  return (
    <PlaceholderPage
      eyebrow="Jobs"
      title="Discover relevant roles."
      description="Search, filter, inspect, and rank Swedish job postings from JobTech."
    />
  );
}

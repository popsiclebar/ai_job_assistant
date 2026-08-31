/**
 * Provides the shared browser-to-backend HTTP boundary.
 * Feature modules use it for consistent base URLs and failed-response handling.
 */
const apiBaseUrl =
  process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000/api/v1";

export async function apiRequest<T>(path: string, init?: RequestInit): Promise<T> {
  /** Send one typed JSON request and reject non-successful HTTP responses. */
  const response = await fetch(`${apiBaseUrl}${path}`, init);
  if (!response.ok) {
    throw new Error(`API request failed with status ${response.status}`);
  }
  return (await response.json()) as T;
}

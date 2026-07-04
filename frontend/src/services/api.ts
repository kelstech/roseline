export async function getHealth(baseUrl = '/api/v1') {
  const response = await fetch(`${baseUrl}/healthz`);
  if (!response.ok) throw new Error(`Health check failed: ${response.status}`);
  return response.json() as Promise<{ status: string; service: string }>;
}

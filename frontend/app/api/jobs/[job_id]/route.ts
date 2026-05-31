import { NextResponse } from "next/server";

export const runtime = "nodejs";

const backendBaseUrl =
  (process.env.BACKEND_URL || process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000").replace(/\/?$/, "");

export async function GET(_req: Request, { params }: { params: Promise<{ job_id: string }> }) {
  const { job_id } = await params;
  const response = await fetch(`${backendBaseUrl}/api/jobs/${job_id}`);
  const payload = await response.text();
  return new NextResponse(payload, {
    status: response.status,
    headers: { "content-type": response.headers.get("content-type") || "application/json" },
  });
}

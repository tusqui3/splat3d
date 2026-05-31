import { NextResponse } from "next/server";

export const runtime = "nodejs";

const backendBaseUrl =
  (process.env.BACKEND_URL || process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000").replace(/\/?$/, "");
const backendUploadUrl = `${backendBaseUrl}/api/upload`;

export async function POST(request: Request) {
  const formData = await request.formData();
  const file = formData.get("file");

  if (!(file instanceof File)) {
    return NextResponse.json({ detail: "Missing file." }, { status: 400 });
  }

  const proxyForm = new FormData();
  proxyForm.append("file", file, file.name);

  const response = await fetch(backendUploadUrl, {
    method: "POST",
    body: proxyForm,
  });

  const payload = await response.text();
  const contentType = response.headers.get("content-type") || "application/json";

  return new NextResponse(payload, {
    status: response.status,
    headers: { "content-type": contentType },
  });
}

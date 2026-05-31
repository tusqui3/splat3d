"use client";

import { useCallback, useEffect, useRef, useState } from "react";
import { useDropzone } from "react-dropzone";

const uploadEndpoint = "/api/upload";
const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

const TERMINAL_STATUSES = new Set(["done", "failed"]);

export default function Home() {
  const [status, setStatus] = useState<string>("Ready to upload your video.");
  const [jobId, setJobId] = useState<string>("");
  const [isLoading, setIsLoading] = useState(false);
  const pollRef = useRef<ReturnType<typeof setInterval> | null>(null);

  useEffect(() => {
    if (!jobId) return;

    pollRef.current = setInterval(async () => {
      try {
        const res = await fetch(`/api/jobs/${jobId}`);
        if (!res.ok) return;
        const job = await res.json();
        if (job.status === "done") {
          setStatus("Job complete! Your 3D Gaussian Splat is ready.");
        } else if (job.status === "failed") {
          setStatus(`Job failed: ${job.error_message || "unknown error"}`);
        } else {
          setStatus(`Processing… ${job.progress ?? 0}%`);
        }
        if (TERMINAL_STATUSES.has(job.status)) {
          clearInterval(pollRef.current!);
          pollRef.current = null;
        }
      } catch {
      }
    }, 3000);

    return () => {
      if (pollRef.current) clearInterval(pollRef.current);
    };
  }, [jobId]);

  const onDrop = useCallback(async (acceptedFiles: File[]) => {
    if (!acceptedFiles.length) {
      return;
    }

    setIsLoading(true);
    setStatus("Uploading video...");
    setJobId("");

    const formData = new FormData();
    formData.append("file", acceptedFiles[0]);

    try {
      const response = await fetch(uploadEndpoint, {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => null);
        const message = errorData?.detail || response.statusText || "Upload failed.";
        throw new Error(message);
      }

      const result = await response.json();
      setJobId(result.job_id);
      setStatus("Upload successful! Your job is queued.");
    } catch (error) {
      setStatus(`Upload failed: ${error instanceof Error ? error.message : "Unknown error."}`);
    } finally {
      setIsLoading(false);
    }
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      "video/*": [],
    },
    maxFiles: 1,
  });

  return (
    <main className="page-container">
      <section className="hero-card">
        <div className="hero-copy">
          <p className="eyebrow">splat3D</p>
          <h1>Upload a short video, generate a 3D Gaussian Splat.</h1>
          <p className="subtitle">
            Drag a video here or click to choose a file. The backend will create a processing job and return a job ID.
          </p>
        </div>

        <div className="upload-card">
          <div
            {...getRootProps()}
            className={`upload-zone ${isDragActive ? "upload-zone-active" : ""}`}
          >
            <input {...getInputProps()} />
            <p>{isDragActive ? "Drop it like it’s hot..." : "Drop a video here, or click to browse."}</p>
            <p className="hint">MP4, MOV, AVI and similar video formats are supported.</p>
          </div>

          <div className="status-panel">
            <p className="status-label">Status</p>
            <p className="status-text">{status}</p>
            {isLoading && <p className="status-note">Uploading now, please wait...</p>}
            {jobId && (
              <p className="status-note">
                Job ID: <code>{jobId}</code>
              </p>
            )}
          </div>
        </div>
      </section>

      <section className="info-card">
        <h2>Need help?</h2>
        <p>
          If you run this locally with Docker Compose, the backend is expected at{' '}
          <code>{apiUrl}</code>.
        </p>
        {jobId && (
          <p>
            Once the job is created, check status at{' '}
            <code>{apiUrl ? `${apiUrl}/api/jobs/${jobId}` : `/api/jobs/${jobId}`}</code>.
          </p>
        )}
      </section>
    </main>
  );
}

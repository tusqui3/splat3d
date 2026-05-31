export default function Home() {
  return (
    <main style={{ fontFamily: "system-ui, sans-serif", padding: "2rem" }}>
      <h1>splat3D</h1>
      <p>Upload a short video and generate a 3D Gaussian Splat.</p>
      <p>
        The backend is available at <code>{process.env.NEXT_PUBLIC_API_URL}</code>.
      </p>
    </main>
  );
}

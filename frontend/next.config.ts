import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  output: "standalone",
  transpilePackages: ["@mkkellogg/gaussian-splats-3d", "three"],
};

export default nextConfig;

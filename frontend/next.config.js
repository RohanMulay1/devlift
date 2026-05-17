/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  webpack: (config, { dev }) => {
    if (dev) {
      // Brave browser blocks eval() which Next.js uses for source maps in dev mode.
      // cheap-module-source-map gives similar DX without eval.
      config.devtool = 'cheap-module-source-map';
    }
    return config;
  },
};

module.exports = nextConfig;

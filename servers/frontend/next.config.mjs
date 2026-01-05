/** @type {import('next').NextConfig()} */

const NextConfig = {
    reactStrictMode: false,
    distDir: ".next-build",

    async rewrites() {
        return [
            {
                source: "/api/:path",
                destination: "http://localhost:8000/:path"
            }
        ]
    }
};

export default NextConfig;

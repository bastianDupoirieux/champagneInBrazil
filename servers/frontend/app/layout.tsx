import React from "react";
import localFont from "next/font/local";
import LayoutProvider from "./context/LayoutContext";
import Sidebar from "@/components/Sidebar";
import "./globals.css";

const inter = localFont({
    src: [
        {
            path: "./fonts/Inter.ttf",
            weight: "400",
            style: "normal",
        },
    ],
    variable: "--font-inter",
});

export default function RootLayout({
    children,
}: Readonly<{
    children: React.ReactNode;
}>) {
    return (
        <html lang="en">
            <body
                className={`${inter.variable} antialiased`}
            >
                <LayoutProvider>
                    <div className="layout-container">
                        <Sidebar />
                        <main className="main-content">
                            {children}
                        </main>
                    </div>
                </LayoutProvider>
            </body>
        </html>
    );
}

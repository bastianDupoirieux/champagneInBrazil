"use client";
import React from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { useLayout } from "@/app/context/LayoutContext";

const navigationItems = [
    { path: "/overview/cellar", label: "Cellar" },
    { path: "/overview/tasted", label: "Tasted Wines" },
    { path: "/overview/wishlist", label: "Wishlist" },
];

export default function Sidebar() {
    const pathname = usePathname();
    const { sidebarOpen, closeSidebar } = useLayout();

    const handleLinkClick = () => {
        // Close sidebar on mobile when a link is clicked
        if (window.innerWidth < 768) {
            closeSidebar();
        }
    };

    return (
        <>
            {/* Overlay for mobile */}
            {sidebarOpen && (
                <div
                    className="sidebar-overlay"
                    onClick={closeSidebar}
                    aria-hidden="true"
                />
            )}

            {/* Sidebar */}
            <aside
                className={`sidebar ${sidebarOpen ? "sidebar-open" : "sidebar-closed"}`}
            >
                <div className="sidebar-content">
                    <div className="sidebar-header">
                        <h2 className="sidebar-title">Wine Collection</h2>
                        <button
                            className="sidebar-close-button"
                            onClick={closeSidebar}
                            aria-label="Close sidebar"
                        >
                            ×
                        </button>
                    </div>

                    <nav className="sidebar-nav">
                        <ul className="sidebar-nav-list">
                            {navigationItems.map((item) => {
                                const isActive = pathname === item.path;
                                return (
                                    <li key={item.path} className="sidebar-nav-item">
                                        <Link
                                            href={item.path}
                                            className={`nav-link ${isActive ? "nav-link-active" : ""}`}
                                            onClick={handleLinkClick}
                                        >
                                            {item.label}
                                        </Link>
                                    </li>
                                );
                            })}
                        </ul>
                    </nav>
                </div>
            </aside>
        </>
    );
}


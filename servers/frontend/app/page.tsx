"use client";
import { useLayout } from "@/app/context/LayoutContext";

export default function Page() {
    const { toggleSidebar, sidebarOpen } = useLayout();
    
    return (
        <div style={{ padding: "2rem" }}>
            <h1>Wine Collection App</h1>
            <p>Sidebar is {sidebarOpen ? "open" : "closed"}</p>
            <button onClick={toggleSidebar}>
                {sidebarOpen ? "Close" : "Open"} Sidebar
            </button>
            <p>Click the navigation links in the sidebar to test routing.</p>
        </div>
    );
}
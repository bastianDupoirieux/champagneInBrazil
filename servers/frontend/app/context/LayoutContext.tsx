"use client";
import React, {
    createContext,
    useContext,
    useState,
    ReactNode,
} from "react";

interface LayoutContextType {
    sidebarOpen: boolean;
    currentSection: string | null;
    toggleSidebar: () => void;
    closeSidebar: () => void;
    setCurrentSection: (section: string) => void;
}

const LayoutContext = createContext<LayoutContextType | undefined>(undefined);

export default function LayoutProvider({ children }: { children: ReactNode }) {
    const [sidebarOpen, setSidebarOpen] = useState(false);
    const [currentSection, setCurrentSection] = useState<string | null>(null);

    const toggleSidebar = () => {
        setSidebarOpen((prev) => !prev);
    };

    const closeSidebar = () => {
        setSidebarOpen(false);
    };

    return (
        <LayoutContext.Provider
            value={{
                sidebarOpen,
                currentSection,
                toggleSidebar,
                closeSidebar,
                setCurrentSection,
            }}
        >
            {children}
        </LayoutContext.Provider>
    );
}

export function useLayout() {
    const context = useContext(LayoutContext);
    if (context === undefined) {
        throw new Error("useLayout must be used within a LayoutProvider");
    }
    return context;
}

"use client";

import type { Wine } from "@/types/wine";
import { WineListVCard } from "./wine-list-v-card";
import { Loader } from "../ui/loader";
import { Error } from "../ui/error";

interface WineListProps {
    wines?: Wine[];               // Array of wines to render (optional to allow loading state)
    loading?: boolean;            // Flag to show a loading placeholder
    error?: string | null;        // Error message to display when fetching fails
    title?: string;               // Optional section title (e.g., "Cellar", "Tasted Wines")
    emptyMessage?: string;        // Optional custom empty state message
}

/**
 * WineList
 *
 * Renders a list of wines using the WineListVCard component.
 * Handles loading, error, and empty states so parent pages stay simple.
 */
export default function WineList({
    wines = [],
    loading = false,
    error = null,
    title,
    emptyMessage = "No wines found.",
}: WineListProps) {

    const wineList = Array.isArray(wines) ? wines : []; //Ensures the element of wines given is an array
    // When data is loading, show a simple placeholder (can be replaced with skeleton UI).
    if (loading) {
        return <Loader message="Loading wines..." className ="wine-list-container"/>;
    }

    // If an error occurred, surface it to the user.
    if (error) {
        return <Error error={error} className="wine-list-container" />;
    }

    // No wines to show -> render empty state.
    if (wineList.length === 0) {
        return (
            <section className="wine-list-container">
                {title && <h2 className="wine-list-title">{title}</h2>}
                <p className="wine-list-status">{emptyMessage}</p>
            </section>
        );
    }

    // Happy path: render all wines as cards.
    return (
        <section className="wine-list-container">
            {title && <h2 className="wine-list-title">{title}</h2>}
            <div className="wine-list-grid">
                {wineList.map((wine) => (
                    <WineListVCard key={String(wine.id)} wine={wine} />
                ))}
            </div>
        </section>
    );
}


"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import WineDetails from "@/components/WineDetails/WineDetails";
import type { Wine } from "@/types/wine";
import { fetchWineDetails } from "@/services/api/wine-details";

export default function DetailsPage() {
    const params = useParams<{ wineId: string }>();
    const wineId = params?.wineId as string;

    const [wine, setWine] = useState<Wine | null>(null);
    const [loading, setLoading] = useState<boolean>(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        if (!wineId) {
            setError("No wine ID provided.");
            setLoading(false);
            return;
        }

        let isMounted = true;
        const load = async () => {
            setLoading(true);
            setError(null);
            try {
                const data = await fetchWineDetails(wineId);
                if (!isMounted) return;
                setWine(data);
            } catch (err) {
                if (!isMounted) return;
                setError(err instanceof Error ? err.message : "Failed to load wine details.");
            } finally {
                if (isMounted) setLoading(false);
            }
        };

        load();
        return () => {
            isMounted = false;
        };
    }, [wineId]);

    return (
        <div className="page-shell">
            <WineDetails
                wine={wine}
                loading={loading}
                error={error}
                emptyMessage="Wine not found."
            />
        </div>
    );
}

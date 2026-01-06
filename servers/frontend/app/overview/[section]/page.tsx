"use client";

import { useEffect, useMemo, useState } from "react";
import { useParams } from "next/navigation";
import WineList from "@/components/WineList";
import type { Wine } from "@/types/wine";
import {
    fetchWinesInCellar,
    fetchTastedWines,
    fetchWinesOnWishlist,
} from "@/services/api/wine-lists";
import { useLayout } from "@/app/context/LayoutContext";

type Section = "cellar" | "tasted" | "wishlist";

export default function OverviewPage() {
    const params = useParams<{ section: string }>();
    const section = (params?.section as Section) ?? "cellar";

    const { setCurrentSection } = useLayout();

    const [wines, setWines] = useState<Wine[]>([]);
    const [loading, setLoading] = useState<boolean>(true);
    const [error, setError] = useState<string | null>(null);

    const sectionConfig = useMemo(() => {
        const titleMap: Record<Section, string> = {
            cellar: "Cellar Wines (Current)",
            tasted: "Tasted Wines",
            wishlist: "Wishlist Wines",
        };

        const fetchers: Record<Section, () => Promise<Wine[]>> = {
            // Requirement: within "cellar" use only the "cellar/current" endpoint
            cellar: fetchWinesInCellar,
            tasted: fetchTastedWines,
            wishlist: fetchWinesOnWishlist,
        };

        return {
            title: titleMap[section] ?? "Wines",
            fetcher: fetchers[section] ?? fetchWinesInCellar,
        };
    }, [section]);
    
    useEffect(() => {
        setCurrentSection(section);
    }, [section, setCurrentSection]);

    useEffect(() => {
        let isMounted = true;
        const load = async () => {
            setLoading(true);
            setError(null);
            try {
                const data = await sectionConfig.fetcher();
                if (!isMounted) return;
                setWines(data);
            } catch (err) {
                if (!isMounted) return;
                setError(err instanceof Error ? err.message : "Failed to load wines.");
            } finally {
                if (isMounted) setLoading(false);
            }
        };

        load();
        return () => {
            isMounted = false;
        };
    }, [sectionConfig]);

useEffect(() => {
    let isMounted = true;
    
    const handleWineAdded = (event: CustomEvent) => {
        // Refetch wines when a wine is added
        const load = async () => {
            setLoading(true);
            setError(null);
            try {
                const data = await sectionConfig.fetcher();
                if (!isMounted) return; // Add this check
                setWines(data);
            } catch (err) {
                if (!isMounted) return; // Add this check
                setError(err instanceof Error ? err.message : "Failed to load wines.");
            } finally {
                if (isMounted) setLoading(false); // Add this check
            }
        };
        load();
    };

    window.addEventListener('wineAdded', handleWineAdded as EventListener);
    
    return () => {
        isMounted = false; // Add this cleanup
        window.removeEventListener('wineAdded', handleWineAdded as EventListener);
    };
}, [sectionConfig]);

    return (
        <div className="page-shell">
            <h1 className="page-title">{sectionConfig.title}</h1>
            <WineList
                wines={wines}
                loading={loading}
                error={error}
                title={sectionConfig.title}
                emptyMessage="No wines found."
            />
        </div>
    );
}

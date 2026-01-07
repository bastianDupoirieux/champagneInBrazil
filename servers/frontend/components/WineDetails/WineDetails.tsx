"use client";

import React from "react";
import type { Wine } from "@/types/wine";
import { WineDetailsTitle } from "./WineDetailTitle";
import { Loader } from "../ui/loader";
import { Error } from "../ui/error";

import { mapImageToColour } from "@/utils/colours";

interface WineDetailsProps {
    wine: Wine | null;
    loading?: boolean;
    error?: string | null;
    title?: string;
    emptyMessage?: string;
}

export default function WineDetails({
    wine = null,
    loading = false,
    error = null,
    title,
    emptyMessage = "No wine details found.",
}: WineDetailsProps) {
    if (loading) {
        return <Loader message="Loading wine details..." className="wine-list-container" />
    }

    if (error) {
        return <Error error={error} className="wine-list-container" />
    }

    if (!wine) {
        return (
            <section className="wine-details-container">
                {title && <h2 className="wine-details-title">{title}</h2>}
                <p className="wine-details-status">{emptyMessage}</p>
            </section>
        );
    }

    // Happy path: there is a wine and details can be rendered
    return (
        <section className="wine-details-container">
            <WineDetailsTitle name={wine.name} producer={wine.producer} vintage={wine.vintage} colour={wine.colour} imagePath={mapImageToColour(wine.colour)} />
        </section>
    )
}

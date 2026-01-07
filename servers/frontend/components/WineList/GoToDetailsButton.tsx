"use client";

import React from "react";
import { useRouter } from "next/navigation";

interface GoToDetailsButtonProps {
    wineId: string | number;
    className?: string;
}

export const GoToDetailsButton: React.FC<GoToDetailsButtonProps> = ({ wineId, className }) => {
    const router = useRouter();

    const handleClick = () => {
        router.push(`/wine/details/${wineId}`);
    };

    return (
        <button
            onClick={handleClick}
            className={`go-to-details-button ${className || ""}`}
            type="button"
        >
            View Details
        </button>
    );
}


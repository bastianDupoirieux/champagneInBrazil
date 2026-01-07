import React from "react";
import { normaliseColour } from "@/utils/colours";

interface WineDetailTitleProps {
    name: string;
    producer: string;
    vintage?: number;
    colour: string;
    imagePath: string;
}


function getWineColourClass(colour: string): string {
    const normalisedColour = normaliseColour(colour);
    const colourClassMap: Record<string, string> = {
        "red": "wine-detail-title-bg-red",
        "white": "wine-detail-title-bg-white",
        "rose": "wine-detail-title-bg-rose",
        "orange": "wine-detail-title-bg-orange",
        "sparkling": "wine-detail-title-bg-sparkling"
    };
    return colourClassMap[normalisedColour] || "wine-detail-title-bg-default";
}

export const WineDetailsTitle: React.FC<WineDetailTitleProps> = ({name, producer, vintage, colour, imagePath}) => {
    const bgColourClass = getWineColourClass(colour);
    
    return (
        <div className="wine-detail-title-container">
            <img 
                src={imagePath}
                alt={`${colour} wine bottle`}
                className="wine-detail-title-image"
            />
            <div className={`wine-detail-title-text ${bgColourClass}`}>
                <div className="wine-detail-title-name">
                    {name}
                    {vintage && <span className="wine-detail-title-vintage"> ({vintage})</span>}
                </div>
                <div className="wine-detail-title-producer">{producer}</div>
            </div>
        </div>
    );
}

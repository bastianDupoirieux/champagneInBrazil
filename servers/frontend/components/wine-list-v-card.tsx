//import React from 'react';
import React from 'react';
import type { Wine } from '../types/wine'

interface WineListVCardProps {
    wine: Wine;
}

function getBottleImagePath(colour: string): string {
    // Normalise colours
    const normalisedColour = colour
        .toLowerCase()
        .trim()
        .normalize("NFD")
        .replace(/[\u0300-\u036f]/g, '')
        .replace(/\s+/g, '-');

    const colourMap: Record<string, string> = {
        "red": "/red.svg",
        "white": "/white.svg",
        "rose": "/rose.svg",
        "orange": "/orange.svg",
        "sparkling": "/sparkling.svg"
    };

    return colourMap[normalisedColour] || "/bottle.svg";
}

export const WineListVCard: React.FC<WineListVCardProps> = ({ wine }) => {
    const bottleImagePath = getBottleImagePath(wine.colour)

    const vintageDisplay = wine.vintage ? (`${wine.vintage}`): '';

    return(
        <div className = "wine-list-v-card">
            <img 
                src = {bottleImagePath}
                alt={`${wine.colour} wine bottle`}
                className = "wine-bottle-image-v-card"
            />
            <div className="wine-info-v-card">
                <span className="wine-name-v-card">{wine.name}</span>
                <span className="wine-separator-v-card"> - </span>
                <span className="wine-producer-v-card">{wine.producer}</span>
                {vintageDisplay && (
                    <span className="wine-vintage-v-card">{vintageDisplay}</span>
                )}
            </div>
        </div>
    );
};

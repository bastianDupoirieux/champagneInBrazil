//import React from 'react';
import React from 'react';
import type { Wine } from '../../types/wine'
import { mapImageToColour } from '../../utils/colours';

interface WineListVCardProps {
    wine: Wine;
}

export const WineListVCard: React.FC<WineListVCardProps> = ({ wine }) => {
    const bottleImagePath = mapImageToColour(wine.colour)

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
                    <span className="wine-vintage-v-card">({vintageDisplay})</span>
                )}
            </div>
        </div>
    );
};

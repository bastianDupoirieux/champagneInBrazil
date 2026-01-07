import React from "react";

interface WineDetailBodyProps {
    region?: string;
    country?: string;
    appellation?: string;
    notes?: string;
    in_cellar: boolean;
    has_been_tasted: boolean;
    on_wishlist: boolean;
    date_bought?: string;
    price_bought?: number;
    quantity?: number;
}

export const WineDetailBody: React.FC<WineDetailBodyProps> = ({
    region,
    country,
    appellation,
    notes,
    in_cellar,
    has_been_tasted,
    on_wishlist,
    date_bought,
    price_bought,
    quantity
}) => {
    const formatDate = (dateString?: string): string => {
        if (!dateString) return "";
        try {
            const date = new Date(dateString);
            return date.toLocaleDateString();
        } catch {
            return dateString;
        }
    };

    const formatPrice = (price?: number): string => {
        if (price === undefined || price === null) return "";
        return `€${price.toFixed(2)}`;
    };

    return (
        <div className="wine-detail-body-container">
            <div className="wine-detail-body-checkboxes">
                <label className="wine-detail-body-checkbox-item">
                    <input
                        type="checkbox"
                        checked={in_cellar}
                        readOnly
                        className="add-wine-form-checkbox"
                    />
                    <span>In Cellar</span>
                </label>
                <label className="wine-detail-body-checkbox-item">
                    <input
                        type="checkbox"
                        checked={has_been_tasted}
                        readOnly
                        className="add-wine-form-checkbox"
                    />
                    <span>Has Been Tasted</span>
                </label>
                <label className="wine-detail-body-checkbox-item">
                    <input
                        type="checkbox"
                        checked={on_wishlist}
                        readOnly
                        className="add-wine-form-checkbox"
                    />
                    <span>On Wishlist</span>
                </label>
            </div>

            <div className="wine-detail-body-content">
                <div className="wine-detail-body-section">
                    <h3 className="wine-detail-body-section-title">Regional</h3>
                    <div className="wine-detail-body-section-content">
                        {appellation && (
                            <div className="wine-detail-body-field">
                                <span className="wine-detail-body-label">Appellation:</span>
                                <span className="wine-detail-body-value">{appellation}</span>
                            </div>
                        )}
                        {region && (
                            <div className="wine-detail-body-field">
                                <span className="wine-detail-body-label">Region:</span>
                                <span className="wine-detail-body-value">{region}</span>
                            </div>
                        )}
                        {country && (
                            <div className="wine-detail-body-field">
                                <span className="wine-detail-body-label">Country:</span>
                                <span className="wine-detail-body-value">{country}</span>
                            </div>
                        )}
                        {!appellation && !region && !country && (
                            <p className="wine-detail-body-empty">No regional information available.</p>
                        )}
                    </div>
                </div>

                <div className="wine-detail-body-section">
                    <h3 className="wine-detail-body-section-title">Notes</h3>
                    <div className="wine-detail-body-section-content">
                        {notes ? (
                            <p className="wine-detail-body-notes">{notes}</p>
                        ) : (
                            <p className="wine-detail-body-empty">No notes available.</p>
                        )}
                    </div>
                </div>

                <div className="wine-detail-body-section">
                    <h3 className="wine-detail-body-section-title">Analytics</h3>
                    <div className="wine-detail-body-section-content">
                        {date_bought && (
                            <div className="wine-detail-body-field">
                                <span className="wine-detail-body-label">Date Bought:</span>
                                <span className="wine-detail-body-value">{formatDate(date_bought)}</span>
                            </div>
                        )}
                        {price_bought !== undefined && price_bought !== null && (
                            <div className="wine-detail-body-field">
                                <span className="wine-detail-body-label">Price:</span>
                                <span className="wine-detail-body-value">{formatPrice(price_bought)}</span>
                            </div>
                        )}
                        {quantity !== undefined && quantity !== null && (
                            <div className="wine-detail-body-field">
                                <span className="wine-detail-body-label">Quantity:</span>
                                <span className="wine-detail-body-value">{quantity}</span>
                            </div>
                        )}
                        {!date_bought && price_bought === undefined && quantity === undefined && (
                            <p className="wine-detail-body-empty">No analytics available.</p>
                        )}
                    </div>
                </div>
            </div>
        </div>
    );
}
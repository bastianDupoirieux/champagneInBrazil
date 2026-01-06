"use client";

import React, { useState, FormEvent } from "react";
import { useLayout } from "@/app/context/LayoutContext";
import { postWineForm, type FormType, type WineFormPayload } from "@/services/api/add-wine";
import { defaultValueTupleByState } from "@/utils/defaultValuesBySection"

interface AddWineFormProps {
    onSuccess?: () => void;
    onCancel?: () => void;
}

const COLOUR_OPTIONS = ["red", "white", "rosé", "orange", "sparkling"] as const;

export default function AddWineForm({ onSuccess, onCancel }: AddWineFormProps) {
    const { currentSection } = useLayout();
    
    // Determine form type from current section, default to "cellar" if not set
    const formType: FormType = 
        (currentSection === "cellar" || currentSection === "tasted" || currentSection === "wishlist")
            ? currentSection
            : "cellar";

    const defaultVals = defaultValueTupleByState(currentSection)
    
    const [formData, setFormData] = useState<WineFormPayload>({
        name: "",
        producer: "",
        region: "",
        country: "",
        appellation: "",
        colour: "",
        vintage: undefined,
        notes: "",
        in_cellar: defaultVals[0],
        has_been_tasted: defaultVals[1],
        on_wishlist: defaultVals[2],
        date_bought: "",
        price_bought: undefined,
        quantity: undefined,
    });

    const [errors, setErrors] = useState<Partial<Record<keyof WineFormPayload, string>>>({});
    const [isSubmitting, setIsSubmitting] = useState(false);
    const [submitError, setSubmitError] = useState<string | null>(null);

    const validateForm = (): boolean => {
        const newErrors: Partial<Record<keyof WineFormPayload, string>> = {};

        if (!formData.name.trim()) {
            newErrors.name = "Name is required";
        }

        if (!formData.producer.trim()) {
            newErrors.producer = "Producer is required";
        }

        if (!formData.colour) {
            newErrors.colour = "Colour is required";
        }

        if (formData.vintage !== undefined && formData.vintage < 0) {
            newErrors.vintage = "Vintage must be a positive number";
        }

        if (formData.price_bought !== undefined && formData.price_bought < 0) {
            newErrors.price_bought = "Price must be a positive number";
        }

        if (formData.quantity !== undefined && formData.quantity < 1) {
            newErrors.quantity = "Quantity must be at least 1";
        }
        if (!formData.in_cellar && !formData.has_been_tasted && !formData.on_wishlist) {
            newErrors.in_cellar = "The status must be at least one of in_cellar, has_been_tasted and on_wishlist";
        }

        setErrors(newErrors);
        return Object.keys(newErrors).length === 0;
    };

    const handleChange = (
        e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>
    ) => {
        const { name, value, type } = e.target;
        const checked = (e.target as HTMLInputElement).checked;
        
        setFormData((prev) => {
            const newData: WineFormPayload = { ...prev };
            
            if (name === "vintage" || name === "price_bought" || name === "quantity") {
                (newData[name as "vintage" | "price_bought" | "quantity"]) = value === "" ? undefined : Number(value);
            } else if (name === "name" || name === "producer" || name === "colour") {
                (newData[name as "name" | "producer" | "colour"]) = value;
            } else if (name === "region" || name === "country" || name === "appellation" || name === "notes" || name === "date_bought") {
                (newData[name as "region" | "country" | "appellation" | "notes" | "date_bought"]) = value;
            } else if (name === "in_cellar" || name === "has_been_tasted" || name === "on_wishlist") {
                (newData[name as "in_cellar" | "has_been_tasted" | "on_wishlist"]) = checked;
            }
            
            return newData;
        });

        // Clear error for this field when user starts typing
        if (errors[name as keyof WineFormPayload]) {
            setErrors((prev) => {
                const newErrors = { ...prev };
                delete newErrors[name as keyof WineFormPayload];
                return newErrors;
            });
        }
    };

    const handleSubmit = async (e: FormEvent) => {
        e.preventDefault();
        setSubmitError(null);

        if (!validateForm()) {
            return;
        }

        setIsSubmitting(true);

        try {
            // Prepare payload, removing empty strings for optional fields
            const payload: WineFormPayload = {
                name: formData.name.trim(),
                producer: formData.producer.trim(),
                colour: formData.colour,
                region: formData.region?.trim() || undefined,
                country: formData.country?.trim() || undefined,
                appellation: formData.appellation?.trim() || undefined,
                vintage: formData.vintage,
                notes: formData.notes?.trim() || undefined,
                in_cellar: formData.in_cellar,
                has_been_tasted: formData.has_been_tasted,
                on_wishlist: formData.on_wishlist,
                date_bought: formData.date_bought || undefined,
                price_bought: formData.price_bought,
                quantity: formData.quantity,
            };

            await postWineForm(formType, payload);
            
            // Reset form on success
            setFormData({
                name: "",
                producer: "",
                region: "",
                country: "",
                appellation: "",
                colour: "",
                vintage: undefined,
                notes: "",
                in_cellar: defaultVals[0],
                has_been_tasted: defaultVals[1],
                on_wishlist: defaultVals[2],
                date_bought: "",
                price_bought: undefined,
                quantity: undefined,
            });

            window.dispatchEvent(new CustomEvent("wineAdded", { 
                detail: { formType }
            }));
            
            onSuccess?.();
        } catch (error) {
            setSubmitError(
                error instanceof Error 
                    ? error.message 
                    : "Failed to add wine. Please try again."
            );
        } finally {
            setIsSubmitting(false);
        }
    };

    return (
        <form onSubmit={handleSubmit} className="add-wine-form">
            <h2 className="add-wine-form-title">
                Add Wine to {formType.charAt(0).toUpperCase() + formType.slice(1)}
            </h2>

            {submitError && (
                <div className="wine-list-error add-wine-form-error">
                    {submitError}
                </div>
            )}

            <div className="add-wine-form-fields">
                {/* Required Fields */}
                <div className="add-wine-form-group">
                    <label htmlFor="in_cellar" className="add-wine-form-label">
                        In Cellar <span className="add-wine-form-required">*</span>
                        <input
                            type="checkbox"
                            id="in_cellar"
                            name="in_cellar"
                            checked={formData.in_cellar}
                            onChange={handleChange}
                            className="add-wine-form-checkbox"
                        />
                    </label>
                </div>
                <div className="add-wine-form-group">
                    <label htmlFor="has_been_tasted" className="add-wine-form-label">
                        Wine has been Tasted <span className="add-wine-form-required">*</span>
                        <input
                            type="checkbox"
                            id="has_been_tasted"
                            name="has_been_tasted"
                            checked={formData.has_been_tasted}
                            onChange={handleChange}
                            className="add-wine-form-checkbox"
                        />
                    </label>
                </div>
                <div className="add-wine-form-group">
                    <label htmlFor="on_wishlist" className="add-wine-form-label">
                        On Wishlist <span className="add-wine-form-required">*</span>
                        <input
                            type="checkbox"
                            id="on_wishlist"
                            name="on_wishlist"
                            checked={formData.on_wishlist}
                            onChange={handleChange}
                            className="add-wine-form-checkbox"
                        />
                    </label>
                </div>

                <div className="add-wine-form-group">
                    <label htmlFor="name" className="add-wine-form-label">
                        Name <span className="add-wine-form-required">*</span>
                    </label>
                    <input
                        type="text"
                        id="name"
                        name="name"
                        value={formData.name}
                        onChange={handleChange}
                        className={`add-wine-form-input ${errors.name ? "add-wine-form-input-error" : ""}`}
                        required
                    />
                    {errors.name && (
                        <span className="add-wine-form-field-error">{errors.name}</span>
                    )}
                </div>

                <div className="add-wine-form-group">
                    <label htmlFor="producer" className="add-wine-form-label">
                        Producer <span className="add-wine-form-required">*</span>
                    </label>
                    <input
                        type="text"
                        id="producer"
                        name="producer"
                        value={formData.producer}
                        onChange={handleChange}
                        className={`add-wine-form-input ${errors.producer ? "add-wine-form-input-error" : ""}`}
                        required
                    />
                    {errors.producer && (
                        <span className="add-wine-form-field-error">{errors.producer}</span>
                    )}
                </div>

                <div className="add-wine-form-group">
                    <label htmlFor="colour" className="add-wine-form-label">
                        Colour <span className="add-wine-form-required">*</span>
                    </label>
                    <select
                        id="colour"
                        name="colour"
                        value={formData.colour}
                        onChange={handleChange}
                        className={`add-wine-form-input add-wine-form-select ${errors.colour ? "add-wine-form-input-error" : ""}`}
                        required
                    >
                        <option value="">Select a colour</option>
                        {COLOUR_OPTIONS.map((colour) => (
                            <option key={colour} value={colour}>
                                {colour.charAt(0).toUpperCase() + colour.slice(1)}
                            </option>
                        ))}
                    </select>
                    {errors.colour && (
                        <span className="add-wine-form-field-error">{errors.colour}</span>
                    )}
                </div>

                {/* Optional Fields */}
                <div className="add-wine-form-group">
                    <label htmlFor="region" className="add-wine-form-label">Region</label>
                    <input
                        type="text"
                        id="region"
                        name="region"
                        value={formData.region}
                        onChange={handleChange}
                        className="add-wine-form-input"
                    />
                </div>

                <div className="add-wine-form-group">
                    <label htmlFor="country" className="add-wine-form-label">Country</label>
                    <input
                        type="text"
                        id="country"
                        name="country"
                        value={formData.country}
                        onChange={handleChange}
                        className="add-wine-form-input"
                    />
                </div>

                <div className="add-wine-form-group">
                    <label htmlFor="appellation" className="add-wine-form-label">Appellation</label>
                    <input
                        type="text"
                        id="appellation"
                        name="appellation"
                        value={formData.appellation}
                        onChange={handleChange}
                        className="add-wine-form-input"
                    />
                </div>

                <div className="add-wine-form-group">
                    <label htmlFor="vintage" className="add-wine-form-label">Vintage</label>
                    <input
                        type="number"
                        id="vintage"
                        name="vintage"
                        value={formData.vintage ?? ""}
                        onChange={handleChange}
                        className={`add-wine-form-input ${errors.vintage ? "add-wine-form-input-error" : ""}`}
                        min="0"
                    />
                    {errors.vintage && (
                        <span className="add-wine-form-field-error">{errors.vintage}</span>
                    )}
                </div>

                <div className="add-wine-form-group">
                    <label htmlFor="date_bought" className="add-wine-form-label">Date Bought</label>
                    <input
                        type="date"
                        id="date_bought"
                        name="date_bought"
                        value={formData.date_bought}
                        onChange={handleChange}
                        className="add-wine-form-input"
                    />
                </div>

                <div className="add-wine-form-group">
                    <label htmlFor="price_bought" className="add-wine-form-label">Price Bought</label>
                    <input
                        type="number"
                        id="price_bought"
                        name="price_bought"
                        value={formData.price_bought ?? ""}
                        onChange={handleChange}
                        className={`add-wine-form-input ${errors.price_bought ? "add-wine-form-input-error" : ""}`}
                        min="0"
                        step="0.01"
                    />
                    {errors.price_bought && (
                        <span className="add-wine-form-field-error">{errors.price_bought}</span>
                    )}
                </div>

                <div className="add-wine-form-group">
                    <label htmlFor="quantity" className="add-wine-form-label">Quantity</label>
                    <input
                        type="number"
                        id="quantity"
                        name="quantity"
                        value={formData.quantity ?? ""}
                        onChange={handleChange}
                        className={`add-wine-form-input ${errors.quantity ? "add-wine-form-input-error" : ""}`}
                        min="1"
                    />
                    {errors.quantity && (
                        <span className="add-wine-form-field-error">{errors.quantity}</span>
                    )}
                </div>

                <div className="add-wine-form-group">
                    <label htmlFor="notes" className="add-wine-form-label">Notes</label>
                    <textarea
                        id="notes"
                        name="notes"
                        value={formData.notes}
                        onChange={handleChange}
                        className="add-wine-form-input add-wine-form-textarea"
                        rows={4}
                    />
                </div>
            </div>

            <div className="add-wine-form-actions">
                {onCancel && (
                    <button
                        type="button"
                        onClick={onCancel}
                        className="add-wine-form-button add-wine-form-button-secondary"
                        disabled={isSubmitting}
                    >
                        Cancel
                    </button>
                )}
                <button
                    type="submit"
                    className="add-wine-form-button add-wine-form-button-primary"
                    disabled={isSubmitting}
                >
                    {isSubmitting ? "Adding..." : "Add Wine"}
                </button>
            </div>
        </form>
    );
}


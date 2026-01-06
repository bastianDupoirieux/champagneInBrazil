"use client";

import React, { useEffect } from "react";
import AddWineForm from "./AddWineForm";

interface AddWineModalProps {
    isOpen: boolean;
    onClose: () => void;
}

export default function AddWineModal({ isOpen, onClose }: AddWineModalProps) {
    // Close modal on Escape key press
    useEffect(() => {
        const handleEscape = (e: KeyboardEvent) => {
            if (e.key === "Escape" && isOpen) {
                onClose();
            }
        };

        if (isOpen) {
            document.addEventListener("keydown", handleEscape);
            // Prevent body scroll when modal is open
            document.body.style.overflow = "hidden";
        }

        return () => {
            document.removeEventListener("keydown", handleEscape);
            document.body.style.overflow = "unset";
        };
    }, [isOpen, onClose]);

    if (!isOpen) {
        return null;
    }

    const handleBackdropClick = (e: React.MouseEvent<HTMLDivElement>) => {
        // Only close if clicking the backdrop itself, not the modal content
        if (e.target === e.currentTarget) {
            onClose();
        }
    };

    const handleSuccess = () => {
        onClose();
    };

    return (
        <div className="add-wine-modal-overlay" onClick={handleBackdropClick}>
            <div className="add-wine-modal-container">
                <button
                    className="add-wine-modal-close"
                    onClick={onClose}
                    aria-label="Close modal"
                >
                    ×
                </button>
                <AddWineForm onSuccess={handleSuccess} onCancel={onClose} />
            </div>
        </div>
    );
}

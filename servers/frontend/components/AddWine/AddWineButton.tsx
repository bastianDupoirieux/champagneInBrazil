"use client";

import React, { useState } from "react";
import AddWineModal from "./AddWineModal";

export default function AddWineButton() {
    const [isModalOpen, setIsModalOpen] = useState(false);

    const handleOpenModal = () => {
        setIsModalOpen(true);
    };

    const handleCloseModal = () => {
        setIsModalOpen(false);
    };

    return (
        <>
            <button
                className="add-wine-button"
                onClick={handleOpenModal}
                aria-label="Add wine"
            >
                +
            </button>
            <AddWineModal isOpen={isModalOpen} onClose={handleCloseModal} />
        </>
    );
}


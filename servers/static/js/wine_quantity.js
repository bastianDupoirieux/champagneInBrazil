document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll('.wine-quantity').forEach(container => {
        const input = container.querySelector('.qty-input');
        const wineId = container.dataset.wineId;

        const updateQuantity = (newQty) => {
            // Send AJAX request to server
            fetch(`/update_quantity/${wineId}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCSRFToken() // optional if using CSRF protection
                },
                body: JSON.stringify({ quantity: newQty })
            })
            .then(res => res.json())
            .then(data => {
                if (!data.success) {
                    alert("Failed to update quantity");
                    input.value = data.quantity || 0; // revert if failed
                }
            })
            .catch(() => {
                alert("Error updating quantity");
            });
        };

        // Listen for any change to the input (typing or native increment/decrement)
        input.addEventListener('change', () => {
            let val = parseInt(input.value);
            if (isNaN(val) || val < 0) val = 0;
            input.value = val; // ensure input is valid
            updateQuantity(val);
        });
    });
});

// Optional helper for CSRF
function getCSRFToken() {
    const tokenMeta = document.querySelector('meta[name=csrf-token]');
    return tokenMeta ? tokenMeta.content : '';
}

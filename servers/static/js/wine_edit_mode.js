
document.querySelectorAll('.field-container').forEach(container => {
  const span = container.querySelector('.field-value');
  const input = container.querySelector('.field-input');
  const button = container.querySelector('.edit-field-btn');

  // Function to enter edit mode
  const enterEditMode = () => {
    span.style.display = 'none';
    input.style.display = 'block';
    input.focus();
    input.select(); // Optional: select existing text
  };

  // Function to exit edit mode
  const exitEditMode = () => {
    span.textContent = input.value;
    span.style.display = 'inline';
    input.style.display = 'none';
  };

  // --- Trigger edit mode ---
  button.addEventListener('click', enterEditMode);
  span.addEventListener('click', enterEditMode);

  // --- Exit edit mode on blur (losing focus) ---
  input.addEventListener('blur', exitEditMode);

  // --- Optionally exit edit mode with Enter key ---
  input.addEventListener('keydown', e => {
    if (e.key === 'Enter') {
      exitEditMode();
    }
  });
});


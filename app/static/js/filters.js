(() => {
  const categoryFilter = document.getElementById("filter-categoria");
  const frequencyFilters = Array.from(document.querySelectorAll("input[name='frequencia']"));
  const clearButton = document.getElementById("clear-filters");
  const clearEmptyButton = document.getElementById("clear-filters-empty");
  const emptyFilterState = document.getElementById("filter-empty-state");
  const rows = Array.from(document.querySelectorAll("[data-subscription-row]"));

  if (!categoryFilter || !clearButton) {
    return;
  }

  const selectedFrequency = () => {
    const selected = frequencyFilters.find((input) => input.checked);
    return selected ? selected.value : "";
  };

  const applyFilters = () => {
    const selectedCategory = categoryFilter.value;
    const selectedFrequencyValue = selectedFrequency();
    let visibleCount = 0;

    rows.forEach((row) => {
      const matchesCategory = !selectedCategory || row.dataset.categoria === selectedCategory;
      const matchesFrequency = !selectedFrequencyValue || row.dataset.frequencia === selectedFrequencyValue;
      const isVisible = matchesCategory && matchesFrequency;

      row.classList.toggle("d-none", !isVisible);
      if (isVisible) {
        visibleCount += 1;
      }
    });

    if (emptyFilterState) {
      emptyFilterState.classList.toggle("d-none", visibleCount > 0);
    }
  };

  const clearFilters = () => {
    categoryFilter.value = "";
    const allFrequency = frequencyFilters.find((input) => input.value === "");
    if (allFrequency) {
      allFrequency.checked = true;
    }
    applyFilters();
  };

  document.querySelectorAll("[data-confirm-message]").forEach((form) => {
    form.addEventListener("submit", (event) => {
      if (!window.confirm(form.dataset.confirmMessage)) {
        event.preventDefault();
      }
    });
  });

  categoryFilter.addEventListener("change", applyFilters);
  frequencyFilters.forEach((input) => input.addEventListener("change", applyFilters));
  clearButton.addEventListener("click", clearFilters);
  if (clearEmptyButton) {
    clearEmptyButton.addEventListener("click", clearFilters);
  }
})();

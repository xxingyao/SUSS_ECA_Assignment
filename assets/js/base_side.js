document.addEventListener('DOMContentLoaded', function() {
  const selectElement = document.getElementById('bookingDropdown');
  const currentPath = window.location.pathname;
  const matchingOption = Array.from(selectElement.options)
                              .find(option => option.value === currentPath);
  if (matchingOption) {
    matchingOption.selected = true;
  } else {
    const placeholderOption = Array.from(selectElement.options)
                                   .find(option => option.value === "");
    if (placeholderOption) {
      placeholderOption.selected = true;
    }
  }
});
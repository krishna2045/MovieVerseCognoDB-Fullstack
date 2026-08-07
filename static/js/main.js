// main.js – handles global UI helpers like spinner and empty state

// Show spinner overlay
function showSpinner() {
  const overlay = document.createElement('div');
  overlay.className = 'spinner-overlay';
  overlay.id = 'global-spinner';
  overlay.innerHTML = `<div class="spinner-border text-light" role="status"><span class="visually-hidden">Loading...</span></div>`;
  document.body.appendChild(overlay);
}

// Hide spinner overlay
function hideSpinner() {
  const overlay = document.getElementById('global-spinner');
  if (overlay) overlay.remove();
}

// Show empty state inside a container
function showEmptyState(containerSelector, message = 'No results found.', imgUrl = null) {
  const container = document.querySelector(containerSelector);
  if (!container) return;
  container.innerHTML = `
    <div class="empty-state">
      ${imgUrl ? `<img src="${imgUrl}" alt="Empty"/>` : ''}
      <p>${message}</p>
    </div>`;
}

// Example usage on page load for static content – can be called from each page as needed
document.addEventListener('DOMContentLoaded', () => {
  // hide spinner if page loaded
  hideSpinner();
});

document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('search-input');
    const participantRows = document.querySelectorAll('#participants-table tbody tr');

    searchInput.addEventListener('input', function() {
        const searchTerm = searchInput.value.trim().toLocaleLowerCase();

        participantRows.forEach(function(row) {
            const participantName = row.dataset.name.toLocaleLowerCase();
            row.hidden = !participantName.includes(searchTerm);
        });
    });
});
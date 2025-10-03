document.addEventListener('DOMContentLoaded', function() {
    const searchBar = document.getElementById('searchBar');
    const tableBody = document.getElementById('table-body');
  
    
    fetch('/api/data')
      .then(response => response.json())
      .then(data => {
        
        updateTable(data);
  
        searchBar.addEventListener('input', function() {
          const searchTerm = searchBar.value.toLowerCase();
          const filteredData = data.filter(item => 
            item.name.toLowerCase().includes(searchTerm)
          );
          updateTable(filteredData);
        });
      });
  
    function updateTable(data) {
      tableBody.innerHTML = '';
      data.forEach(item => {
        const row = `
          <tr>
            <td>${item.name}</td>
            <td>${item.redemptionStatus}</td>
            <td>${item.cloudProfile}</td>
            <td>${item.completion}</td>
            <td>${item.chapterCompleted}</td>
            <td>${item.arcadeCompleted}</td>
            <td>${item.arcadeStatus}</td>
          </tr>
        `;
        tableBody.innerHTML += row;
      });
    }
  });
  
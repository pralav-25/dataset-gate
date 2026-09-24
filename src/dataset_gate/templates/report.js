(() => {
  const search = document.getElementById('rule-search');
  const status = document.getElementById('result-filter');
  const rows = [...document.querySelectorAll('tbody tr')];
  const counter = document.getElementById('visible-count');
  const empty = document.getElementById('empty-state');
  const table = document.getElementById('results-table');
  function filter() {
    const query = search.value.trim().toLocaleLowerCase();
    let count = 0;
    for (const row of rows) {
      row.hidden = !(row.textContent.toLocaleLowerCase().includes(query) &&
        (status.value === 'all' || row.dataset.status === status.value));
      if (!row.hidden) count++;
    }
    counter.textContent = `${count} of ${rows.length} checks shown`;
    empty.hidden = count !== 0;
    table.hidden = count === 0;
  }
  search.addEventListener('input', filter);
  status.addEventListener('change', filter);
  document.getElementById('clear-filters').addEventListener('click', () => {
    search.value = '';
    status.value = 'all';
    filter();
    search.focus();
  });
  document.getElementById('print-report').addEventListener('click', () => window.print());
  filter();
})();

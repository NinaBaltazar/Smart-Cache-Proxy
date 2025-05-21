document.addEventListener('DOMContentLoaded', function () {
    const ctx = document.getElementById('cacheChart').getContext('2d');
    const total = cacheHits + cacheMisses;
    const data = total > 0 ? [cacheHits, cacheMisses] : [1, 0];
  
    new Chart(ctx, {
      type: 'bar',
      data: {
        labels: ['Cache Hits', 'Cache Misses'],
        datasets: [{
          label: 'Quantidade',
          data: data,
          backgroundColor: ['#d63384', '#faa2c1'],
          borderWidth: 1
        }]
      },
      options: {
        indexAxis: 'y',
        responsive: true,
        plugins: {
          legend: { display: false },
          tooltip: {
            callbacks: {
              label: function (context) {
                if (total === 0) return 'Nenhum dado ainda';
                return `${context.label}: ${context.raw}`;
              }
            }
          }
        },
        scales: {
          x: {
            beginAtZero: true,
            ticks: { precision: 0 }
          }
        }
      }
    });
  });
  
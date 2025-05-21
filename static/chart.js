document.addEventListener('DOMContentLoaded', function () {
    const ctx = document.getElementById('cacheChart').getContext('2d');
    const total = cacheHits + cacheMisses;
    const data = total > 0 ? [cacheHits, cacheMisses] : [1, 0];
    const labels = ['Cache Hits', 'Cache Misses'];
  
    new Chart(ctx, {
      type: 'bar',
      data: {
        labels: labels,
        datasets: [{
          label: 'Requisições',
          data: data,
          backgroundColor: ['#d63384', '#faa2c1'],
          borderRadius: 10,
          hoverBackgroundColor: ['#c22567', '#f8a2be']
        }]
      },
      options: {
        indexAxis: 'y',
        responsive: true,
        animation: {
          duration: 800,
          easing: 'easeOutQuart'
        },
        plugins: {
          legend: {
            display: false
          },
          tooltip: {
            backgroundColor: '#fff0f6',
            titleColor: '#d63384',
            bodyColor: '#333',
            borderColor: '#f783ac',
            borderWidth: 1,
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
            ticks: { precision: 0 },
            grid: { display: false }
          },
          y: {
            grid: { display: false }
          }
        }
      }
    });
  });
  
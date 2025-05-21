const ctx = document.getElementById('cacheChart').getContext('2d');
new Chart(ctx, {
  type: 'pie',
  data: {
    labels: ['Cache Hits', 'Cache Misses'],
    datasets: [{
      label: 'Cache Stats',
      data: [cacheHits, cacheMisses],
      borderWidth: 1
    }]
  }
});
document.addEventListener("DOMContentLoaded", () => {
  loadStatusChart();
  loadMonthlyChart();

  document.getElementById("filterType")?.addEventListener("change", updateMonthlyChart);
  document.getElementById("filterSeason")?.addEventListener("change", updateMonthlyChart);
  document.getElementById("filterMonth")?.addEventListener("change", updateMonthlyChart);
});

function loadStatusChart() {
  const ctx = document.getElementById("statusBreakdownChart");
  if (!ctx) return;

  const chart = new Chart(ctx, {
    type: "doughnut",
    data: {
      labels: ["Pending", "Confirmed", "Cancelled"],
      datasets: [{
        label: "Booking Status",
        data: window.statusData || [10, 25, 5],
        backgroundColor: ["#ffc107", "#28a745", "#dc3545"]
      }]
    },
    options: {
      responsive: true,
      plugins: {
        legend: { position: "bottom" }
      }
    }
  });
}

let monthlyChart;
function loadMonthlyChart(filterData = null) {
  const ctx = document.getElementById("monthlyBookingChart");
  if (!ctx) return;

  const data = filterData || window.monthlyData || {
    labels: ["Jan", "Feb", "Mar", "Apr"],
    datasets: [{
      label: "Bookings",
      data: [20, 30, 15, 25],
      backgroundColor: "#17a2b8"
    }]
  };

  monthlyChart = new Chart(ctx, {
    type: "bar",
    data: data,
    options: {
      responsive: true,
      scales: { y: { beginAtZero: true } }
    }
  });
}

function updateMonthlyChart() {
  const month = document.getElementById("filterMonth")?.value;
  const season = document.getElementById("filterSeason")?.value;
  const type = document.getElementById("filterType")?.value;

  // Example mock filter logic
  const filteredLabels = ["Jun", "Jul", "Aug"];
  const filteredData = [35, 40, 30];

  const newData = {
    labels: filteredLabels,
    datasets: [{
      label: `${season || "Monthly"} Bookings`,
      data: filteredData,
      backgroundColor: "#007bff"
    }]
  };

  monthlyChart.destroy();
  loadMonthlyChart(newData);
}
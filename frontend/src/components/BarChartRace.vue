<template>
  <div>
    <div id="chart-container" style="width: 100%; height: 600px"></div>
    <div style="text-align: center; margin-top: 10px">
      <button @click="togglePlay" class="play-pause-btn">
        {{ isPlaying ? "Pause" : "Play" }}
      </button>
      <button @click="resetChart" class="reset-btn">Reset</button>
    </div>
  </div>
</template>

<script>
import Highcharts from "highcharts";

export default {
  data() {
    return {
      chart: null,
      dataset: [],
      currentYear: 2016,
      startYear: 2016,
      endYear: 2022,
      isPlaying: false,
      timer: null,
    };
  },
  mounted() {
    this.fetchData().then(() => {
      this.createChart();
    });
  },
  methods: {
    async fetchData() {
      const response = await fetch("http://127.0.0.1:8000/data/");
      const data = await response.json();

      // Format data menjadi objek berdasarkan tahun
      this.dataset = data.reduce((acc, item) => {
        if (!acc[item.tahun]) {
          acc[item.tahun] = [];
        }
        acc[item.tahun].push({
          name: item.bps_nama_kecamatan,
          y: item.total_kasus,
        });
        return acc;
      }, {});
    },
    getData(year) {
      return this.dataset[year] || [];
    },
    createChart() {
      this.chart = Highcharts.chart("chart-container", {
        chart: {
          type: "bar",
          animation: {
            duration: 500,
          },
        },
        title: {
          text: "Kasus per Kecamatan Berdasarkan Tahun",
        },
        subtitle: {
          text: `Tahun: ${this.currentYear}`,
        },
        xAxis: {
          type: "category",
        },
        yAxis: {
          title: {
            text: "Total Kasus",
          },
        },
        plotOptions: {
          series: {
            dataSorting: {
              enabled: true,
            },
            dataLabels: {
              enabled: true,
            },
          },
        },
        series: [
          {
            name: `Tahun ${this.currentYear}`,
            data: this.getData(this.currentYear),
            colorByPoint: true,
          },
        ],
      });
    },
    updateChart() {
      if (this.chart) {
        this.chart.update({
          subtitle: {
            text: `Tahun: ${this.currentYear}`,
          },
          series: [
            {
              name: `Tahun ${this.currentYear}`,
              data: this.getData(this.currentYear),
            },
          ],
        });
      }
    },
    playAnimation() {
      this.timer = setInterval(() => {
        if (this.currentYear >= this.endYear) {
          this.pauseAnimation();
        } else {
          this.currentYear++;
          this.updateChart();
        }
      }, 1000);
    },
    pauseAnimation() {
      clearInterval(this.timer);
      this.timer = null;
      this.isPlaying = false;
    },
    togglePlay() {
      if (this.isPlaying) {
        this.pauseAnimation();
      } else {
        this.isPlaying = true;
        this.playAnimation();
      }
    },
    resetChart() {
      this.pauseAnimation(); // Hentikan animasi
      this.currentYear = this.startYear; // Reset tahun ke awal

      // Hancurkan chart lama
      if (this.chart) {
        this.chart.destroy();
      }

      // Buat ulang chart dengan tahun awal
      this.createChart();
    },
  },
};
</script>

<style>
.play-pause-btn,
.reset-btn {
  background-color: #007bff;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  margin: 0 5px;
}
.play-pause-btn:hover,
.reset-btn:hover {
  background-color: #0056b3;
}
</style>

<template>
  <div id="app">
    <h1>Highcharts Bar Chart Race</h1>
    <BarRaceChart />
  </div>
</template>

<script>
import BarRaceChart from "./BarChartRace.vue";

export default {
  name: "App",
  components: {
    BarRaceChart,
  },
};
</script>

<style>
#app {
  text-align: center;
}
</style>

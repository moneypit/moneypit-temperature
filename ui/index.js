new Vue({
  el: '#mp-fan-controller',
  data: {
    device: '',
    location: '',
    temps: [],
    temp_last_updated: ''
  },

  created () {
    var vm = this;

    axios.get('./api/config')
    .then(function (response) {
      vm.device = response.data.device;
      vm.location = response.data.location;
    })

    axios.get('./api/temperature')
    .then(function (response) {
      // need to loop
      .forEach(function (temp) {

      })
      vm.temps = response.data.temperature;
      vm.temp_last_updated = response.data.timestamp;
    })


  }
})

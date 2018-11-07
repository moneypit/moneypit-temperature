new Vue({
  el: '#mp-temperature',
  data: {
    device: '',
    location: '',
    rack_supply_temp_F: '',
    rack_exhaust_temp_F: '',
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
      vm.rack_supply_temp_F = Math.round(response['data']['rack-supply']['temperatureF'] * 100) / 100;
      vm.rack_exhaust_temp_F = Math.round(response['data']['rack-exhaust']['temperatureF'] * 100) / 100;
      vm.temp_last_updated = response['data']['timestamp'];
    })


  }
})

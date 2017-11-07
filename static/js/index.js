

const Search = {
  name: "searchbox",
  delimiters: ["((", "))"],
  template: '#search_template',
  data: function(){
    return {
      keyword: '',
      results: {},
      searching: false
    }
  },
  watch: {
    keyword: function(keyword){
      if (keyword !== '') {
        this.getResults(keyword);
      }else {
        this.searching = false;
      }
    }
  },
  methods: {
    getResults: function(keyword){
      var vm = this;
      vm.searching = true;
      var url = 'http://'+location.host+"/api/search?title="+keyword;

      axios.get(url)
          .then(function (response) {
            vm.results = response
          })
          .catch(function (error) {
            vm.results = 'Error! Could not reach the API. ' + error
          })

    }

  }
}

const Results = { template: '#results_template' }

const Detail = {
  name: "detail",
  delimiters: ["((", "))"],
  template: '#detail_template',
  data: function(){
    return {
      data: {},
      title: this.$route.params.title
    }
  },
  created: function(){
    var vm = this;
    var url = 'http://'+location.host+"/comic/"+vm.title;

    axios.get(url)
        .then(function (response) {
          vm.data = response.data;
        })
        .catch(function (error) {
          vm.data = 'Error! Could not reach the API. ' + error
        })
  }
 }

const Trend = {
  name: "trendchart",
  delimiters: ["((", "))"],
  template: '#trend_template',
  data: function(){
    return {
      data: {},
      genre: this.$route.params.genre
    }
  },
  created: function(){
    var vm = this;
    var url = 'http://'+location.host+"/api/trend/genre/"+vm.genre;

    axios.get(url)
        .then(function (response) {
          vm.data = response.data;
          var chart = c3.generate({
              bindto: '#chart',
              data: vm.data
          });
        })
        .catch(function (error) {
          vm.data = 'Error! Could not reach the API. ' + error
        })
  }
 }

const Network = {
  name: "network",
  delimiters: ["((", "))"],
  template: '#network_template',
  data: function(){
    return {
      data: {}//,
      // genre: this.$route.params.title
    }
  },
  created: function(){
    var vm = this;
    var url = 'http://'+location.host+"/api/network_graph";

    // 領域の確定
    var svg = d3.select('svg');
        // width = svg.attr("width": $('#network_graph').width(); ),
        // height = svg.attr("height": $('#network_graph').height(); );

    d3.json(url, function(error, graph) {

      vm.data = graph;


    });

  }
 }

const routes = [
  { path: '/', component: Search },
  { path: '/search/:word', component: Results ,params: true },
  { path: '/trend/:genre', component: Trend ,params: true  },
  { path: '/network', component: Network ,params: true  },
  { path: '/comic/:title', component: Detail ,params: true }
]

const router = new VueRouter({
  mode: 'history',
  routes // `routes: routes` の短縮表記
})

var app = new Vue({
  router,
  delimiters: ["((", "))"],
  data(){
    return{
      // test: "this is the test string!"
    }
  }
}).$mount('#app')

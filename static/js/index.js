

const Search = {
  name: "searchbox",
  delimiters: ["((", "))"],
  template: '#search_template',
  data: function(){
    return {
      keyword: '',
      results: {},
      themes: [],
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
      var url = '//'+location.host+"/api/search?title="+keyword;

      axios.get(url)
          .then(function (response) {
            vm.results = response
          })
          .catch(function (error) {
            vm.results = 'Error! Could not reach the API. ' + error
          })

    },
    getThemes: function(){
      var vm = this;
      var url = '//'+location.host+"/api/themes";
      axios.get(url)
        .then(function (response) {
          vm.themes = response
        })
        .catch(function (error) {
          vm.themes = 'Error! Could not reach the API. ' + error
        })
    }
  },
  created: function(){
    this.getThemes();
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
  watch: {
    '$route' (to, from) {
      this.getdata();
    }
  },
  methods: {
    getdata: function(){
      var vm = this;
      var url = '//'+location.host+"/api/comic/"+vm.title;

      axios.get(url)
          .then(function (response) {
            vm.data = response.data;
          })
          .catch(function (error) {
            vm.data = 'Error! Could not reach the API. ' + error
          })
    }
  },
  created: function(){
    this.getdata();
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
    var url = '//'+location.host+"/api/trend/genre/"+vm.genre;

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


Vue.component('back-button', {
  name: "backButton",
  template: "<a class='back' v-on:click='this.$route.router.go(-1)'>戻る</a>"
})

Vue.component('network-graph', {
  name: "network",
  delimiters: ["((", "))"],
  template: '#network_template',
  data: function(){
    return {
      data: {}
    }
  },
  created: function(){
    var url = '//'+location.host+"/api/network_graph";
    forceLayout.config = {
      width: 600,
      // width: $("#network_graph").width(),
      height: 600,
      jsonURI: url
    };
    forceLayout.start();
  }
 })

const routes = [
  { path: '/', component: Search },
  { path: '/search/:word', component: Results ,params: true },
  { path: '/trend/:genre', component: Trend ,params: true  },
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

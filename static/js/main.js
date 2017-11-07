
var app;

app = {

  getJson: function (arg) {

    var _path,
        _result;

    switch (arg.type) {
      case "genre":
        _path = "/api/trend/genre/"+arg.key;
        break;

      case "search_theme":
        var _query = this._makeQueryString("theme",arg.keys)
        _path = "/api/search?theme="+_query;
        break;

      case "search_title":
        _path = "/api/search?title="+arg.key;
        break;

      case "comic":
        _path = "/comic/"+arg.key;
        break;

      case "nwg":
        _path = "/api/network_graph";
        break;

      default:
        return false;
        break;
    }

    var result = $.ajax({
          url:'http://'+location.host+_path,
          type:'GET',
          dataType: "json",
      })//.done(function(data){
      //   console.log(data);
      //   return data;
      // });

      return result;
  },


  // 配列からURLクエリを作成する
  _makeQueryString: function (key,values) {
    var _query = "?";
    $.each(values,function(index,val){
        if (index !== 0) {
          _query += "&";
        }
        _query += key+"="+val;
    });
    return _query;
  },


  makeLineChart: function(obj){
    var chart = c3.generate({
        bindto: '#chart',
        data: obj
    });
  }
}

// app.getJson({
//   type: "genre",
//   key: "少年漫画"
// }).done(function(data){
//   app.makeLineChart(data);
// });

// app.getJson({
//   type: "search_title",
//   key: "最強"
// }).done(function(data){
//   var $container = $('#search_results');
//   data.forEach(function(value){
//     var href = '/comic/'+value;
//     $container.append('<li class="search_result"><a href='+href+'>'+value+'</li>');
//   });
// });
//
// app.getJson({
//   type: "comic",
//   key: "ベルサイユのばら"
// }).done(function(data){
//   var $container = $('#details');
//   $.each(data,function(i,elm){
//     if (!elm||elm=="") {
//       return true;
//     }
//     $container.append("<tr><th scope='row'>"+i+"</th><td>"+elm+"</td></tr>");
//   });
// });

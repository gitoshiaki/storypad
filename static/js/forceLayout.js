var forceLayout = {

  // 設定
  config: {

    width: 800,
    height: 800,
    jsonURI: "data.json"

  },

  // データ
  data: {},
  nodes: [],
  links: [],

  // d3
  nodeWeightScale: {},
  forceLayout: {},
  svg: {},

  //セレクション
  linkSelection: {},
  nodeSelection: {},
  labelSelection: {},

  start: function(){

    var self = this;
    this.getJson()
    .then(function(){

      self.makeNodes();
      self.makeLinks();
      self.makeScale();
      self.startLayout();
      self.svgSelection();
      self.renderLink();
      self.renderNode();
      self.renderLabel();
      self.startTick();

    },function(){

      console.log('エラー')

    });
  },

  // プロミスを返す
  getJson: function(){

    var self = this;
    var d = new $.Deferred;
    d3.json(this.config.jsonURI, function(error, data){
      if (error) { d.reject('Error!!'); }
      self.data = data;
      d.resolve();
    });
    return d.promise();

  },

  // 取得したデータからノードデータを整形して格納
  makeNodes: function(){

    var self = this;
    this.data.node.forEach(function(v,i,a){
        var node = {
          id: v.theme_id,
          label: v.theme_name,
          weight: v.count
        };
        self.nodes.push(node);
      });

  },

  // 取得したデータからリンクデータを整形して格納
  makeLinks: function(){

    var self = this;
    this.data.edge.forEach(function(v,i,a){
      var link = {
        source: v.combination[0]-1,
        target: v.combination[1]-1,
        weight: v.count,
        id: v.id
      };
      self.links.push(link);
    });

  },

  // スケールを作成
  makeScale: function(){

    this.nodeWeightScale = d3.scale.linear()
    .domain([0, d3.max(this.nodes, function(d) {
      return d.weight;
    })])
    .range([10, 1000]);

  },

  //レイアウトの計算
  startLayout: function(){

    this.forceLayout = d3.layout.force()
    .nodes(this.nodes)
    .links(this.links)
    .size([this.config.width, this.config.height])
    .distance(200) // node同士の距離
    .friction(0.9) // 摩擦力(加速度)的なものらしい。
    .charge(10) // 寄っていこうとする力。推進力(反発力)というらしい。
    .gravity(0.1) // 画面の中央に引っ張る力。引力。
    .start();

  },

  // 描画領域の設定
  svgSelection: function(){

    this.svg = d3.select("#network_graph")
                .append("svg")
                .attr({
                  width:this.config.width,
                  height:this.config.height
                });

  },


  // リンク線を描画
  renderLink: function(){

    this.linkSelection = this.svg.selectAll("line")
    .data(this.links)
    .enter()
    .append("line")
    .style({
        "stroke": "rgba(0,0,0,0.1)",
        "stroke-width": function(d){
          return 2;
          // return Math.sqrt(d.weight);
        }
      });

  },

  // ノードを描画
  renderNode: function(){

    this.nodeSelection = this.svg.selectAll("circle")
    .data(this.nodes)
    .enter()
    .append("circle")
    .attr({
      "r": function(d){
        return 20;
        // return Math.sqrt(d.weight);
      },
      "stroke-width": "5px",
      "stroke": "white"
    })
    .style({
      fill: "black"
    })
    .call(this.forceLayout.drag);

  },

  // ラベルの描画
  renderLabel: function(){

    this.labelSelection = this.svg.selectAll('text')
    .data(this.nodes)
    .enter()
    .append('text')
    .attr({
      "class":"label",
      "text-anchor":"left",
      "fill":"black",
      "font-size": "15px"
    })
    .text(function(d) { return d.label; });

  },


  // tickイベントの設定(力学計算が起こるたびに呼ばれるらしいので、座標追従などはここで)
  startTick: function(){

    var self = this;

    this.forceLayout.on("tick", function() {
      self.linkSelection.attr({
        x1: function(d) { return d.source.x;},
        y1: function(d) { return d.source.y;},
        x2: function(d) { return d.target.x;},
        y2: function(d) { return d.target.y;}
      });
      self.nodeSelection.attr({
        cx: function(d) { return d.x;},
        cy: function(d) { return d.y;}
      });
      // labelも追随するように
      self.labelSelection.attr({
        x: function(d) { return d.x;},
        y: function(d) { return d.y;}
      });
    });

  }

}; //app

<!DOCTYPE html>
<html lang="{_LANG}">
  <head>
    <meta charset="utf-8">
    <title>W-PCA Scatterplot Chart</title>
	<meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="WPCA scatter plot">
    <meta name="author" content="Michal Škop">

    <meta property="og:image" content="{_OG_IMAGE}"/>
	<meta property="og:title" content="WPCA scatter plot"/>
	<meta property="og:url" content="{_OG_URL}"/>
	<meta property="og:site_name" content="WPCA scatter plot"/>
	<meta property="og:type" content="website"/>
	
    <script src="http://d3js.org/d3.v3.min.js"></script>
    <script src="./d3.scatterplotwithlineplot.js"></script>
    <script src="./d3.tips.js"></script>

    <style type="text/css">
			
			/* note: we duplicate some of the styles (css, and as attributes of svg elements), so FF displays it correctly, and it is possible to generate png */
			.tick {
			  fill-opacity: 0;
			  stroke: #000000;
			  stroke-width: 1;
			}
			
			.domain {
			    fill: none;
				fill-opacity: 0;
				stroke: black;
				stroke-width: 1;
			}
			.axis line {
				fill: none;
				fill-opacity: 0;
				stroke: black;
				stroke-width: 1;
				shape-rendering: crispEdges;
			}
			
			.axis text {
				font-family: sans-serif;
				font-size: 11px;
				stroke: gray;
			}
			circle:hover {
			  fill-opacity: 1;
			}
			.label {
			  font-family: sans-serif;
			  font-size: 15px;
			}

			.d3-tip {
                line-height: 1;
                font-weight: bold;
                padding: 12px;
                background: rgba(0, 0, 0, 0.8);
                color: #fff;
                border-radius: 2px;
                pointer-events: none;
                max-width: 250px;
            }
            /* Creates a small triangle extender for the tooltip */
            .d3-tip:after {
                box-sizing: border-box;
                display: inline;
                font-size: 10px;
                width: 100%;
                line-height: 1;
                color: rgba(0, 0, 0, 0.8);
                position: absolute;
                pointer-events: none;
            }
            /* Northward tooltips */
            .d3-tip:after {
                content: "\25BC";
                margin: -1px 0 0 0;
                top: 100%;
                left: 0;
                text-align: center;
            }
            line {
             stroke:gray;
             stroke-width:1;
             opacity: .15;
            }
            .perfect {
              stroke: gray;
              stroke-width:3;
              opacity: 0.5;
            }
		</style>
  </head>
  <body>
    <div id="chart"></div>

    
<script type="text/javascript">
lines = {_LINES};
people = {_PEOPLE};

linesselected = [];
for (k in lines) {
  if ((parseFloat(lines[k]['w2']) > 0.5) && (parseFloat(lines[k]['cl_beta0']) < 50)) {
      beta = [lines[k]['normal_x'],lines[k]['normal_y']];
      beta0 = lines[k]['cl_beta0'];
      if (beta[1] != 0) {
        lines[k]['a'] = -beta0/beta[1];
        lines[k]['b'] = -beta[0]/beta[1];
      } else {
        lines[k]['a'] = 0;
        lines[k]['b'] = 0;
      }
      //add class for a perfect cut:
      if (lines[k]['loss'] == 0) {
        lines[k]['class'] = 'perfect';
      } else {
        lines[k]['class'] = 'non-perfect';
      }
      lines[k]['name'] = lines[k]["motion:name"] +"<br>"+lines[k]["start_date"]
      linesselected.push(lines[k]);
  }
}

spdata = [];
people.forEach(function(d) {
  spdata.push({"x":d["wpca:d1"],"y":d["wpca:d2"],"r":1,"color":d["color"],"name":d["name"]})
});
var scatterplotwithlineplot = [{
  "data": spdata,
  "margin": {top: 10, right: 10, bottom: 30, left: 30},
  "axes": {"labels":{"x":{_LABEL_DIM1}, "y":{_LABEL_DIM2}}},
  "minmax":{"x":{'min':{_XMIN},'max':{_XMAX}},"y":{'min':{_YMIN},'max':{_YMAX}},"r":{'min':0,'max':1},"rrange":{'min':0,'max':10}},
  "size":{"width":{_WIDTH},"height":{_HEIGHT}},
  "lines": linesselected
}];

 var svg = d3.select("#chart")
    .append("svg")
    .attr("width",scatterplotwithlineplot[0]['size']['width'])
    .attr("height",scatterplotwithlineplot[0]['size']['height']);
    
/* Initialize tooltip */
tip = d3.tip().attr('class', 'd3-tip').html(function(d) { 
  return "<span class=\'stronger\'>" + d["name"] + "</span><br>";
});

/* Invoke the tip in the context of your visualization */
svg.call(tip)

var sp = d3.scatterplotwithlineplot()
    .data(function(d) {return d.data})
    .margin(function(d) {return d.margin})
    .axes(function(d) {return d.axes})
    .minmax(function(d) {return d.minmax})
    .size(function(d) {return d.size})
    .lines(function(d) {return d.lines})

var scatter = svg.selectAll(".scatterplot")
    .data(scatterplotwithlineplot)
  .enter()
    .append("svg:g")
    .attr("transform", "translate(" + scatterplotwithlineplot[0].margin.left + "," + scatterplotwithlineplot[0].margin.top + ")")
    .call(sp);
</script>
<!-- creates svg and png pictures (using create_png.php) -->
<script src="https://code.jquery.com/jquery-1.11.1.js"></script>
<script src="http://crypto-js.googlecode.com/svn/tags/3.0.2/build/rollups/md5.js"></script>
<script>
    $(document).ready(function () {
        postdata = {'url':CryptoJS.MD5(window.location.href).toString(), 'svg':$('#chart').html().replace(/<strong>/g,'').replace(/<\/strong>/g,'').replace(/<br>/g,''), 'nocache': getParameterByName('nocache')};
        $.post('create_png.php',postdata);
        nothing = 0;
        //redirects to it when svg and png are ready
        if (($.inArray(getParameterByName('format'),['png','svg'])) > -1)
            get_picture();
    });
    function getParameterByName(name) {
        name = name.replace(/[\[]/, "\\[").replace(/[\]]/, "\\]");
        var regex = new RegExp("[\\?&]" + name + "=([^&#]*)"),
            results = regex.exec(location.search);
        return results === null ? "" : decodeURIComponent(results[1].replace(/\+/g, " "));
    }
    function get_picture() {
        var i = 0;
        $.ajax('cache/{_FORMAT}/' + CryptoJS.MD5(window.location.href).toString() + '.{_FORMAT}', {
            statusCode: {
              200: function (response) {
                 location.href = 'cache/{_FORMAT}/' + CryptoJS.MD5(window.location.href).toString() + '.{_FORMAT}';
              },
              404: function(response) {
                i++;
                if (i < 60) {
                  setTimeout(get_picture, 1000)
                } else {
                    alert('Something wrong, giving up...');
                }
              }
            }
        });
    }
</script>
  </body>
</html>

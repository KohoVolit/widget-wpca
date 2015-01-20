/* requires D3 + https://github.com/Caged/d3-tip */
d3.scatterplot = function() {
  function scatterplot(selection) {
    selection.each(function(d, i) {
      //options
      var data = (typeof(data) === "function" ? data(d) : d.data),
          margin = (typeof(margin) === "function" ? margin(d) : d.margin),
          axes = (typeof(axes) === "function" ? axes(d) : d.axes),
          minmax = (typeof(minmax) === "function" ? minmax(d) : d.minmax),
          size = (typeof(size) === "function" ? size(d) : d.size);
      
      // chart sizes
      var width = size['width'] - margin.left - margin.right,
          height = size['height'] - margin.top - margin.bottom;
      
      //scales
      var xScale = d3.scale.linear()
							 .domain([minmax['x']['min'], minmax['x']['max']])
							 .range([0, width])

      var yScale = d3.scale.linear()
							 .domain([minmax['y']['min'], minmax['y']['max']])
							 .range([height, 0])

      var rScale = d3.scale.linear()
							 .domain([minmax['r']['min'],minmax['r']['max']])
							 .range([minmax['rrange']['min'],minmax['rrange']['max']]);

      //axes
      var xAxis = d3.svg.axis()
        .scale(xScale)
        .orient("bottom");
        //.ticks(5);
        //.tickSize(16, 0);  
      var yAxis = d3.svg.axis()
        .scale(yScale)
        .orient("left");
        //.ticks(5); 
      

      var element = d3.select(this);
      
		//Create X axis
      element.append("g")
			.attr("class", "axis x-axis")
			.attr("transform", "translate(0," + height + ")")
			.call(xAxis);
		
		//Create Y axis
      element.append("g")
			.attr("class", "axis y-axis")
			.call(yAxis);
      
      element.selectAll("circle")
        .data(data)
		   .enter()
		 .append("circle")
		   .attr("cx", function(d) {
		   		return xScale(d.x);
		   })
		   .attr("cy", function(d) {
		   		return yScale(d.y);
		   })
		   .attr("r", function(d) {
		   		return rScale(1);
		   })
		   .attr("class", function(d) {
		   		if (typeof(d['class'] != 'undefined')) return d['class'];
		   		else return 'circle';
		   })
		   .on('mouseover', tip.show)
           .on('mouseout', tip.hide);
	
      //axis labels
	  element.append("text")
			.attr("class", "x-label label")
			.attr("text-anchor", "end")
			.attr("x", width)
			.attr("y", height-5)
			.text(axes['labels']['x']);
	  element.append("text")
			.attr("class", "y label")
			.attr("text-anchor", "end")
			.attr("y", 5)
			.attr("x", 0)
			.attr("dy", ".75em")
			.attr("transform", "rotate(-90)")
			.text(axes['labels']['y']);
			 
		
    });
  }
  scatterplot.data = function(value) {
    if (!arguments.length) return value;
    data = value;
    return scatterplot;
  };  
  scatterplot.margin = function(value) {
    if (!arguments.length) return value;
    margin = value;
    return scatterplot;
  };
  scatterplot.axes = function(value) {
    if (!arguments.length) return value;
    axes = value;
    return scatterplot;
  };
  scatterplot.minmax = function(value) {
    if (!arguments.length) return value;
    minmax = value;
    return scatterplot;
  };
  scatterplot.size = function(value) {
    if (!arguments.length) return value;
    size = value;
    return scatterplot;
  };
  
  return scatterplot;
}
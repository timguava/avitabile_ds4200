// code adapted from https://d3-graph-gallery.com/graph/connectedscatter_basic.html

// set the dimensions and margins of the graph
var margin = { top: 10, right: 30, bottom: 30, left: 60 },
    width = 460 - margin.left - margin.right,
    height = 400 - margin.top - margin.bottom;

// append the svg object to the body of the page
var svg = d3.select("#my_dataviz")
    .append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform",
        "translate(" + margin.left + "," + margin.top + ")");

//Read the data
d3.csv("gender_d3.csv",
    function (data) {
        // Add X axis --> it is a date format
        var x = d3.scaleLinear()
            .domain([0,0.5])
            .range([0, width]);
        svg.append("g")
            .attr("transform", "translate(0," + height + ")")
            .call(d3.axisBottom(x));
        svg.append("text")
            .attr("text-anchor", "end")
            .attr("x", width)
            .attr("y", height + margin.top + 20)
            .text("% of Women in the Senate");
        // Add Y axis
        var y = d3.scaleLinear()
            .domain([0, 0.5])
            .range([height, 0]);
        svg.append("g")
            .call(d3.axisLeft(y));
        svg.append("text")
            .attr("text-anchor", "end")
            .attr("transform", "rotate(-90)")
            .attr("y", -margin.left + 20)
            .attr("x", -margin.top)
            .text("% of Women in the House")
        // Add the line
        svg.append("path")
            .datum(data)
            .attr("fill", "none")
            .attr("stroke", "#00ff00")
            .attr("stroke-width", 1)
            .attr("d", d3.line()
                .x(function (d) { return x(d.senate) })
                .y(function (d) { return y(d.house) })
            )
        // Add the points
        svg
            .append("g")
            .selectAll("dot")
            .data(data)
            .enter()
            .append("circle")
            .attr("cx", function (d) { return x(d.senate) })
            .attr("cy", function (d) { return y(d.house) })
            .attr("r", 2)
            .attr("fill", "#00ff00")
    })
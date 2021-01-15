// Set up SVG object with width, height and margin
let scatter_width = (MAX_WIDTH / 2) - 10, scatter_height = 275;
let svg_scatter = d3.select("#scatterplot")
    .append("svg")
    .attr("width", scatter_width)
    .attr("height", scatter_height)
    .append("g")
    .attr("transform", `translate(${margin.left}, ${margin.top})`);

// Store data for calculating regression curves
let regData;
// D3 line generator for regression curves
let lineGenerator = d3.line().curve(d3.curveCatmullRom.alpha(0.5));

// Set up reference to tooltip
let tooltip = d3.select("body")
    .append("div")
    .attr("class", "tooltip")
    .style("opacity", 0);

// Declare scatter axes and labels
let x_scatter = d3.scaleTime()
    .range([0, scatter_width - margin.left - margin.right]);

let x_scatter_label = svg_scatter.append("g")
    .attr("transform", `translate(0, ${scatter_height - margin.top - margin.bottom})`);

let y_scatter = d3.scaleLinear()
    .range([0, scatter_height - margin.top - margin.bottom]);

let y_scatter_label = svg_scatter.append("g");

// Add x-axis label
svg_scatter.append("text")
    .attr("transform",
        `translate(${(scatter_width - margin.left - margin.right) / 2},
        ${(scatter_height - margin.top - margin.bottom) + 40})`)
    .style("text-anchor", "middle")
    .text("Date");

// Add y-axis label
svg_scatter.append("text")
    .attr("transform",
        `translate(-60, ${(scatter_height - margin.top - margin.bottom) / 2})`)
    .style("text-anchor", "middle")
    .text("Position");

let color_scatter = d3.scaleOrdinal();

// Add chart title
let title_scatter = svg_scatter.append("text")
    .attr("transform", `translate(${(bar_width - margin.left - margin.right) / 2}, ${-20})`)
    .style("text-anchor", "middle")
    .style("font-size", 15);

// Mouseover function to display the tooltip on hover
let mouseover = function(d) {
    let color_span = `<span style="color: ${color_scatter(d.song)};">`;
    let html = `${d.artist}<br/>
                ${color_span}${d.song}</span><br/>
                Position: ${color_span}${d.position}</span>`;

    // Show the tooltip and set the position relative to the event X and Y location
    tooltip.html(html)
        .style("left", `${(d3.event.pageX) + 30}px`)
        .style("top", `${(d3.event.pageY) - 100}px`)
        .style("box-shadow", `2px 2px 5px ${color_scatter(d.song)}`)
        .transition()
        .duration(200)
        .style("opacity", 0.9)
};

// Mouseout function to hide the tool on exit
let mouseout = function(d) {
    // Set opacity back to 0 to hide
    tooltip.transition()
        .duration(200)
        .style("opacity", 0);
};

/**
 * Sets the scatterplot to display information for a given song from the
 * startYear to the endYear
 */
function setScatterSong(startYear, endYear, song) {
    // Clear old regression curves
    d3.selectAll("path.reg").remove();
    // Filter data by year and song
    let filteredData = filterDataSong(startYear, endYear, song);
    // Store regression data for use in drawRegLines
    regData = [{key: song, values: filteredData}];

    // Update x-axis domain and axis label
    x_scatter.domain([Date.parse(startYear), Date.parse(endYear)]);
    x_scatter_label.call(d3.axisBottom(x_scatter)
        .tickFormat(function(date) {
            if (d3.timeYear(date) < date) {
                return d3.timeFormat('%b')(date);
            } else {
                return d3.timeFormat('%Y')(date);
            }
        }));
    // Update y-axis domain and axis label
    y_scatter.domain([0, d3.max(filteredData, function(d) {
        return parseInt(d.position);
    })]);
    y_scatter_label.call(d3.axisLeft(y_scatter));

    // Creates a reference to all the scatterplot dots
    let dots = svg_scatter.selectAll("circle").data(filteredData);
    // Render the dot elements on the DOM
    dots.enter()
        .append("circle")
        .on("mouseover", mouseover)
        .on("mouseout", mouseout)
        .merge(dots)
        .transition()
        .delay(function(d, i) { return(i*3) })
        .duration(1000)
        .attr("cx", function (d) { return x_scatter(Date.parse(d.date)); })
        .attr("cy", function (d) { return y_scatter(parseInt(d.position)); })
        .attr("r", 4)
        .attr("fill",  "#66a0e2");
    dots.exit().remove();
    // Chart title
    title_scatter.text(`${sentenceCase(cur_song)} (${cur_start_year}-${cur_end_year})`);
}

/**
 * Sets the scatterplot to display information for a given artist from the
 * startYear to the endYear
 */
function setScatter(startYear, endYear, artist) {
    // Clear old regression curves
    d3.selectAll("path.reg").remove();
    // Filter data by year and song
    let filteredData = filterDataArtist(startYear, endYear, artist);
    // Nest the data into groups, where a group is a given song by the artist
    let nestedData = d3.nest()
        .key(function(d) { return d.song })
        .entries(filteredData);
    // Store regression data for use in drawRegLines
    regData = nestedData;

    // Update x-axis domain and axis label
    x_scatter.domain([Date.parse(startYear), Date.parse(endYear)]);
    x_scatter_label.call(d3.axisBottom(x_scatter)
        .tickFormat(function(date) {
            if (d3.timeYear(date) < date) {
                return d3.timeFormat('%b')(date);
            } else {
                return d3.timeFormat('%Y')(date);
            }
        }));
    // Update y-axis domain and axis label
    y_scatter.domain([0, d3.max(filteredData, function(d) {
        return parseInt(d.position);
    })]);
    y_scatter_label.call(d3.axisLeft(y_scatter));

    // Get list of groups (songs) from nestedData
    let groups = nestedData.map(function(d) { return d.key });
    color_scatter.range(d3.quantize(d3.interpolateHcl("#66a0e2", "#ff5c7a"),
        Math.max(2, groups.length)));

    // Creates a reference to all the scatterplot dots
    let dots = svg_scatter.selectAll("circle").data(filteredData);
    // Render the dot elements on the DOM
    dots.enter()
        .append("circle")
        .on("mouseover", mouseover)
        .on("mouseout", mouseout)
        .merge(dots)
        .transition()
        .delay(function(d, i) { return(i*3) })
        .duration(1000)
        .attr("cx", function (d) { return x_scatter(Date.parse(d.date)); })
        .attr("cy", function (d) { return y_scatter(parseInt(d.position)); })
        .attr("r", 4)
        .attr("fill",  function(d){ return color_scatter(d.song); });
    dots.exit().remove();
    // Chart title
    title_scatter.text(`${sentenceCase(cur_artist)} (${cur_start_year}-${cur_end_year})`);
}

/**
 * Draw regression lines on the scatterplot
 */
function drawRegLines() {
    // Set up the D3 regression model
    let regression = d3.regressionQuad();
    // Create curve data by creating and array of [x,y] coordinates relative to the scatterplot
    regData = regData.filter(function(group) {
        return group.values.length > 1;
    });
    let curveData = regData.map(function(group) {
        // Map over each group
        return {
          song: group.key,
          data: group.values.map(function(entry) {
              // Convert entry date and position to [x,y] using x_scatter and y_scatter
              return [
                  x_scatter(Date.parse(entry.date)),
                  y_scatter(parseInt(entry.position))
              ];
          })
        };
    });
    // Select all path.reg DOM elements
    let reg_lines = svg_scatter.selectAll("path.reg").data(curveData);
    reg_lines.enter()
        .append("path")
        .attr("class", "reg")
        // Run regression then lineGenerator to create <path> element
        .attr("d", function(d) { return lineGenerator(regression(d.data)) })
        .style('stroke', function(d) { return darkenColor(color_scatter(d.song), 1); })
        .style('stroke-width', 3);
}


/**
 * Filters the given data to only include entries by the given artist and released
 * after the given year
 */
function filterDataArtist(startYear, endYear, artist) {
    return data.filter(function(a) {
        return splitArtist(a.artist).includes(artist) &&
            validYear(startYear, endYear, a.date);
    });
}

/**
 * Filters the given data to only include entries of a given song and released
 * after the given year
 */
function filterDataSong(startYear, endYear, song) {
    return data.filter(function(a) {
        return a.song === song && validYear(startYear, endYear, a.date);
    });
}

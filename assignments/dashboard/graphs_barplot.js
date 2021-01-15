let bar_width = (MAX_WIDTH / 2) - 10, bar_height = 250;

// Set up SVG object with width, height and margin
let svg_barplot = d3.select("#barplot")
    .append("svg")
    .attr("width", bar_width)
    .attr("height", bar_height)
    .append("g")
    .attr("transform", `translate(${margin.left}, ${margin.top})`);

// Create a linear scale for the x axis (number of occurrences)
let x_bar = d3.scaleLinear()
    .range([0, bar_width - margin.left - margin.right]);

// Create a scale band for the y axis (artist / song)
let y_bar = d3.scaleBand()
    .range([0, bar_height - margin.top - margin.bottom])
    .padding(0.1);  // Improves readability

// Set up reference to count SVG group
let countRef = svg_barplot.append("g");
// Set up reference to y axis label to update text in setData
let y_axis_label = svg_barplot.append("g").attr("id", "y_bar_label");

// Add x-axis label
svg_barplot.append("text")
    .attr("transform",
        `translate(${(bar_width - margin.left - margin.right) / 2},
        ${(bar_height - margin.top - margin.bottom) + 15})`)
    .style("text-anchor", "middle")
    .text("Count");

// Add y-axis label
let y_axis_text = svg_barplot.append("text")
    .attr("transform", `translate(-120, ${(bar_height - margin.top - margin.bottom) / 2})`)
    .style("text-anchor", "middle");

// Add chart title
let title = svg_barplot.append("text")
    .attr("transform", `translate(${(bar_width - margin.left - margin.right) / 2}, ${-20})`)
    .style("text-anchor", "middle")
    .style("font-size", 15);

// Define color scale
let color = d3.scaleOrdinal()
    .range(d3.quantize(d3.interpolateHcl("#66a0e2", "#81c2c3"), NUM_EXAMPLES));

/**
 * Sets the data on the barplot using the provided index of valid data sources and an attribute
 * to use for comparison
 */
function updateData(startYear, endYear, attr) {
    // Filter data by year
    let filteredData = data.filter(function(a) {
        return validYear(startYear, endYear, a.date);
    });
    // Store counts for each attr in hash
    let hash = {};
    filteredData.forEach(function(a) {
        let cleaned = trimText(a[attr]);
        if (hash[cleaned]) {
            hash[cleaned] += 1;
        }  else {
            hash[cleaned] = 1;
        }
    });

    // Post-process data before sorting and splicing
    let attr_data = [];
    for (let i=0; i < Object.keys(hash).length; i++) {
        let k = Object.keys(hash)[i];
        // Store each entry as hash of attr, count, and id
        attr_data.push({attr: k, count: hash[k], id: i});
    }
    attr_data = cleanData(attr_data, function(a, b) {
        return parseInt(b.count) - parseInt(a.count)
    }, NUM_EXAMPLES);

    // Update the x axis domain with the max count of the provided data
    x_bar.domain([0, d3.max(attr_data, function(d) { return parseInt(d.count); })]);
    // Update the y axis domains with the desired attribute
    y_bar.domain(attr_data.map(function(d) { return d.attr }));
    color.domain(attr_data.map(function(d) { return d.attr }));

    // Render y-axis label
    y_axis_label.call(d3.axisLeft(y_bar).tickSize(0).tickPadding(10));
    let bars = svg_barplot.selectAll("rect").data(attr_data);

    // Render the bar elements on the DOM
    bars.enter()
        .append("rect")
        // Set up mouse interactivity functions
        .on("mouseover", mouseover_barplot)
        .on("mouseout", mouseout_barplot)
        .on("click", click_barplot)
        .merge(bars)
        .transition()
        .duration(1000)
        .attr("fill", function(d) { return color(d.attr) })
        .attr("x", x_bar(0))
        .attr("y", function(d) { return y_bar(d.attr); })
        .attr("width", function(d) { return x_bar(parseInt(d.count)); })
        .attr("height",  y_bar.bandwidth())
        .attr("id", function(d) { return `rect-${d.id}` });
    /*
        In lieu of x-axis labels, display the count of the artist next to its bar on the
        bar plot.
     */
    let counts = countRef.selectAll("text").data(attr_data);
    // Render the text elements on the DOM
    counts.enter()
        .append("text")
        .merge(counts)
        .transition()
        .duration(1000)
        .attr("x", function(d) { return x_bar(parseInt(d.count)) + 10; })
        .attr("y", function(d) { return y_bar(d.attr) + 10; })
        .style("text-anchor", "start")
        .text(function(d) {return parseInt(d.count);});
    // Add y-axis text and chart title
    y_axis_text.text(sentenceCase(attr));
    title.text(`Top ${sentenceCase(attr)}s in Billboard 100 Charts (${startYear} - ${endYear})`);
    // Remove elements not in use if fewer groups in new dataset
    bars.exit().remove();
    counts.exit().remove();
}

/**
 * Cleans the provided data using the given comparator then strips to first numExamples
 * instances
 */
function cleanData(data, comparator, numExamples) {
    return data.sort(comparator).slice(0, numExamples);
}

// Darken bar fill in barplot on mouseover
let mouseover_barplot = function(d) {
    svg_barplot.select(`#rect-${d.id}`).attr("fill", function(d) {
        return darkenColor(color(d.attr), 0.5);
    });
};

// Set scatterplot to song or artist based on cur_attr
let click_barplot = function(d) {
    if (cur_attr === 'artist') {
        cur_artist = d.attr;
        setScatter(cur_start_year, cur_end_year, cur_artist);
    } else {
        cur_song = d.attr;
        setScatterSong(cur_start_year, cur_end_year, cur_song);
    }
};

// Restore bar fill to original color on mouseout
let mouseout_barplot = function(d) {
    svg_barplot.select(`#rect-${d.id}`).attr("fill", function(d) {
        return color(d.attr)
    });
};

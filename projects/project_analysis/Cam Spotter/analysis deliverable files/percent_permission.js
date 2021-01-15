// Set up width and height for barplot
let width = 900,
    height = 350;

// TODO: Set up SVG object with width, height and margin
/*
    HINT: Our first call to select will select the id of the div in HTML where we want to insert our barplot

    HINT: To add a margin to your svg graph, add the attribute
    attr("transform", "translate(x, y)"), where x is the left margin
    and y is the top margin
 */
let svg = d3.select("#barplot")
    .append("svg")
    .attr("width", width)     // HINT: width
    .attr("height", height)     // HINT: height
    .append("g")
    .attr("transform", `translate(${margin.left}, ${margin.top})`);    // HINT: transform

// Set up reference to count SVG group
let countRef = svg.append("g");



// TODO: Load the artists CSV file into D3 by using the d3.csv() method
d3.csv("/Users/chisommbadugha/Downloads/Overprivilege-B.csv").then(function(data) {
    // TODO: Clean and strip desired amount of data for barplot
    data = cleanData(data, function(a, b) { return parseInt(b.count) - parseInt(a.count) }, NUM_EXAMPLES);

    // TODO: Create a linear scale for the x axis (number of occurrences)
    let x = d3.scaleLinear()
        .domain([0, d3.max(data, function(d) { return parseInt(d.count); })])
        .range([0, width - margin.left - margin.right]);
    /*
        HINT: The domain and range for the linear scale map the data points
        to appropriate screen space.

        The domain is the interval of the smallest to largest data point
        along the desired dimension. You can use the d3.max(data, function(d) {...})
        function to get the max value in the dataset, where d refers to a single data
        point. You can access the fields in the data point through d.count or,
        equivalently, d["count"].

        The range is the amount of space on the screen where the given element
        should lie. We want the x-axis to appear from the left edge of the svg object
        (location 0) to the right edge (width - margin.left - margin.right).
     */

    // TODO: Create a scale band for the y axis (artist)
    let y = d3.scaleBand()
        .domain(data.map(function(d) { return d["percentage granted permissions"] }))
        .range([0, height - margin.top - margin.bottom])
        .padding(0.1);  // Improves readability
    /*
        HINT: For the y-axis domain, we want a list of all the artist names in the dataset.
        You might find JavaScript's map function helpful.

        Set up the range similar to that of the x-axis. Instead of going from the left edge to
        the right edge, we want the y-axis to go from the top edge to the bottom edge. How
        should we define our boundaries to incorporate margins?
     */

    // TODO: Add y-axis label
    svg.append("g")
        .call(d3.axisLeft(y).tickSize(0).tickPadding(10));
    // HINT: The call function takes in a d3 axis object. Take a look at the d3.axisLeft() function.

    // OPTIONAL: Define color scale
    let color = d3.scaleOrdinal()
        .domain(data.map(function(d) { return d["percentage granted permissions"] }))
        .range(d3.quantize(d3.interpolateHcl("#66a0e2", "#81c2c3"), NUM_EXAMPLES));

    /*
        This next line does the following:
            1. Select all desired elements in the DOM
            2. Count and parse the data values
            3. Create new, data-bound elements for each data value
     */
    let bars = svg.selectAll("rect").data(data);

    // TODO: Render the bar elements on the DOM
    /*
        This next section of code does the following:
            1. Take each selection and append a desired element in the DOM
            2. Merge bars with previously rendered elements
            3. For each data point, apply styling attributes to each element
     */
    bars.enter()
        .append("rect")
        .merge(bars)
        .attr("fill", function(d) { return color(d["percentage granted permissions"]) })    // OPTIONAL for students
        .attr("x", x(0))
        .attr("y", function(d) { return y(d["percentage granted permissions"]); })          // HINT: Use function(d) { return ...; } to apply styles based on the data point
        .attr("width", function(d) { return x(parseInt(d.count)); })
        .attr("height",  y.bandwidth());        // HINT: y.bandwidth() makes a reasonable display height
    /*
        HINT: The x and y scale objects are also functions! Calling the scale as a function can be
        used to convert between one coordinate system to another.

        To get the y starting coordinates of a data point, use the y scale object, passing in a desired
        artist name to get its corresponding coordinate on the y-axis.

        To get the bar width, use the x scale object, passing in a desired artist count to get its corresponding
        coordinate on the x-axis.
     */
    /*
        In lieu of x-axis labels, we are going to display the count of the artist next to its bar on the
        bar plot. We will be creating these in the same manner as the bars.
     */
    let counts = countRef.selectAll("text").data(data);

    // TODO: Render the text elements on the DOM
    counts.enter()
        .append("text")
        .merge(counts)
        .attr("x", function(d) { return x(parseInt(d.count)) + 10; })       // HINT: Add a small offset to the right edge of the bar, found by x(d.count)
        .attr("y", function(d) { return y(d.percentage granted permissions) + 10})       // HINT: Add a small offset to the top edge of the bar, found by y(d.artist)
        .style("text-anchor", "start")
        .text(function(d) { return parseInt(d.count)});           // HINT: Get the count of the artist

    // Add x-axis label
    svg.append("text")
        .attr("transform", `translate(${(width - margin.left - margin.right) / 2},
                                        ${(height - margin.top - margin.bottom) + 15})`)       // HINT: Place this at the bottom middle edge of the graph
        .style("text-anchor", "middle")
        .text("permissions");

    // Add y-axis label
    svg.append("text")
        .attr("transform", `translate(-120, ${(height - margin.top - margin.bottom) / 2})`)       // HINT: Place this at the center left edge of the graph
        .style("text-anchor", "middle")
        .text("percentage granted permissions");

    // Add chart title
    svg.append("text")
        .attr("transform", `translate(${(width - margin.left - margin.right) / 2}, ${-10})`)       // HINT: Place this at the top middle edge of the graph
        .style("text-anchor", "middle")
        .style("font-size", 15)
        .text("Percetage of times overprivilege occurs in given number of applications");
});

/**
 * Cleans the provided data using the given comparator then strips to first numExamples
 * instances
 */
function cleanData(data, comparator, numExamples) {
    return data.sort(comparator).slice(0, numExamples);
}

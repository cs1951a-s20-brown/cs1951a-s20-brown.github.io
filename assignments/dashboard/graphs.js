// Declare svg_graph with width and height
let graph_width = MAX_WIDTH / 2, graph_height = 575;
let svg_graph = d3.select("#graph")
    .append("svg")
    .attr("width", graph_width)
    .attr("height", graph_height)
    .append("g")
    .attr("transform", `translate(${-10}, ${margin.top})`);

// Define forces along X and Y axes with custom center and strength values
const forceX = d3.forceX(graph_width / 2).strength(0.05);
const forceY = d3.forceY((graph_height + margin.top) / 2).strength(0.05);

// Graph title
let graph_title = svg_graph.append("text")
    .attr("transform", `translate(${(graph_width / 2)}, ${-20})`)
    .style("text-anchor", "middle")
    .style("font-size", 15);

// Create D3 forceSimulation for graph
let simulation = d3.forceSimulation()
    .force('x', forceX)
    .force('y',  forceY)
    // Use data id field for links
    .force("link", d3.forceLink().id(function(d) { return d.id; }))
    .force("charge", d3.forceManyBody())
    .force("center", d3.forceCenter((graph_width - margin.right) / 2,
        (graph_height - margin.top) / 2));

// Set up color scheme for graph
let color_artists = d3.scaleOrdinal(d3.schemeTableau10);

/**
 * Given a year, creates a graph of connectivity between artists by parsing song titles
 * in the year. Nodes represent artists and edges represent a song that both artists
 * have appeared in.
 */
function createGraph(year) {
    // Set up links, nodes, and output_links
    let links = [], nodes = [], output_links = [];
    // Set up sets of seen songs and all artists
    let seen = new Set(), artists = new Set();
    // Iterate over all data entries
    for (let i = 0; i < data.length; i++){
        let entry = data[i];
        // Split entry to get all artists that appeared in the song
        let song_collaborators = splitArtist(entry.artist);
        // Skip if already seen, no collaborators, or not within given year
        if (seen.has(entry.song) || song_collaborators.length === 1 ||
            !validYear(year, year + 1, entry.date)) {
            continue;
        }
        // Add all song_collaborators to set of artists
        song_collaborators.forEach(artists.add, artists);
        // First collaborator is the source in edge
        let source = song_collaborators[0];
        for (let j = 1; j < song_collaborators.length; j++) {
            // Each additional collaborator is target in edge
            links.push([source, song_collaborators[j], entry.song]);
        }
        seen.add(entry.song);
    }
    // Convert artists to array
    artists = [...artists];
    // Define count function to get number of times two artists collaborated
    let count = function(pair) {
      let c = 0;
      links.forEach(function(l) {
          // Check for forward and reverse pairs
          if (JSON.stringify(l) === JSON.stringify(pair) ||
              JSON.stringify(l) === JSON.stringify(pair.reverse())) {
            c++;
          }
      });
      return c;
    };
    let i = 0;
    // Map each link to an object with source, target, and value fields
    links.forEach(function(a) {
        let html = `<b><u>${a[2]}</u></b><br/> ${a[0]} &#8596; ${a[1]}`;
        output_links.push({source: a[0], target: a[1], value: count(a), html: html, id: i});
        i++;
    });
    // Get list of valid artists (run DFS and make sure depth of at least 4)
    let validArtists = [];
    artists.forEach(function(a) {
        // Filter out invalid artists
        if (!validArtist(a, output_links, 2)) {
            output_links = output_links.filter(function(link) {
                return !(link.source === a || link.target === a);
            })
        } else {
            validArtists.push(a);
        }
    });
    // Map each valid artist to an object with id, group, and count fields
    i = 0;
    validArtists.forEach(function(a) {
        let group = Math.round(artists.indexOf(a) * (10.0 / artists.length));
        let count = links.filter(function(link) {
            return link[0] === a || link[1] === a;
        }).length;
        nodes.push({id: a, group: group, count: count, idx: i});
        i++;
    });
    // Graph title
    graph_title.text(`Artist Collaborations* in the Billboard Top 100 Songs (${year})`);
    // Start graph animation
    startGraph({nodes: nodes, links: output_links});
}

/**
 * Given an artist and list of links, checks if the artist is valid to display.
 * Artist is defined as valid if there exist a path from the artist with
 * length of at least n.
 */
function validArtist(artist, links, n) {
    // Run a DFS to get depth at each stage
    let stack = [artist];
    let depth = 0;
    let seen = new Set();
    while (stack.length > 0) {
        let vertex = stack.pop();
        if (!seen.has(vertex)) {
            // Find neighbors
            let neighbors = links.filter(function(a) {
                return a.source === vertex || a.target === vertex;
            });
            neighbors = neighbors.map(function(a) {
                if (a.source === vertex) return a.target;
                else return a.source;
            });
            // Push neighbors to stack and increment depth
            stack.push(...neighbors);
            depth += 1;
            seen.add(vertex);
            // If depth is at least n, return true (valid artist)
            if (depth > n) {
                return true;
            }
        }
    }
    // Otherwise, return false (invalid artist)
    return false;
}

let node_size = d3.scaleLinear().range([4, 10]);

/**
 * Starts the graph animation given a graph object
 */
function startGraph(graph) {
    // Set up D3 linear scale for the node size based on the number of connections an artist has
    node_size.domain(d3.extent(graph.nodes, function(d) { return parseInt(d.count); }));

    // Use graph.links to create lines with width as a function of number of collaborations
    let link = svg_graph.append("g")
        .attr("class", "links")
        .selectAll("line")
        .data(graph.links)
        .enter().append("line")
        // Use number of collaborations to get stroke-width
        .attr("stroke-width", "2")
        .attr("id", function(d) { return `link-${d.id}` })
        .on("mouseover", function(d) { flow_mouseover(d, "html", "link") })
        .on("mouseout", function(d) { flow_mouseout(d, "html", "link")} );

    // Use graph.nodes to create circles for each artist
    let node = svg_graph.append("g")
        .attr("class", "nodes")
        .selectAll("g")
        .data(graph.nodes)
        .enter().append("g");
    node.append("circle")
        // Use number of collaborators to get radius
        .attr("r", function(d) { return node_size(parseInt(d.count)) })
        .attr("fill", function(d) { return color_artists(d.group); })
        .attr("id", function(d) { return `node-${d.idx}` })
        .on("mouseover", function(d) { flow_mouseover(d, "id", 'node') })
        .on("mouseout", function(d) { flow_mouseout(d, "id", 'node') })
        .call(d3.drag()
            .on("start", dragstarted)
            .on("drag", dragged)
            .on("end", dragended));
    // Set up simulation handlers and simulation link force
    simulation.nodes(graph.nodes).on("tick", ticked);
    simulation.force("link").links(graph.links);

    /**
     * Function for when animation is ticked
     */
    function ticked() {
        link.attr("x1", function(d) { return d.source.x; })
            .attr("y1", function(d) { return d.source.y; })
            .attr("x2", function(d) { return d.target.x; })
            .attr("y2", function(d) { return d.target.y; });

        node.attr("transform", function(d) {
                // Set up boundary box to prevent animation from going past SVG dimensions
                let radius = Math.round(node_size(parseInt(d.count)));
                d.x = Math.max(radius,
                    Math.min(graph_width - radius, d.x));
                d.y = Math.max(radius,
                    Math.min((graph_height - margin.top - margin.bottom) - radius, d.y));
                return "translate(" + d.x + "," + d.y + ")";
            });
    }
}

// Mouseover function to display the tooltip on hover
let flow_mouseover = function(d, attr, id) {
    if (id === "node") {
        svg_graph.select(`#node-${d.idx}`).attr("fill", function(d) {
            return darkenColor(color_artists(d.group), 0.5);
        }).attr("r", function(d) {
            return node_size(parseInt(d.count)) * 1.5;
        })
    } else {
        svg_graph.select(`#link-${d.id}`).attr("stroke-width", '7');
    }

    //

    let html = `${d[attr]}`;

    // Show the tooltip and set the position relative to the event X and Y location
    tooltip.html(html)
        .style("left", `${(d3.event.pageX) - 50}px`)
        .style("top", `${(d3.event.pageY) + 30}px`)
        .style("box-shadow", `1px 1px 5px`)
        .transition()
        .duration(200)
        .style("opacity", 0.9)
};

// Mouseout function to hide the tool on exit
let flow_mouseout = function(d, attr, id) {
    if (id === "node") {
        svg_graph.select(`#node-${d.idx}`).attr("fill", function(d) {
            return color_artists(d.group);
        }).attr("r", function(d) {
            return node_size(parseInt(d.count));
        })
    } else {
        svg_graph.select(`#link-${d.id}`).attr("stroke-width", '2');
    }

    // Set opacity back to 0 to hide
    tooltip.transition()
        .duration(200)
        .style("opacity", 0);
};


/**
 * Function for when node is starting to be dragged
 */
function dragstarted(d) {
    if (!d3.event.active) simulation.alphaTarget(0.3).restart();
    d.fx = d.x;
    d.fy = d.y;
}

/**
 * Function for when node is dragged
 */
function dragged(d) {
    d.fx = d3.event.x;
    d.fy = d3.event.y;
}

/**
 * Function for when node has finished being dragged
 */
function dragended(d) {
    if (!d3.event.active) simulation.alphaTarget(0);
    d.fx = null;
    d.fy = null;
}

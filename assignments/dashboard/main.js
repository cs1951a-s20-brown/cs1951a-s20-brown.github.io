const MAX_WIDTH = Math.max(1080, window.innerWidth);
const MAX_HEIGHT = 720;
const margin = {top: 40, right: 100, bottom: 40, left: 175};
const NUM_EXAMPLES = 10;

let data;
let cur_artist = "Maroon 5";
let cur_song = "Better";
let cur_attr = "artist";
let cur_start_year = 2019;
let cur_end_year = 2020;

let slider = new Slider('#year', {});
let attr_input = document.getElementById("attrInput");


// Load data from billboard.csv file
d3.csv("./data/billboard.csv").then(function(d) {
    data = d;
    updateDashboard();
    createGraph(2019);
});

// Update cur_start_year and cur_end_year on slideStop of range slider
slider.on("slideStop", function(range) {
    cur_start_year = range[0];
    cur_end_year = range[1];
    updateDashboard();
});

/**
 * Set the data source for bar and scatter plots between artist and song
 */
function setData(attr) {
    cur_attr = attr;
    attr_input.placeholder = sentenceCase(attr);
    updateDashboard();
}

/**
 * Updates cur attribute with new artist or song from user input
 */
function setAttr() {
    if (cur_attr === "artist") {
        cur_artist = attr_input.value;
    } else {
        cur_song = attr_input.value;
    }
    updateDashboard();
}

/**
 * Updates dashboard scatterplot and barplot after change in date or cur_attr
 */
function updateDashboard() {
    updateData(cur_start_year, cur_end_year, cur_attr);
    if (cur_attr === "artist") {
        setScatter(cur_start_year, cur_end_year, cur_artist);
    } else {
        setScatterSong(cur_start_year, cur_end_year, cur_song);
    }
}

/**
 * Checks if a date falls within a provided year range
 */
function validYear(start, end, cur) {
    return (Date.parse(start) < Date.parse(cur)) &&
        (Date.parse(cur) < Date.parse(end));
}

/**
 * Converts a text to sentence case
 */
function sentenceCase(word) {
    return `${word[0].toUpperCase()}${word.substring(1)}`;
}

/**
 * Abbreviates and shortens a given label by adding ellipses
 */
function trimText(label) {
    if (label.length > 20) {
        return label.substring(0, 20) + "..."
    }
    return label;
}

/**
 * Finds all artists collaborating on a song by splitting on predefined text
 * and returns a list of all artists
 */
function splitArtist(artist) {
    let song_artists = artist.split(/(?:Featuring|&|,)/);
    return song_artists.map(s => trimText(s.trim()));
}

/**
 * Returns a darker shade of a given color
 */
function darkenColor(color, percentage) {
    return d3.hsl(color).darker(percentage);
}

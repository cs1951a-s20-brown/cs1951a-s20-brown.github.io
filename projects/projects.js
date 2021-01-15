
const DATA = true;
const STATS = false;
const VIZ = false;
const POSTER = true;
const ANALYSIS = true;

let deck = document.body.getElementsByClassName("card-deck").item(0);

$.getJSON("teams.json", function(json) {
    for (var key in json) {

        var base = document.createElement("div");
        base.className = "card text-white";
        base.style = "max-width: 14rem; max-height: 26rem;";

        var cbody = document.createElement("div");
        cbody.className = "card-body";

        var card_container = document.createElement("div");
        card_container.className = "card_container";
        card_container.style = "width: inherit";

        var link = document.createElement("a");
        if (POSTER) {
            link.href = "project_poster/" + encodeURIComponent(key).replace("%2F", "/") + "/poster.pdf";
        } else {
            link.href = "rick.jpg";
        }
	link.target= "_blank"

        link.style = "width: inherit";

        var img = document.createElement("img");
        img.className = "card-img-top";
        if (POSTER) {
            img.src = "project_poster/" + encodeURIComponent(key).replace("%2F", "/") + "/thumbnail.jpg";
        } else {
            img.src = "rick.jpg";
        }
        img.alt = "Card image cap";
        img.style="width: 90%;";

        // link.appendChild(img);

        var h5 = document.createElement("h5");
        h5.className = "card-title";
        h5.innerHTML = key;

        var h6 = document.createElement("h6");
        h6.className = "card-subtitle  text-justify ";
        h6.innerHTML = json[key];

        var buttonGroup = document.createElement("div");
        buttonGroup.className = "btn-group";
        buttonGroup.role = "group";

        var b1 = document.createElement("a");
        if (DATA) {
            b1.className = "b1 btn btn-primary";
        } else {
            b1.className = "b1 btn btn-primary disabled";
        }
        b1.href = "project_data/" + encodeURIComponent(key).replace("%2F", "/") + "/data.html";
        b1.innerHTML = "DATA";
	/*
        var b2 = document.createElement("a");
        if (STATS) {
            b2.className = "b2 btn btn-primary ";
        } else {
            b2.className = "b2 btn btn-primary disabled";
        }
        b2.href ="project_stats/" + encodeURIComponent(key).replace("%2F", "/") + "/stats.html";
        b2.innerHTML = "STATS";

        var b3 = document.createElement("a");
        if (VIZ) {
            b3.className = "b3 btn btn-primary";
        } else {
            b3.className = "b3 btn btn-primary disabled";
        }
        b3.href = "project_viz/" + encodeURIComponent(key).replace("%2F", "/") + "/viz.html";
        b3.innerHTML = "VIZ";
	*/
	var b4 = document.createElement("a");
        if (ANALYSIS) {
            b4.className = "b2 btn btn-primary ";
        } else {
            b4.className = "b2 btn btn-primary disabled";
        }
        b4.href ="project_analysis/" + encodeURIComponent(key).replace("%2F", "/") + "/analysis.html";
        b4.innerHTML = "ANALYSIS";

	var b5= document.createElement("a");
        if (POSTER) {
            b5.className = "b3 btn btn-primary ";
        } else {
            b5.className = "b3 btn btn-primary disabled";
        }
        b5.href ="project_poster/" + encodeURIComponent(key).replace("%2F", "/") + "/abstract.pdf";
        b5.innerHTML = "ABSTRACT";


        var button_container = document.createElement("div");
        button_container.className = "button-container";
        button_container.appendChild(b1);
        button_container.appendChild(b4);
	button_container.appendChild(b5);
	//button_container.appendChild(b3);

        var img_container = document.createElement("div");
        img_container.className = "img-container";
        //img_container.append(link);

        img_container.style.backgroundImage = "url(" + '' + img.src + '' +  ")";

        var content_container = document.createElement("div");
        content_container.className = "content-container";
        content_container.appendChild(h5);
        content_container.appendChild(h6);
        content_container.appendChild(button_container);
	
	link.appendChild(img_container);
	card_container.appendChild(link);
	//card_container.appendChild(img_container);
        card_container.appendChild(content_container);

        cbody.appendChild(card_container);
        base.appendChild(cbody);
        deck.appendChild(base);
    }
});

var enableRaphaelGroups = function() {
    r.group = function(c, e) {
        this.svg = "http://www.w3.org/2000/svg";
        this.defs = document.getElementsByTagName("defs")[c];
        this.svgcanv = document.querySelector("g");
        this.group = document.createElementNS(this.svg, "g");
        for(i = 0; i < e.length; i++) {
            this.group.appendChild(e[i].node);
        }
        this.svgcanv.appendChild(this.group);

        return this.group;
    };
};
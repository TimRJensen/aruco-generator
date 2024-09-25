let MODE = 0;

// Hide event handle
(function () {
    const elm = document.getElementById("hide");
    elm.onpointerdown = (e) => {
        e.preventDefault();
        elm.dataset.toggled = elm.dataset.toggled == "0" ? "1" : "0";
    };
})();

// Mode event handler
(function () {
    const elm = document.getElementById("mode");

    for (const child of elm.children) {
        child.onpointerdown = (e) => {
            e.preventDefault();

            if (child.dataset.toggled == "1") {
                return;
            }

            const sibling =
                child == elm.firstElementChild
                    ? child.nextElementSibling
                    : child.previousElementSibling;
            child.dataset.toggled = "1";
            sibling.dataset.toggled = "0";
            MODE = ++MODE % 2;
        };
    }
})();

const inputs = [];
for (const form of document.querySelectorAll(".form")) {
    inputs.push(...form.querySelectorAll(".input"));
    form.onsubmit = (e) => {
        e.preventDefault();
    };
}

// Generator event handler
(function () {
    const root = document.querySelector(":root");
    const elm = document.getElementById("content");

    function handleSubmit(e) {
        if (e) {
            e.preventDefault();
        }

        const markers = [];
        const q = `/q?dict=${inputs[0].value}&size=${inputs[1].value}`;
        if (MODE) {
            // Board mode
            for (let i = 0; i < parseInt(inputs[4].value) * parseInt(inputs[3].value); i++) {
                const mark = document.createElement("img");
                mark.src = `${q}&id=${i}`;
                markers.push(mark);
            }
        } else {
            // Single mode
            const mark = document.createElement("img");
            mark.src = `${q}&id=${inputs[2].value}`;
            markers.push(mark);
        }

        const children = []
        for (let mark of markers) {
            const child = document.createElement("div");
            child.appendChild(mark);
            children.push(child);
        }

        root.style.setProperty("--mark-size", inputs[1].value);
        root.style.setProperty("--grid-rows", MODE ? inputs[3].value : 1);
        root.style.setProperty("--grid-cols", MODE ? inputs[4].value : 1);
        elm.replaceChildren(...children);
    }

    document.querySelector(".form.generate").onsubmit = handleSubmit;
    handleSubmit(null);
})();

// Measure event handler
(function () {
    const elms = document.querySelectorAll(".log");
    const texts = ["Marker length", "Column gap", "Row gap"];

    function handleSubmit(e) {
        e.preventDefault();

        if (!inputs[4].reportValidity()) {
            return;
        }

        const diagonal = parseInt(inputs[5].value);
        const vw = parseInt(inputs[6].value);
        const vh = parseInt(inputs[7].value);
        const ppmm = Math.sqrt(vw ** 2 + vh ** 2) / diagonal / 25.4;

        const n = parseInt(inputs[4].value);
        const markers = document.querySelectorAll("#content img");
        const first = markers[0];
        const first_box = first.getBoundingClientRect();
        const measures = [first_box.width / ppmm];
        let next = null;
        let i = 0;

        while (MODE && i < 2 && (next = markers[n ** i])) {
            measures.push(
                Math.abs(
                    i
                        ? first_box.bottom - next.getBoundingClientRect().top
                        : first_box.right - next.getBoundingClientRect().left
                ) / ppmm
            );
            i++;
        }

        const children = [];
        for (let i = 0; i < measures.length; i++) {
            for (let text of [texts[i], `${measures[i].toFixed(2)}mm`]) {
                const child = document.createElement("div");
                child.textContent = text;
                children.push(child);
            }
        }
        for (const elm of elms) {
            if (window.getComputedStyle(elm).getPropertyValue("display") != "none") {
                elm.replaceChildren(...children);
            }
        }
    }

    document.querySelector(".form.measure").onsubmit = handleSubmit;
    const obs = new ResizeObserver(() => {
        inputs[6].value = window.innerWidth;
        inputs[7].value = window.innerHeight;
    });
    obs.observe(document.querySelector("body"));
})();

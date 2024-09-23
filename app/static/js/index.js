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
            let sibling;
            if (child.dataset.toggled == "1") {
                return;
            }
            sibling =
                child == elm.firstElementChild
                    ? child.nextElementSibling
                    : child.previousElementSibling;
            child.dataset.toggled = "1";
            sibling.dataset.toggled = "0";
            MODE = ++MODE % 2;
        };
    }
})();

let inputs = [];
for (const form of document.querySelectorAll(".form")) {
    inputs = inputs.concat(form.querySelectorAll(".input"));
    form.onsubmit = (e) => {
        e.preventDefault();
    };
}

// Generator event handler
(function () {
    const root = document.querySelector(":root");
    const elm = document.getElementById("content");
    const img = document.createElement("img");
    img.src = "/q?dict=0&id=0&size=200";
    const box = document.createElement("div");
    box.appendChild(img);
    elm.appendChild(box);

    function handleSubmit(e) {
        e.preventDefault();

        const q = `/q?dict=${inputs[0][0].value}&size=${inputs[0][1].value}`;
        let vals = [inputs[0][1].value, 1, 1];
        let children = [];
        if (MODE) {
            // Board mode
            vals[1] = inputs[0][3].value;
            vals[2] = inputs[0][4].value;

            for (let i = 0; i < inputs[0][4].value * inputs[0][3].value; i++) {
                const img = document.createElement("img");
                img.src = `${q}&id=${i}`;
                const box = document.createElement("div");
                box.appendChild(img);
                children = children.concat(box);
            }
        } else {
            // Single mode
            const img = document.createElement("img");
            img.src = `${q}&id=${inputs[0][2].value}`;
            const box = document.createElement("div");
            box.appendChild(img);
            children = children.concat(box);
        }
        root.style.setProperty("--mark-size", vals[0]);
        root.style.setProperty("--grid-rows", vals[1]);
        root.style.setProperty("--grid-cols", vals[2]);
        elm.replaceChildren(...children);
    }

    document.querySelector(".form.generate").onsubmit = handleSubmit;
})();

// Measure event handler
(function () {
    const elm = document.getElementById("log");
    const msgs = ["Marker length", "Column gap", "Row gap"];

    function handleSubmit(e) {
        e.preventDefault();

        if (!inputs[0][4].reportValidity()) {
            return;
        }

        const diagonal = parseInt(inputs[1][0].value);
        const vw = parseInt(inputs[1][1].value);
        const vh = parseInt(inputs[1][2].value);
        const ppmm = Math.sqrt(vw ** 2 + vh ** 2) / diagonal / 25.4;

        // Generated markers are always 200px, but just in case get the actual px
        const n = parseInt(inputs[0][3].value);
        const markers = document.querySelectorAll("#content img");
        const first = markers[0];
        const first_box = first.getBoundingClientRect();
        let measures = [first_box.width / ppmm];
        let next = null;
        let i = 0;

        while (MODE && i < 2 && (next = markers[n ** i])) {
            let next_box = next.getBoundingClientRect();
            measures = measures.concat(
                Math.abs(
                    i
                        ? first_box.bottom - next_box.top
                        : first_box.right - next_box.left
                ) / ppmm
            );
            i++;
        }

        let children = [];
        for (let i = 0; i < measures.length; i++) {
            const msg = document.createElement("div");
            msg.textContent = msgs[i];
            const result = document.createElement("div");
            result.textContent = `${measures[i].toFixed(2)}mm`;
            children = children.concat(msg, result);
        }
        elm.replaceChildren(...children);
    }

    document.querySelector(".form.measure").onsubmit = handleSubmit;

    const obs = new ResizeObserver(() => {
        inputs[1][1].value = window.innerWidth;
        inputs[1][2].value = window.innerHeight;
    });
    obs.observe(document.querySelector("body"));
})();

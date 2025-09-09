function typeText(elementId, text, delay = 100, callback = null) {
    let i = 0;
    function typing() {
        if (i < text.length) {
            document.getElementById(elementId).innerHTML += text.charAt(i);
            i++;
            setTimeout(typing, delay);
        } else if (callback) {
            callback();
        }
    }
    typing();
}

// Run typing sequence
window.onload = function () {
    typeText("line1", "Follow your dreams", 120, function () {
        typeText("line2", "Software for the future", 100, function () {
            typeText("line3", "Your idea, my purpose", 80);
        });
    });
};

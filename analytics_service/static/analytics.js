// analytics.js
// Zero dependencies, beacon-only, no preflight

(function () {
    const ENDPOINT = "http://localhost:5001/collect";

    const payload = JSON.stringify({
        browser: navigator.userAgent
    });

    // sendBeacon sends as text/plain → NO CORS preflight
    navigator.sendBeacon(ENDPOINT, payload);
})();

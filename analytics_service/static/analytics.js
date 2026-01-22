// analytics.js
// Event-streaming web analytics (no dependencies)

(function () {
    const ENDPOINT = "http://localhost:5001/collect";

    // Generate or reuse visitor ID
    function getVisitorId() {
        let id = localStorage.getItem("visitor_id");
        if (!id) {
            id = crypto.randomUUID();
            localStorage.setItem("visitor_id", id);
        }
        return id;
    }

    const visitorId = getVisitorId();
    const sessionId = crypto.randomUUID();
    let currentPage = location.pathname;
    let pageEnterTime = Date.now();

    function send(event, data = {}) {
        const payload = {
            event,
            visitor_id: visitorId,
            session_id: sessionId,
            page: currentPage,
            referrer: document.referrer || null,
            browser: navigator.userAgent,
            screen: `${screen.width}x${screen.height}`,
            timestamp: Date.now(),
            ...data
        };

        navigator.sendBeacon(
            ENDPOINT,
            JSON.stringify(payload)
        );
    }

    /* -------- CORE EVENTS -------- */

    // Page view
    send("page_view");

    // Time-on-page heartbeat (every 10s)
    const heartbeat = setInterval(() => {
        send("heartbeat");
    }, 10000);

    // Track clicks
    document.addEventListener("click", (e) => {
        send("click", {
            tag: e.target.tagName,
            id: e.target.id || null,
            class: e.target.className || null
        });
    });

    // Scroll depth
    let maxScroll = 0;
    window.addEventListener("scroll", () => {
        const scrolled =
            (window.scrollY + window.innerHeight) /
            document.body.scrollHeight;
        maxScroll = Math.max(maxScroll, Math.round(scrolled * 100));
    });

    // Page exit
    window.addEventListener("beforeunload", () => {
        send("page_exit", {
            duration_ms: Date.now() - pageEnterTime,
            scroll_percent: maxScroll
        });
        clearInterval(heartbeat);
    });

})();

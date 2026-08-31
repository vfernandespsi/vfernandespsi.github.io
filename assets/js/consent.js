(function () {
  var STORAGE_KEY = "vf_consent";
  var LANDING_KEY = "vf_landing_url";
  var LANDING_SENT_KEY = "vf_landing_sent";
  var ATTRIBUTION_KEY = "vf_attribution";
  var CONSENT_VERSION = 1;
  var GA_ID = "G-PXV8NTKC6D";
  var CONSENT_SCRIPT = "/assets/js/consent.js?v=3";

  window.dataLayer = window.dataLayer || [];
  function gtag() {
    window.dataLayer.push(arguments);
  }
  window.gtag = gtag;

  gtag("consent", "default", {
    analytics_storage: "denied",
    ad_storage: "denied",
    ad_user_data: "denied",
    ad_personalization: "denied",
    functionality_storage: "denied",
    personalization_storage: "denied",
    security_storage: "granted",
    wait_for_update: 500,
  });

  gtag("js", new Date());

  function inferSourceFromReferrer(referrer) {
    if (!referrer) {
      return "";
    }
    var host = referrer.toLowerCase();
    if (host.indexOf("instagram.com") !== -1 || host.indexOf("l.instagram.com") !== -1) {
      return "instagram";
    }
    if (host.indexOf("facebook.com") !== -1 || host.indexOf("fb.com") !== -1) {
      return "facebook";
    }
    if (host.indexOf("google.") !== -1) {
      return "google";
    }
    if (host.indexOf("bing.com") !== -1) {
      return "bing";
    }
    return "";
  }

  function inferMediumFromReferrer(referrer, source) {
    if (!source) {
      return "";
    }
    if (source === "instagram" || source === "facebook") {
      return "social";
    }
    if (source === "google" || source === "bing") {
      return "organic";
    }
    return "referral";
  }

  function captureAttribution() {
    try {
      if (!sessionStorage.getItem(LANDING_KEY)) {
        sessionStorage.setItem(LANDING_KEY, window.location.href);
      }

      if (sessionStorage.getItem(ATTRIBUTION_KEY)) {
        return;
      }

      var params = new URLSearchParams(window.location.search);
      var referrer = document.referrer || "";
      var source = params.get("utm_source") || "";
      var medium = params.get("utm_medium") || "";
      var campaign = params.get("utm_campaign") || "";
      var content = params.get("utm_content") || "";
      var term = params.get("utm_term") || "";

      if (!source && params.get("fbclid")) {
        source = inferSourceFromReferrer(referrer) || "facebook";
        medium = medium || "social";
      }

      if (!source) {
        source = inferSourceFromReferrer(referrer);
        if (source && !medium) {
          medium = inferMediumFromReferrer(referrer, source);
        }
      }

      if (params.get("gclid")) {
        source = source || "google";
        medium = medium || "cpc";
        campaign = campaign || "google_ads";
      }

      var data = {
        utm_source: source || "(direct)",
        utm_medium: medium || "(none)",
        utm_campaign: campaign || "",
        utm_content: content || "",
        utm_term: term || "",
        landing_page: window.location.pathname + window.location.search,
        landing_url: window.location.href,
        referrer: referrer,
        ts: new Date().toISOString(),
      };

      sessionStorage.setItem(ATTRIBUTION_KEY, JSON.stringify(data));
    } catch (error) {
      /* sessionStorage blocked */
    }
  }

  function readAttribution() {
    try {
      var raw = sessionStorage.getItem(ATTRIBUTION_KEY);
      return raw ? JSON.parse(raw) : null;
    } catch (error) {
      return null;
    }
  }

  function readStoredRaw() {
    try {
      var raw = localStorage.getItem(STORAGE_KEY);
      if (raw) {
        return raw;
      }
      return sessionStorage.getItem(STORAGE_KEY);
    } catch (error) {
      return null;
    }
  }

  function readConsent() {
    try {
      var raw = readStoredRaw();
      if (!raw && window._vfConsentMem) {
        raw = JSON.stringify(window._vfConsentMem);
      }
      if (!raw) {
        return null;
      }
      var data = JSON.parse(raw);
      if (data.v !== CONSENT_VERSION) {
        return null;
      }
      return data;
    } catch (error) {
      return null;
    }
  }

  function saveConsent(analytics) {
    var data = {
      v: CONSENT_VERSION,
      analytics: analytics,
      ts: new Date().toISOString(),
    };
    var json = JSON.stringify(data);
    try {
      localStorage.setItem(STORAGE_KEY, json);
    } catch (error) {
      try {
        sessionStorage.setItem(STORAGE_KEY, json);
      } catch (error2) {
        window._vfConsentMem = data;
      }
    }
    return data;
  }

  function denyAnalytics() {
    window._vfGaLoaded = false;
    try {
      gtag("consent", "update", {
        analytics_storage: "denied",
        ad_storage: "denied",
        ad_user_data: "denied",
        ad_personalization: "denied",
      });
    } catch (error) {
      /* ignore */
    }
  }

  function sendAttributionEvent(att) {
    if (!att) {
      return;
    }
    gtag("event", "session_attribution", {
      source: att.utm_source,
      medium: att.utm_medium,
      campaign: att.utm_campaign || undefined,
      content: att.utm_content || undefined,
      term: att.utm_term || undefined,
      page_referrer: att.referrer || undefined,
      landing_page: att.landing_page || undefined,
    });
  }

  function loadGA() {
    if (window._vfGaLoaded) {
      return;
    }
    window._vfGaLoaded = true;

    gtag("consent", "update", {
      analytics_storage: "granted",
    });

    var script = document.createElement("script");
    script.async = true;
    script.src = "https://www.googletagmanager.com/gtag/js?id=" + GA_ID;
    script.onload = function () {
      var config = {
        anonymize_ip: true,
        allow_google_signals: false,
        allow_ad_personalization_signals: false,
        send_page_view: false,
      };

      var landingUrl = null;
      try {
        landingUrl = sessionStorage.getItem(LANDING_KEY);
      } catch (error) {
        landingUrl = null;
      }

      var landingSent = false;
      try {
        landingSent = sessionStorage.getItem(LANDING_SENT_KEY) === "1";
      } catch (error) {
        landingSent = false;
      }

      if (landingUrl && !landingSent) {
        config.page_location = landingUrl;
        try {
          sessionStorage.setItem(LANDING_SENT_KEY, "1");
        } catch (error) {
          /* ignore */
        }
        gtag("config", GA_ID, config);
        gtag("event", "page_view", { page_location: landingUrl });
        if (landingUrl !== window.location.href) {
          gtag("event", "page_view");
        }
      } else {
        config.send_page_view = true;
        gtag("config", GA_ID, config);
      }

      sendAttributionEvent(readAttribution());
      window.dispatchEvent(new CustomEvent("vf:analytics-ready"));
    };
    document.head.appendChild(script);
  }

  function getBanner() {
    return document.getElementById("vf-consent");
  }

  function isBannerOpen() {
    var banner = getBanner();
    return banner && !banner.classList.contains("is-closed");
  }

  function hideBanner() {
    var banner = getBanner();
    if (!banner) {
      return;
    }
    banner.classList.add("is-closed");
    banner.setAttribute("hidden", "hidden");
    banner.hidden = true;
    banner.style.display = "none";
  }

  function showBanner() {
    var banner = getBanner();
    if (!banner) {
      return;
    }
    banner.classList.remove("is-closed");
    banner.hidden = false;
    banner.removeAttribute("hidden");
    banner.style.display = "";
  }

  function acceptCookies() {
    hideBanner();
    saveConsent(true);
    loadGA();
  }

  function rejectCookies() {
    hideBanner();
    saveConsent(false);
    denyAnalytics();
  }

  function onConsentAction(event, accepted) {
    event.preventDefault();
    event.stopPropagation();
    if (event.stopImmediatePropagation) {
      event.stopImmediatePropagation();
    }
    if (!isBannerOpen()) {
      return;
    }
    if (accepted) {
      acceptCookies();
    } else {
      rejectCookies();
    }
  }

  function bindBannerButtons() {
    var banner = getBanner();
    if (!banner || banner.dataset.vfConsentBound === "1") {
      return;
    }
    banner.dataset.vfConsentBound = "1";

    var acceptBtn = banner.querySelector("#vf-consent-accept, [data-vf-consent-accept]");
    var rejectBtn = banner.querySelector("#vf-consent-reject, [data-vf-consent-reject]");

    if (acceptBtn) {
      acceptBtn.addEventListener("click", function (event) {
        onConsentAction(event, true);
      });
    }

    if (rejectBtn) {
      rejectBtn.addEventListener("click", function (event) {
        onConsentAction(event, false);
      });
    }
  }

  function bindOpenLinks() {
    document.addEventListener("click", function (event) {
      var link = event.target.closest("[data-vf-open-consent]");
      if (!link) {
        return;
      }
      event.preventDefault();
      showBanner();
    });
  }

  function init() {
    captureAttribution();
    bindBannerButtons();
    bindOpenLinks();

    var stored = readConsent();
    if (stored) {
      if (stored.analytics) {
        loadGA();
      } else {
        denyAnalytics();
      }
      hideBanner();
      return;
    }

    showBanner();
  }

  window.vfConsent = {
    open: function () {
      showBanner();
    },
    accept: acceptCookies,
    reject: rejectCookies,
    get: readConsent,
    getAttribution: readAttribution,
    version: CONSENT_VERSION,
    script: CONSENT_SCRIPT,
  };

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();

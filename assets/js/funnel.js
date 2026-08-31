(function () {
  var pendingEvents = [];

  function getSonoBookingUrl() {
    var config = window.VF || {};
    var url = config.bookingSonoUrl || "/psicologia-do-sono/";
    if (typeof url !== "string" || !url) {
      return "/psicologia-do-sono/";
    }
    if (url.indexOf("/marcar") !== -1 && url.indexOf("servico=sono") !== -1) {
      return "/psicologia-do-sono/";
    }
    return url;
  }

  function track(name, params) {
    if (window._vfGaLoaded && typeof gtag === "function") {
      gtag("event", name, params || {});
      return;
    }
    if (window._vfGaLoaded === false) {
      return;
    }
    pendingEvents.push({ name: name, params: params || {} });
  }

  window.addEventListener("vf:analytics-ready", function () {
    pendingEvents.forEach(function (item) {
      gtag("event", item.name, item.params);
    });
    pendingEvents = [];
  });

  document.addEventListener("click", function (event) {
    var link = event.target.closest("[data-track]");
    if (!link) {
      return;
    }
    track(link.getAttribute("data-track"), {
      location: link.getAttribute("data-track-location") || window.location.pathname,
      label: (link.textContent || "").trim().slice(0, 80)
    });
  });

  function initCityFilter() {
    var localizacao = document.getElementById("localizacao");
    if (!localizacao) {
      return;
    }

    var serviceChips = localizacao.querySelectorAll("[data-service-filter]");
    var cityChips = localizacao.querySelectorAll("[data-city-filter]");
    var cards = localizacao.querySelectorAll("[data-city]");
    if (!cards.length) {
      return;
    }

    var selectedService = "avaliacao";
    var selectedCity = "all";

    function citiesForService(service) {
      var available = {};
      cards.forEach(function (card) {
        var services = (card.getAttribute("data-services") || "avaliacao").split(",");
        if (services.indexOf(service) !== -1) {
          available[card.getAttribute("data-city")] = true;
        }
      });
      return available;
    }

    function animateVisibleCards() {
      cards.forEach(function (card) {
        if (card.hidden) {
          return;
        }
        card.classList.remove("is-filter-animate");
        void card.offsetWidth;
        card.classList.add("is-filter-animate");
      });
    }

    function syncCityChips() {
      if (!cityChips.length) {
        return;
      }
      var available = citiesForService(selectedService);
      cityChips.forEach(function (chip) {
        var city = chip.getAttribute("data-city-filter");
        chip.hidden = city !== "all" && !available[city];
      });
      if (selectedCity !== "all" && !available[selectedCity]) {
        selectedCity = "all";
        cityChips.forEach(function (item) {
          item.classList.toggle("is-active", item.getAttribute("data-city-filter") === "all");
        });
      }
    }

    function applyFilters(animate) {
      syncCityChips();
      cards.forEach(function (card) {
        var city = card.getAttribute("data-city");
        var services = (card.getAttribute("data-services") || "avaliacao").split(",");
        var cityOk = selectedCity === "all" || city === selectedCity;
        var serviceOk = services.indexOf(selectedService) !== -1;
        card.hidden = !(cityOk && serviceOk);
      });
      if (animate) {
        animateVisibleCards();
      }
    }

    serviceChips.forEach(function (chip) {
      chip.addEventListener("click", function () {
        selectedService = chip.getAttribute("data-service-filter");
        serviceChips.forEach(function (item) {
          item.classList.toggle("is-active", item === chip);
        });
        track("localizacao", { service: selectedService });
        applyFilters(true);
      });
    });

    cityChips.forEach(function (chip) {
      chip.addEventListener("click", function () {
        selectedCity = chip.getAttribute("data-city-filter");
        cityChips.forEach(function (item) {
          item.classList.toggle("is-active", item === chip);
        });
        track("localizacao", { city: selectedCity, service: selectedService });
        applyFilters(true);
      });
    });

    applyFilters(false);
  }

  function initSonoBookingLinks() {
    var links = document.querySelectorAll("[data-sono-booking]");
    if (!links.length) {
      return;
    }
    var url = getSonoBookingUrl();
    var onSonoPage = document.documentElement.classList.contains("page-sono");
    var samePage =
      onSonoPage &&
      (url === "/psicologia-do-sono/" ||
        url === window.location.pathname ||
        url.replace(/\/$/, "") === window.location.pathname.replace(/\/$/, ""));
    var consultasWhatsApp =
      "https://api.whatsapp.com/send?phone=351914166181&text=" +
      encodeURIComponent("Gostaria de marcar consulta de psicologia do sono.");
    links.forEach(function (link) {
      if (samePage && link.closest("#consultas")) {
        link.setAttribute("href", consultasWhatsApp);
        link.classList.remove("page-scroll");
        link.setAttribute("rel", "noopener");
        link.setAttribute("target", "_blank");
        return;
      }
      if (samePage) {
        link.setAttribute("href", "#consultas");
        link.classList.add("page-scroll");
        return;
      }
      link.setAttribute("href", url);
    });
  }

  function initTriage() {
    var form = document.getElementById("triage-form");
    if (!form) {
      return;
    }

    var isSonoPage = document.documentElement.classList.contains("page-sono");
    var result = document.getElementById("triage-result");
    var resultText = document.getElementById("triage-result-text");
    var questions = form.querySelectorAll(".triage-question");

    form.addEventListener("click", function (event) {
      var button = event.target.closest("[data-triage-answer]");
      if (!button) {
        return;
      }
      var group = button.parentElement;
      group.querySelectorAll("button").forEach(function (item) {
        item.classList.toggle("is-active", item === button);
      });
      updateTriage();
    });

    function updateTriage() {
      var answers = [];
      questions.forEach(function (question) {
        var active = question.querySelector("button.is-active");
        if (active) {
          answers.push(active.getAttribute("data-triage-answer"));
        }
      });
      if (answers.length < questions.length) {
        result.hidden = true;
        return;
      }
      var yesCount = answers.filter(function (value) {
        return value === "yes";
      }).length;
      if (yesCount >= 1) {
        resultText.textContent = isSonoPage
          ? "Pelos dados indicados, uma consulta de psicologia do sono poderá ser adequada. Esta triagem não substitui uma consulta médica nem estabelece um diagnóstico."
          : "Pelos dados indicados, uma avaliação neuropsicológica poderá ser adequada. Esta triagem não substitui uma consulta médica nem estabelece um diagnóstico.";
      } else {
        resultText.textContent = isSonoPage
          ? "Se a dúvida se mantém, pode marcar para esclarecer se a consulta é indicada. Esta triagem não substitui uma consulta médica nem estabelece um diagnóstico."
          : "Se a dúvida se mantém, pode marcar para esclarecer se a avaliação é indicada. Esta triagem não substitui uma consulta médica nem estabelece um diagnóstico.";
      }
      result.hidden = false;
      track("triagem", { yes_count: yesCount });
    }
  }

  function initBooking() {
    var cityButtons = document.querySelectorAll("[data-book-city]");
    var serviceButtons = document.querySelectorAll("[data-book-service]");
    var venues = document.querySelectorAll("[data-book-venue]");
    var venuesWrap = document.getElementById("booking-venues");
    var emptyNote = document.getElementById("booking-empty");
    var citiesWrap = document.getElementById("booking-cities");
    var sonoPanel = document.getElementById("booking-sono-panel");
    var notePresencial = document.getElementById("booking-note-presencial");
    var doubtPresencial = document.getElementById("booking-doubt-presencial");
    if (!venues.length) {
      return;
    }

    var selectedCity = "";
    var selectedService = "avaliacao";
    var params = new URLSearchParams(window.location.search);
    var fromQuery = params.get("servico");
    if (fromQuery === "sono") {
      window.location.replace(getSonoBookingUrl());
      return;
    }
    if (fromQuery === "estimulacao" || fromQuery === "avaliacao") {
      selectedService = fromQuery;
    }

    function isSono() {
      return selectedService === "sono";
    }

    function citiesForService(service) {
      var available = {};
      venues.forEach(function (venue) {
        var services = (venue.getAttribute("data-services") || "").split(",");
        if (services.indexOf(service) !== -1) {
          available[venue.getAttribute("data-city")] = true;
        }
      });
      return available;
    }

    function syncCityChips() {
      var available = citiesForService(selectedService);
      cityButtons.forEach(function (button) {
        var city = button.getAttribute("data-book-city");
        button.hidden = !available[city];
      });

      if (!available[selectedCity]) {
        selectedCity = "";
        cityButtons.forEach(function (item) {
          item.classList.remove("is-active");
        });
      }

      if (selectedService === "estimulacao" && available.braga) {
        selectedCity = "braga";
        cityButtons.forEach(function (item) {
          item.classList.toggle("is-active", item.getAttribute("data-book-city") === "braga");
        });
      }
    }

    function syncServiceChips() {
      serviceButtons.forEach(function (item) {
        item.classList.toggle(
          "is-active",
          item.getAttribute("data-book-service") === selectedService
        );
      });
    }

    function render() {
      syncCityChips();
      var sono = isSono();
      if (citiesWrap) {
        citiesWrap.hidden = sono;
      }
      if (sonoPanel) {
        sonoPanel.hidden = !sono;
      }
      if (notePresencial) {
        notePresencial.hidden = sono;
      }
      if (doubtPresencial) {
        doubtPresencial.hidden = sono;
      }
      if (sono) {
        venues.forEach(function (venue) {
          venue.hidden = true;
        });
        if (venuesWrap) {
          venuesWrap.hidden = true;
        }
        if (emptyNote) {
          emptyNote.hidden = true;
        }
        return;
      }
      var visible = 0;
      venues.forEach(function (venue) {
        var cityOk = !selectedCity || venue.getAttribute("data-city") === selectedCity;
        var services = (venue.getAttribute("data-services") || "").split(",");
        var serviceOk = services.indexOf(selectedService) !== -1;
        var show = cityOk && serviceOk;
        venue.hidden = !show;
        if (show) {
          visible += 1;
        }
      });
      if (venuesWrap) {
        venuesWrap.hidden = visible === 0;
      }
      if (emptyNote) {
        emptyNote.hidden = visible !== 0 || !selectedCity;
      }
    }

    cityButtons.forEach(function (button) {
      button.addEventListener("click", function () {
        selectedCity = button.getAttribute("data-book-city");
        cityButtons.forEach(function (item) {
          item.classList.toggle("is-active", item === button);
        });
        track("localizacao", { city: selectedCity, context: "marcar" });
        render();
      });
    });

    serviceButtons.forEach(function (button) {
      button.addEventListener("click", function () {
        selectedService = button.getAttribute("data-book-service");
        syncServiceChips();
        track("servico", { service: selectedService });
        render();
      });
    });

    if (serviceButtons.length) {
      syncServiceChips();
    }
    render();
  }

  function initBookingModal() {
    var modal = document.getElementById("vf-booking-modal");
    if (!modal) {
      return;
    }

    var panel = modal.querySelector(".vf-booking-modal__panel");
    var openers = document.querySelectorAll("[data-open-booking-modal]");
    var closers = modal.querySelectorAll("[data-close-booking-modal]");
    var choices = modal.querySelectorAll("[data-booking-choice]");
    var lastFocus = null;

    function getBookingUrl(choice) {
      if (choice === "sono") {
        return getSonoBookingUrl();
      }
      return (window.VF && window.VF.bookingNeuroUrl) || "/marcar/";
    }

    function openModal() {
      lastFocus = document.activeElement;
      modal.hidden = false;
      document.body.classList.add("vf-booking-modal-open");
      var firstChoice = modal.querySelector("[data-booking-choice]");
      if (firstChoice) {
        firstChoice.focus();
      }
    }

    function closeModal() {
      modal.hidden = true;
      document.body.classList.remove("vf-booking-modal-open");
      if (lastFocus && typeof lastFocus.focus === "function") {
        lastFocus.focus();
      }
    }

    openers.forEach(function (button) {
      button.addEventListener("click", function (event) {
        if (event.cancelable) {
          event.preventDefault();
        }
        openModal();
      });
    });

    closers.forEach(function (button) {
      button.addEventListener("click", function () {
        closeModal();
      });
    });

    choices.forEach(function (button) {
      button.addEventListener("click", function () {
        var choice = button.getAttribute("data-booking-choice");
        track("marcar_modal", { choice: choice });
        window.location.href = getBookingUrl(choice);
      });
    });

    modal.addEventListener("keydown", function (event) {
      if (event.key === "Escape") {
        closeModal();
        return;
      }
      if (event.key !== "Tab" || !panel) {
        return;
      }
      var focusable = panel.querySelectorAll(
        'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
      );
      if (!focusable.length) {
        return;
      }
      var first = focusable[0];
      var last = focusable[focusable.length - 1];
      if (event.shiftKey && document.activeElement === first) {
        event.preventDefault();
        last.focus();
      } else if (!event.shiftKey && document.activeElement === last) {
        event.preventDefault();
        first.focus();
      }
    });
  }

  function initTriageReveal() {
    var triggers = document.querySelectorAll("[data-reveal-triage]");
    var section = document.getElementById("triagem");
    if (!triggers.length || !section) {
      return;
    }

    triggers.forEach(function (trigger) {
      trigger.addEventListener("click", function (event) {
        event.preventDefault();
        section.classList.add("is-visible");
        section.scrollIntoView({ behavior: "smooth", block: "start" });
        var firstButton = section.querySelector("[data-triage-answer]");
        if (firstButton) {
          window.setTimeout(function () {
            firstButton.focus();
          }, 400);
        }
        track("triagem_open", { location: "hero" });
      });
    });
  }

  initCityFilter();
  initSonoBookingLinks();
  initTriage();
  initBooking();
  initBookingModal();
  initTriageReveal();
})();

(function () {
  function track(name, params) {
    if (typeof gtag === "function") {
      gtag("event", name, params || {});
    }
  }

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
    var chips = document.querySelectorAll("[data-city-filter]");
    var cards = document.querySelectorAll("[data-city]");
    if (!chips.length || !cards.length) {
      return;
    }

    chips.forEach(function (chip) {
      chip.addEventListener("click", function () {
        var city = chip.getAttribute("data-city-filter");
        chips.forEach(function (item) {
          item.classList.toggle("is-active", item === chip);
        });
        cards.forEach(function (card) {
          var match = city === "all" || card.getAttribute("data-city") === city;
          card.hidden = !match;
        });
        track("localizacao", { city: city });
      });
    });
  }

  function initTriage() {
    var form = document.getElementById("triage-form");
    if (!form) {
      return;
    }

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
        resultText.textContent =
          "Pelos dados indicados, uma avaliação neuropsicológica poderá ser adequada. Esta triagem não substitui uma consulta médica nem estabelece um diagnóstico.";
      } else {
        resultText.textContent =
          "Se a dúvida se mantém, pode marcar para esclarecer se a avaliação é indicada. Esta triagem não substitui uma consulta médica nem estabelece um diagnóstico.";
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
    if (!cityButtons.length || !venues.length) {
      return;
    }

    var selectedCity = "";
    var selectedService = "avaliacao";

    function render() {
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
        serviceButtons.forEach(function (item) {
          item.classList.toggle("is-active", item === button);
        });
        track("servico", { service: selectedService });
        render();
      });
    });
  }

  initCityFilter();
  initTriage();
  initBooking();
})();

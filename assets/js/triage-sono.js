(function () {
  var QUESTIONNAIRE = "sono-isi";
  var TOTAL_QUESTIONS = 7;
  var RECOMMENDATION_THRESHOLD = 14;
  var pendingEvents = [];
  var started = false;

  function track(name, params) {
    var payload = params || {};
    if (window._vfGaLoaded && typeof gtag === "function") {
      gtag("event", name, payload);
      return;
    }
    if (window._vfGaLoaded === false) {
      return;
    }
    pendingEvents.push({ name: name, params: payload });
  }

  window.addEventListener("vf:analytics-ready", function () {
    pendingEvents.forEach(function (item) {
      gtag("event", item.name, item.params);
    });
    pendingEvents = [];
  });

  function initSonoScreening() {
    var form = document.getElementById("sono-isi-form");
    if (!form) {
      return;
    }

    var result = document.getElementById("sono-isi-result");
    var scoreEl = document.getElementById("sono-isi-score");
    var questions = form.querySelectorAll(".triage-question");

    track("triagem_sono_view", {
      questionnaire: QUESTIONNAIRE,
      total_questions: TOTAL_QUESTIONS,
      location: window.location.pathname
    });

    form.addEventListener("click", function (event) {
      var button = event.target.closest("[data-sono-score]");
      if (!button) {
        return;
      }

      var question = button.closest(".triage-question");
      var questionIndex = question
        ? Array.prototype.indexOf.call(questions, question) + 1
        : 0;
      var wasActive = button.classList.contains("is-active");

      var group = button.parentElement;
      group.querySelectorAll("[data-sono-score]").forEach(function (item) {
        item.classList.toggle("is-active", item === button);
      });

      if (!started) {
        started = true;
        track("triagem_sono_start", {
          questionnaire: QUESTIONNAIRE,
          question_index: questionIndex,
          location: window.location.pathname
        });
      }

      if (!wasActive) {
        var answeredCount = 0;
        questions.forEach(function (item) {
          if (item.querySelector("[data-sono-score].is-active")) {
            answeredCount += 1;
          }
        });
        track("triagem_sono_progress", {
          questionnaire: QUESTIONNAIRE,
          answered_count: answeredCount,
          total_questions: TOTAL_QUESTIONS,
          question_index: questionIndex,
          location: window.location.pathname
        });
      }

      updateSonoScreening();
    });

    function updateSonoScreening() {
      var scores = [];
      questions.forEach(function (question) {
        var active = question.querySelector("[data-sono-score].is-active");
        if (active) {
          scores.push(Number(active.getAttribute("data-sono-score")));
        }
      });

      if (scores.length < questions.length) {
        result.hidden = true;
        return;
      }

      var total = scores.reduce(function (sum, value) {
        return sum + value;
      }, 0);
      var needsConsultation = total >= RECOMMENDATION_THRESHOLD;

      scoreEl.textContent = String(total);

      result.hidden = false;
      result.scrollIntoView({ behavior: "smooth", block: "nearest" });

      track("triagem_sono_complete", {
        questionnaire: QUESTIONNAIRE,
        score: total,
        needs_consultation: needsConsultation,
        answered_count: scores.length,
        total_questions: TOTAL_QUESTIONS,
        location: window.location.pathname
      });
    }
  }

  initSonoScreening();
})();

(function () {
  var QUESTIONNAIRE = "memoria";
  var TOTAL_QUESTIONS = 10;
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

  function initMemoryScreening() {
    var form = document.getElementById("neuro-memory-form");
    if (!form) {
      return;
    }

    var result = document.getElementById("neuro-memory-result");
    var scoreEl = document.getElementById("neuro-memory-score");
    var questions = form.querySelectorAll(".triage-question");

    track("triagem_neuro_view", {
      questionnaire: QUESTIONNAIRE,
      total_questions: TOTAL_QUESTIONS,
      location: window.location.pathname
    });

    form.addEventListener("click", function (event) {
      var button = event.target.closest("[data-neuro-score]");
      if (!button) {
        return;
      }

      var question = button.closest(".triage-question");
      var questionIndex = question
        ? Array.prototype.indexOf.call(questions, question) + 1
        : 0;
      var wasActive = button.classList.contains("is-active");

      var group = button.parentElement;
      group.querySelectorAll("[data-neuro-score]").forEach(function (item) {
        item.classList.toggle("is-active", item === button);
      });

      if (!started) {
        started = true;
        track("triagem_neuro_start", {
          questionnaire: QUESTIONNAIRE,
          question_index: questionIndex,
          location: window.location.pathname
        });
      }

      if (!wasActive) {
        var answeredCount = 0;
        questions.forEach(function (item) {
          if (item.querySelector("[data-neuro-score].is-active")) {
            answeredCount += 1;
          }
        });
        track("triagem_neuro_progress", {
          questionnaire: QUESTIONNAIRE,
          answered_count: answeredCount,
          total_questions: TOTAL_QUESTIONS,
          question_index: questionIndex,
          location: window.location.pathname
        });
      }

      updateMemoryScreening();
    });

    function updateMemoryScreening() {
      var scores = [];
      questions.forEach(function (question) {
        var active = question.querySelector("[data-neuro-score].is-active");
        if (active) {
          scores.push(Number(active.getAttribute("data-neuro-score")));
        }
      });

      if (scores.length < questions.length) {
        result.hidden = true;
        return;
      }

      var total = scores.reduce(function (sum, value) {
        return sum + value;
      }, 0);
      var needsInvestigation = total > 4;

      scoreEl.textContent = String(total);

      result.hidden = false;
      result.scrollIntoView({ behavior: "smooth", block: "nearest" });

      track("triagem_memoria_complete", {
        questionnaire: QUESTIONNAIRE,
        score: total,
        needs_investigation: needsInvestigation,
        answered_count: scores.length,
        total_questions: TOTAL_QUESTIONS,
        location: window.location.pathname
      });
    }
  }

  initMemoryScreening();
})();

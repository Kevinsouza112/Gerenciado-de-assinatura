(() => {
  const emailInput = document.getElementById("email");
  const emailSuggestion = document.getElementById("email-domain-suggestion");
  const passwordInput = document.getElementById("senha");
  const confirmInput = document.getElementById("confirmar_senha");
  const passwordFeedback = document.getElementById("password-match-feedback");
  const domains = ["gmail.com", "hotmail.com", "outlook.com", "yahoo.com"];

  if (!emailInput || !emailSuggestion || !passwordInput || !confirmInput || !passwordFeedback) {
    return;
  }

  const renderEmailSuggestion = () => {
    const value = emailInput.value.trim();
    const atIndex = value.indexOf("@");

    if (atIndex === -1 || value.indexOf(".", atIndex) !== -1) {
      emailSuggestion.replaceChildren();
      return;
    }

    const local = value.slice(0, atIndex);
    const typedDomain = value.slice(atIndex + 1).toLowerCase();
    if (!local || !typedDomain) {
      emailSuggestion.replaceChildren();
      return;
    }

    const match = domains.find((domain) => domain.startsWith(typedDomain));
    if (!match || match === typedDomain) {
      emailSuggestion.replaceChildren();
      return;
    }

    const suggestion = `${local}@${match}`;
    const button = document.createElement("button");
    button.className = "btn btn-link btn-sm p-0 fw-bold";
    button.type = "button";
    button.textContent = `Usar ${suggestion}`;
    button.addEventListener("click", () => {
      emailInput.value = suggestion;
      emailSuggestion.replaceChildren();
      emailInput.focus();
    });
    emailSuggestion.replaceChildren(button);
  };

  const renderPasswordMatch = () => {
    if (!confirmInput.value) {
      passwordFeedback.textContent = "";
      confirmInput.classList.remove("is-valid", "is-invalid");
      return;
    }

    if (passwordInput.value === confirmInput.value) {
      passwordFeedback.textContent = "As senhas conferem.";
      confirmInput.classList.remove("is-invalid");
      confirmInput.classList.add("is-valid");
    } else {
      passwordFeedback.textContent = "As senhas ainda nao conferem.";
      confirmInput.classList.remove("is-valid");
      confirmInput.classList.add("is-invalid");
    }
  };

  emailInput.addEventListener("input", renderEmailSuggestion);
  passwordInput.addEventListener("input", renderPasswordMatch);
  confirmInput.addEventListener("input", renderPasswordMatch);
})();

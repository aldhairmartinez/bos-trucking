/* ==========================================================================
   QUOTE FORM — mode switch + accessible client-side validation
   --------------------------------------------------------------------------
   The form has two modes, Material Delivery and Truck Parking, which swap the
   middle set of fields. Notes:

   * Mode is reflected in the URL (?type=parking) so "Check Availability"
     links can deep-link straight into the parking fields.
   * Hidden field sets get the `disabled` attribute as well as being hidden, so
     their values are never submitted and they leave the tab order.
   * Native constraint validation does the checking; this file only supplies
     readable messages and moves focus to the first problem.

   NO SUBMISSION BACKEND IS WIRED YET. The <form> has no live action; see
   docs/forms.md for the Wix Forms and Cloudflare options and exactly which
   fields each one needs.
   ========================================================================== */
(function () {
  "use strict";

  const form = document.querySelector("[data-quote-form]");
  if (!form) return;

  const status = form.querySelector("[data-form-status]");
  const groups = Array.from(form.querySelectorAll("[data-mode-group]"));
  const radios = Array.from(form.querySelectorAll('input[name="requestType"]'));

  /* ---- Mode switching --------------------------------------------------- */
  function applyMode(mode, pushUrl) {
    groups.forEach((group) => {
      const active = group.dataset.modeGroup === mode;
      group.hidden = !active;
      // Disabling keeps hidden values out of the payload and out of tab order.
      group
        .querySelectorAll("input, select, textarea")
        .forEach((el) => {
          el.disabled = !active;
          if (!active) clearError(el);
        });
    });

    const heading = form.querySelector("[data-mode-heading]");
    if (heading) {
      heading.textContent =
        mode === "parking"
          ? "Tell us about your vehicle"
          : "Tell us about your material";
    }

    if (pushUrl && window.history && window.history.replaceState) {
      const url = new URL(window.location.href);
      url.searchParams.set("type", mode);
      window.history.replaceState({}, "", url);
    }
  }

  radios.forEach((radio) =>
    radio.addEventListener("change", () => {
      if (radio.checked) applyMode(radio.value, true);
    })
  );

  // Honour ?type=parking / ?type=material on load.
  const requested = new URLSearchParams(window.location.search).get("type");
  const initial =
    requested === "parking" || requested === "material"
      ? requested
      : (radios.find((r) => r.checked) || {}).value || "material";
  const initialRadio = radios.find((r) => r.value === initial);
  if (initialRadio) initialRadio.checked = true;
  applyMode(initial, false);

  /* ---- Validation messaging --------------------------------------------- */
  const LABELS = {
    valueMissing: (name) => `${name} is required.`,
    typeMismatch: () => "Please enter a valid email address, e.g. name@example.com.",
    tooShort: (name) => `${name} is too short.`,
    patternMismatch: (name) => `Please check the format of ${name.toLowerCase()}.`,
  };

  function fieldName(input) {
    const wrap = input.closest(".field");
    const label = wrap && wrap.querySelector("label");
    if (!label) return "This field";
    return label.textContent.replace(/\*|\(optional\)/g, "").trim();
  }

  function errorNode(input) {
    const wrap = input.closest(".field");
    return wrap ? wrap.querySelector(".field__error") : null;
  }

  function showError(input) {
    const wrap = input.closest(".field");
    const node = errorNode(input);
    if (!wrap || !node) return;

    const v = input.validity;
    let msg = "Please check this field.";
    if (v.valueMissing) msg = LABELS.valueMissing(fieldName(input));
    else if (v.typeMismatch) msg = LABELS.typeMismatch();
    else if (v.tooShort) msg = LABELS.tooShort(fieldName(input));
    else if (v.patternMismatch) msg = LABELS.patternMismatch(fieldName(input));

    node.textContent = msg;
    wrap.classList.add("has-error");
    input.setAttribute("aria-invalid", "true");
    if (node.id) input.setAttribute("aria-describedby", node.id);
  }

  function clearError(input) {
    const wrap = input.closest(".field");
    if (!wrap) return;
    wrap.classList.remove("has-error");
    input.removeAttribute("aria-invalid");
    const node = errorNode(input);
    if (node) node.textContent = "";
  }

  form.querySelectorAll("input, select, textarea").forEach((input) => {
    input.addEventListener("blur", () => {
      if (input.disabled || !input.willValidate) return;
      if (input.value.trim() === "" && !input.required) {
        clearError(input);
        return;
      }
      input.checkValidity() ? clearError(input) : showError(input);
    });
    input.addEventListener("input", () => {
      if (input.closest(".field") && input.closest(".field").classList.contains("has-error")) {
        if (input.checkValidity()) clearError(input);
      }
    });
  });

  /* ---- Submit ----------------------------------------------------------- */
  form.setAttribute("novalidate", "novalidate");

  form.addEventListener("submit", (e) => {
    const fields = Array.from(form.querySelectorAll("input, select, textarea")).filter(
      (el) => !el.disabled && el.willValidate
    );

    let firstBad = null;
    fields.forEach((input) => {
      if (input.checkValidity()) {
        clearError(input);
      } else {
        showError(input);
        if (!firstBad) firstBad = input;
      }
    });

    if (firstBad) {
      e.preventDefault();
      if (status) {
        status.className = "form-status form-status--error";
        status.textContent =
          "Please correct the highlighted fields, or just call or text 239-900-6374.";
      }
      firstBad.focus();
      firstBad.scrollIntoView({ block: "center", behavior: "smooth" });
      return;
    }

    // Spam honeypot: a bot filled a field no human can see.
    const hp = form.querySelector('input[name="_hp"]');
    if (hp && hp.value !== "") {
      e.preventDefault();
      return;
    }

    // No endpoint is wired yet. Rather than silently appear to work, tell the
    // visitor plainly and keep the phone number in front of them.
    const action = (form.getAttribute("action") || "").trim();
    if (!action || action === "#") {
      e.preventDefault();
      if (status) {
        status.className = "form-status form-status--info";
        status.innerHTML =
          "<strong>Preview mode.</strong> Online form delivery is not connected yet. " +
          'To reach B.O.S. right now, call or text <a href="tel:+12399006374">239-900-6374</a> ' +
          'or email <a href="mailto:bostruckingsite@gmail.com">bostruckingsite@gmail.com</a>.';
        status.focus();
        status.scrollIntoView({ block: "center", behavior: "smooth" });
      }
    }
  });
})();

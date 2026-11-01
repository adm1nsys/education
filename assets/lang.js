// DE/EN switch. Pages are written in German; elements carry their English text in
// data-en (plain text) or data-en-html (markup). The choice is remembered per browser.
(function () {
  const KEY = "education-lang";
  const root = document.documentElement;
  const nodes = document.querySelectorAll("[data-en],[data-en-html]");
  const titleDe = document.title;

  let lang = "de";
  try { lang = localStorage.getItem(KEY) === "en" ? "en" : "de"; } catch (e) { /* storage blocked */ }

  const toggle = document.createElement("button");
  toggle.type = "button";
  toggle.className = "lang-toggle";
  toggle.innerHTML = '<span data-l="de">DE</span><span data-l="en">EN</span>';
  document.body.appendChild(toggle);

  function apply(next) {
    lang = next;
    root.lang = next;
    nodes.forEach((el) => {
      if (el.dataset.de === undefined) el.dataset.de = el.innerHTML;
      if (next === "de") el.innerHTML = el.dataset.de;
      else if (el.dataset.enHtml !== undefined) el.innerHTML = el.dataset.enHtml;
      else el.textContent = el.dataset.en;
    });
    document.title = next === "en" && root.dataset.titleEn ? root.dataset.titleEn : titleDe;
    toggle.dataset.active = next;
    toggle.setAttribute("aria-label", next === "de" ? "Switch to English" : "Auf Deutsch umschalten");
  }

  toggle.addEventListener("click", () => {
    apply(lang === "de" ? "en" : "de");
    try { localStorage.setItem(KEY, lang); } catch (e) { /* storage blocked */ }
  });

  apply(lang);
})();

/* Console enhancements. Everything already works without this file
   (radio buttons + CSS). This only adds:
   - ←/→ (or A/D) anywhere on the page to swap cartridges
   - Enter to "press start" while the console has focus
   - swipe left/right on the TV */
(() => {
  const deck = document.querySelector(".deck");
  if (!deck) return;
  const radios = [...deck.querySelectorAll(".cart-radio")];
  if (!radios.length) return;

  const current = () => radios.findIndex((r) => r.checked);
  const select = (i) => {
    const r = radios[(i + radios.length) % radios.length];
    r.checked = true;
    if (deck.contains(document.activeElement)) r.focus({ preventScroll: true });
  };
  const step = (d) => select(current() + d);
  const start = () => { window.location.href = radios[current()].dataset.href; };

  document.addEventListener("keydown", (e) => {
    if (e.altKey || e.ctrlKey || e.metaKey) return;
    const t = e.target;
    if (t.closest("input:not(.cart-radio), textarea, select, [contenteditable]")) return;
    // Focused radios already handle arrows natively.
    const onRadio = t.classList && t.classList.contains("cart-radio");
    if (!onRadio && (e.key === "ArrowLeft" || e.key === "a")) { e.preventDefault(); step(-1); }
    else if (!onRadio && (e.key === "ArrowRight" || e.key === "d")) { e.preventDefault(); step(1); }
    else if (e.key === "Enter" && (onRadio || t === document.body)) { e.preventDefault(); start(); }
  });

  const tv = deck.querySelector(".tv");
  let x0 = null;
  tv.addEventListener("touchstart", (e) => { x0 = e.touches[0].clientX; }, { passive: true });
  tv.addEventListener("touchend", (e) => {
    if (x0 === null) return;
    const dx = e.changedTouches[0].clientX - x0;
    if (Math.abs(dx) > 40) step(dx < 0 ? 1 : -1);
    x0 = null;
  });
})();

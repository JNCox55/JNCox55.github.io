Title: Building This Site: Cartridges, CRTs, and Zero Frameworks
Date: 2026-09-27 20:00
Tags: meta, web, css
Category: Tech
Summary: How the home page console works using radio buttons, the CSS :has() selector, and a sprinkle of vanilla JavaScript for keyboard controls.
Cover: images/covers/build.svg
Cart_color: #89b482

The console on the home page is mostly **HTML and CSS**. Here's how.

## Radio buttons are state machines

Each cartridge is a `<label>` for a hidden radio button. Only one radio can be checked, which is exactly how a cartridge slot works.

```css
.deck:has(#cart-2:checked) [data-slot="2"] {
  /* this cartridge drops into the slot */
}
```

## The CRT boot animation is free

The preview panel for each cartridge is `display: none` until selected. CSS animations restart when an element becomes displayed, so every cartridge swap replays the power-on effect. No JavaScript needed.

## Where JavaScript *is* used

- Arrow keys and swipe gestures on the console
- The search page, which filters a JSON index generated at build time

That's it. About 100 lines total.

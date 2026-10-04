A toast reports the result of an action the person just took and leaves by itself.

- Markup: `<div class="toast" role="status">`; `danger` with `role="alert"` for a failure. Optional one action: Undo or Retry.
- At most three at once, each for 8 seconds; errors stay until dismissed. One implementation for the core and all modules.
- Position: bottom right on a computer, above the taskbar on a phone.
- Long-running work is not a toast: it goes to the Tasks menu.

A dialog asks for a decision or collects the parameters of one operation.

- Sizes: default 480px (confirmation), `form` 640px, `details` 960px. On a phone every dialog is a full-width bottom sheet.
- Structure: `.dialog-head` with the title as a question or the name of the operation, body, `.dialog-foot` with Cancel first and the confirming button last.
- ONE confirmation pattern replaces the six in the old interface. Simple and reversible: Cancel + verb. Destructive: Cancel + `danger` button that repeats the verb and object ("Remove task"). System operations (storage, network, updates): the three steps Parameters → Plan → Confirm, where Plan lists in plain words what will change and what stays.
- Never "Yes / No" or "OK": the button says what will happen.
- A dialog with unsaved input asks before closing. While the operation runs the dialog shows the Waiting state and cannot be closed.
- Always opaque, on `scrim`.

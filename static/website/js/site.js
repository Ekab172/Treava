"use strict";

// Django renders validation errors and preserves the submitted values.
const firstInvalid = document.querySelector('[aria-invalid="true"]');
if (firstInvalid) firstInvalid.focus();


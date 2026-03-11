## Description

<!-- Describe what file type you are adding and why it is useful. -->

**Format name:** <!-- e.g. XCF (GIMP image) -->  
**MIME type:** <!-- e.g. image/x-xcf -->  
**Typical extensions:** <!-- e.g. .xcf -->  
**Magic bytes source:** <!-- URL to official spec or reference -->

## Checklist

- [ ] `@register` decorator is present on the class
- [ ] `name`, `mime_type`, and `extensions` class attributes are set
- [ ] Magic bytes are sourced from an official specification (link provided above)
- [ ] `match()` returns `False` for a zero-filled 262-byte buffer
- [ ] At least one positive **and** one negative test case are included
- [ ] `pytest` passes locally with no failures

## Notes

<!-- Anything else reviewers should know, e.g. edge cases, related formats, ordering considerations. -->

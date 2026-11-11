---
name: vividsites-library
description: Retrieve public VividSites components marked free in the component registry. Does not retrieve paid templates or build prompts.
---

# VividSites free components

This plugin reads the public component registry only. A result is a component, not a website template and not a build prompt.

## Use

1. Call `list_free_components` to see components whose `meta.free` value is boolean true.
2. Call `get_free_component` with a slug from that list. Use the returned file content as component source.

If a call returns an error, say so. Do not invent a component, do not substitute a template, and do not call another VividSites URL.

## Refused

Unknown slugs, template ids, paths, and URLs are refused. A missing or non-boolean `free` flag is refused. This plugin has no API key and does not open the paid connector.

Component code from this registry is published by VividSites as free. Do not present it as a paid template.

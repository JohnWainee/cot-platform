# `wks_<area>_<verb>` — contract (TEMPLATE)

- **Server:** <memory|teams|clickup|…>
- **Kind:** read | write | write-block
- **Gate:** none | human
- **Egress:** none | <endpoint> (architect-approved if not none)

## Purpose

One sentence: what it does and when a Chief uses it.

## Inputs

| Field | Type | Required | Notes |
|---|---|---|---|
| `example` | string | yes | … |

## Outputs

| Field | Type | Notes |
|---|---|---|
| `result` | object | … |

## Side effects

What changes in the world. For `write-block`, what it waits on.

## Errors

Named failure modes and what the Chief should do on each.

## Example

```json
{ "tool": "wks_area_verb", "args": { "example": "value" } }
```

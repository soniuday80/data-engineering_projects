{% macro cleanse_html_tags(field_with_html_tags) %}

{% set html_tags = [
    -- Common HTML tags
    '<[^>]*>',                     -- Matches any HTML tag
    -- HTML entities
    '&nbsp;',                      -- Non-breaking space
    '&amp;',                       -- Ampersand
    '&lt;',                        -- Less than
    '&gt;',                        -- Greater than
    '&quot;',                      -- Quotation mark
    '&#39;',                       -- Apostrophe
    -- Common special characters
    ' ',                     -- Non-breaking space (Unicode)
    '&[a-zA-Z]+;',                 -- Any other HTML entity
    -- Whitespace cleanup (optional)
    '\\s+',                        -- Multiple spaces
    '^\\s+|\\s+$'                  -- Leading/trailing spaces
] %}

-- Replace HTML tags and entities with spaces, then trim and collapse whitespace
trim(regexp_replace(
    regexp_replace(
        regexp_replace({{ field_with_html_tags }}, '{{ html_tags|join('|') }}', ' ', 'g'),
        '\\s+', ' ', 'g'
    ),
    '^\\s+|\\s+$', '', 'g'
))

{% endmacro %}
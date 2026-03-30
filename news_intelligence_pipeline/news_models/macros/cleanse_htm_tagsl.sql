{% macro cleanse_html_tags(field_with_html_tags) %}

{% set html_tags = [
    '<[^>]*>',
    '&nbsp;',
    '&amp;',
    '&lt;',
    '&gt;',
    '&quot;',
    '&#39;',
    ' ',
    '&[a-zA-Z]+;',
    '\\s+',
    '^\\s+|\\s+$'
] %}

trim(regexp_replace(
    regexp_replace(
        regexp_replace({{ field_with_html_tags }}, '{{ html_tags|join('|') }}', ' '),
        '\\s+', ' '
    ),
    '^\\s+|\\s+$', ''
))

{% endmacro %}
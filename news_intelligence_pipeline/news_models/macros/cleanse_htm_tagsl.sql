{% macro cleanse_html_tags(field) %}

trim(
    regexp_replace(
        regexp_replace(
            regexp_replace(
                regexp_replace(
                    regexp_replace({{ field }}, '<[^>]*>', ' '),
                '&nbsp;|&amp;|&lt;|&gt;|&quot;|&#39;', ' '),
            '&[a-zA-Z0-9]+;', ' '),
        '[^a-zA-Z0-9\\s.,!?\'\"\\-]', ' '),
    '\\s+', ' ')
)

{% endmacro %}
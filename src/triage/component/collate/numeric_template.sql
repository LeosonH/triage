{% for group in groups %}
create table as {{ prefix }}_{{ group }} as ( 
    {% for as_of_date in as_of_dates %}
    select {{ group }}, '{{ as_of_date }}'::date as date
        {% for numeric_column in numeric_columns %}
        {% for interval in intervals %}
        {% for function in functions %}
        ,{{ function }} ({{ numeric_column }}) FILTER (WHERE date >= '{{ as_of_date }}'::date - interval '{{ interval }}') AS 
        "{{ prefix }}_{{ group }}_{{ interval }}_{{ function }}_{{ numeric_column }}"    
        {% endfor %}
        {% endfor %}
        {% endfor %}
        FROM {{ table_name }}
        WHERE date < '{{ as_of_date }}' AND date >= {{ as_of_date }}::date - greatest(
            {% for interval in intervals %}
            interval '{{ interval }}',
            {% endfor %}
        )
        GROUP BY {{ group }}, {{ as_of_date }}
     union 
     {% endfor %}    
     );
{% endfor %}
      

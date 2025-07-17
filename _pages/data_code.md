---
layout: single
title: "Data & Code"
permalink: /data_code/
---

Welcome to my repository of datasets and code resources. This section will showcase datasets I have built, tools I have developed, and the research code used in my work.

{% assign entries = site.data.data_code.items %}

{% if entries.size > 0 %}
  {% for item in entries %}
  ### {{ item.title }}
  **{{ item.type }}**{% if item.date %} — _{{ item.date }}_{% endif %}  
  _{{ item.description }}_

  {% if item.link %}
  [🔗 View Project]({{ item.link }})
  {% endif %}

  {% if item.repo %}
  [💻 GitHub Repo]({{ item.repo }})
  {% endif %}

  ---
  {% endfor %}
{% else %}
<p><em>No projects available yet. Check back soon!</em></p>
{% endif %}


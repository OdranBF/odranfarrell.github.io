---
layout: single
title: "Research"
permalink: /research/
---

{% assign wip = site.data.research.work_in_progress %}
{% assign wp = site.data.research.working_papers %}
{% assign pubs = site.data.research.publications %}

{% if wip and wip.size > 0 %}
## Work in Progress

{% for paper in wip %}
<p><strong style="font-size: 1.1em;">{{ paper.title }}</strong></p>
<p><strong>{{ paper.authors }}</strong></p>
_{{ paper.description }}_  
{% if paper.note %}_Status_: *{{ paper.note }}*{% endif %}

{% if paper.link %}
[📄 {{ paper.link_text | default: "Download PDF" }}]({{ paper.link }})
{% endif %}

---
{% endfor %}
{% endif %}

{% if wp and wp.size > 0 %}
## Working Papers

{% for paper in wp %}
<p><strong style="font-size: 1.1em;">{{ paper.title }}</strong></p>
<p><strong>{{ paper.authors }}</strong></p>
_{{ paper.description }}_  
{% if paper.note %}_Status_: *{{ paper.note }}*{% endif %}

{% if paper.link %}
[📄 {{ paper.link_text | default: "Download PDF" }}]({{ paper.link }})
{% endif %}

---
{% endfor %}
{% endif %}

{% if pubs and pubs.size > 0 %}
## Publications

{% for paper in pubs %}
<p><strong style="font-size: 1.1em;">{{ paper.title }}</strong></p>
<p><strong>{{ paper.authors }}</strong></p>
_{{ paper.description }}_  
{% if paper.note %}_Published in_: *{{ paper.note }}*{% endif %}

{% if paper.link %}
[🔗 {{ paper.link_text | default: "View Publication" }}]({{ paper.link }})
{% endif %}

---
{% endfor %}
{% endif %}

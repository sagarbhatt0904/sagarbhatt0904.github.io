---
layout: archive
title: "Presentations and Posters"
permalink: /talks/
author_profile: true
---

{% if site.talkmap_link == true %}

<p style="text-decoration:underline;"><a href="/talkmap.html">See a map of all the places I've given a talk!</a></p>

{% endif %}

{% for post in site.talks reversed %}
  {% include archive-single-talk.html %}
{% endfor %}

<p class="page__meta"><i class="fa fa-clock-o" aria-hidden="true"></i> </p>
---
layout: default
title: Tags
content-type: eg
---

<style>
.category-content a {
    text-decoration: none;
    color: #4183c4;
}

.category-content a:hover {
    text-decoration: underline;
    color: #4183c4;
}
</style>

<div>
    {%- assign date_format = site.minima.date_format | default: "%b %-d, %Y" -%}
    {% for tag in site.tags %}
    <div>
        <h3 id="{{ tag | first }}">{{ tag | first }}</h3>
        <ul>
        {% for post in tag.last %}
            <li><a href="{{post.url}}">{{ post.title }}</a> | {{ post.date | date: date_format }}</li>
        {% endfor %}
        </ul>
    </div>
    {% endfor %}
    <br/>
    <br/>
</div>
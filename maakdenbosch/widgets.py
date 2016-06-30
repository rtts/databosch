from django.forms.widgets import CheckboxSelectMultiple, CheckboxFieldRenderer
from django.utils.html import conditional_escape, format_html, html_safe
from django.utils.encoding import force_str, force_text
from django.utils.safestring import mark_safe
from .models import TagGroep, Tag

class ColumnRenderer(CheckboxFieldRenderer):
    def render(self):
        """
        Outputs a <ul> for this set of choice fields, wrapped in nested <ul>'s for each tag groep.
        """
        id_ = self.attrs.get('id')
        output = []
        #tags = self.choices
        tags = list(Tag.objects.order_by('groep__naam', 'naam').select_related('groep'))

        if tags:
            output.append('<li><h2>{}</h2><ul>'.format(tags[0].groep))
            previous_group = tags[0].groep

        for i, tag in enumerate(tags):
            current_group = tag.groep
            if current_group != previous_group:
                output.append('</ul></li><li><h2>{}</h2><ul>'.format(tag.groep))
            previous_group = current_group

            w = self.choice_input_class(self.name, self.value, self.attrs.copy(), (tag.pk, tag.naam), i)
            output.append(format_html(self.inner_html, choice_value=force_text(w), sub_widgets=''))

        if tags:
            output.append('</li></ul>')

        return format_html(self.outer_html,
                           id_attr=format_html(' id="{}"', id_) if id_ else '',
                           content=mark_safe('\n'.join(output)))

class TagWidget(CheckboxSelectMultiple):
    renderer = ColumnRenderer


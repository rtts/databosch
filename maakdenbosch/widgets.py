from django.forms.widgets import CheckboxSelectMultiple
from django.utils.safestring import mark_safe
from .models import Tag

class TagWidget(CheckboxSelectMultiple):
    def optgroups(self, name, value, attrs=None):
        '''The original optgroups() function simply returns a flat list of
        options. This one, however, returns a nested list based on tag
        groups. This is enough to make Django render nested lists (an
        undocumented feature of template based form field rendering)

        '''

        tags = list(Tag.objects.order_by('groep__naam', 'naam').select_related('groep'))
        self.choices = []
        for group in sorted(set([t.groep.naam for t in tags])):
            self.choices.append((mark_safe('<h2>{}</h2>'.format(group)), [(tag.pk, tag.naam) for tag in tags if tag.groep.naam == group]))
        return super().optgroups(name, value, attrs)

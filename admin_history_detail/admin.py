# -*- coding: utf-8 -*-

from django.contrib import admin
from django.contrib.admin.options import get_content_type_for_model
from django.utils.translation import (
    override as translation_override
)
from django.utils.encoding import force_text
from django.forms.models import model_to_dict
from django.utils.translation import ugettext_lazy as _


class DetailHistoryModelAdmin(admin.ModelAdmin):
    def construct_change_message(self, request, form, formsets, add=False):
        """
            Construct a JSON structure describing changes from a changed object.
            Translations are deactivated so that strings are stored untranslated.
            Translation happens later on LogEntry access.
            """
        change_message = []
        if add:
            change_message.append({'added': form.cleaned_data})
        elif form.changed_data:
            changed_data_detail = []
            for each_changed_data in form.changed_data:
                before_change_data = form.initial.get(each_changed_data)
                after_changed_data = form.cleaned_data.get(each_changed_data)
                changed_detail = _('{0}: {1} to {0}: {2}').format(each_changed_data,
                                                                  before_change_data,
                                                                  after_changed_data)
                changed_data_detail.append(changed_detail)
            change_message.append({'changed': {'fields': changed_data_detail}})

        if formsets:
            with translation_override(None):
                for formset in formsets:
                    for added_object in formset.new_objects:
                        change_message.append({
                            'added': {
                                'name': force_text(added_object._meta.verbose_name),
                                'object': force_text(added_object),
                                'fields': model_to_dict(added_object)
                            }
                        })
                    for index, (changed_object, changed_fields) in enumerate(formset.changed_objects):
                        changed_fields_detail = []
                        for each_changed_field in changed_fields:
                            before_change_data = formset.initial_forms[index].initial.get(each_changed_field)
                            after_changed_data = formset.initial_forms[index].cleaned_data.get(each_changed_field)
                            changed_detail = _('{0}: {1} to {0}: {2}').format(each_changed_field,
                                                                              before_change_data,
                                                                              after_changed_data)
                            changed_fields_detail.append(changed_detail)
                        change_message.append({
                            'changed': {
                                'name': force_text(changed_object._meta.verbose_name),
                                'object': force_text(changed_object),
                                'fields': changed_fields_detail,
                            }
                        })
                    for deleted_object in formset.deleted_objects:
                        change_message.append({
                            'deleted': {
                                'name': force_text(deleted_object._meta.verbose_name),
                                'object': force_text(deleted_object),
                                'fields': model_to_dict(deleted_object)
                            }
                        })
        return change_message

    def log_deletion(self, request, object, object_repr):
        """
        Log that an object will be deleted. Note that this method must be
        called before the deletion.

        The default implementation creates an admin LogEntry object.
        """
        from django.contrib.admin.models import LogEntry, DELETION
        LogEntry.objects.log_action(
            user_id=request.user.pk,
            content_type_id=get_content_type_for_model(object).pk,
            object_id=object.pk,
            object_repr=object_repr,
            action_flag=DELETION,
            change_message=model_to_dict(object)
        )

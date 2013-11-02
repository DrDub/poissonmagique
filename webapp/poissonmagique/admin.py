from webapp.poissonmagique.models import UserState, Human, Campaign, Character, Fragment, Message, MessageID, Queue
from django.contrib import admin

from bitfield import BitField
from bitfield.forms import BitFieldCheckboxSelectMultiple
from bitfield.admin import BitFieldListFilter

class MessageAdmin(admin.ModelAdmin):
    formfield_overrides = { BitField: {'widget': BitFieldCheckboxSelectMultiple}, }
    fields = ('author_character', 'author_human', 'campaign', 'text', 'when', 'game_time', 'message_id', 'receivers_character','receivers_human', 'parts' )
    #list_filter = ( ('status', BitFieldListFilter,)  )

admin.site.register(UserState)
admin.site.register(Human)
admin.site.register(Campaign)
admin.site.register(Character)
admin.site.register(Fragment)
admin.site.register(Message, MessageAdmin)
admin.site.register(MessageID)
admin.site.register(Queue)



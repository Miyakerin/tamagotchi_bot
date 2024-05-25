from django.contrib import admin

from .models import *

admin.site.register(TgUser)
admin.site.register(Rarity)
admin.site.register(Element)
admin.site.register(Item)
admin.site.register(Tamagotchi)
admin.site.register(ItemInInventory)
admin.site.register(TamagotchiInPossession)
admin.site.register(Action)
admin.site.register(Task)
admin.site.register(ItemsForAction)
admin.site.register(RewardForTask)





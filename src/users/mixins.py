class DisplayRoleMixin:
    def display_role(self, obj):
        return obj.get_role_display()

    display_role.short_description = 'Роль'

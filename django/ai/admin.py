from django.contrib import admin

class StyledModelAdmin(admin.ModelAdmin):
    """A common base admin class with shared media information."""
    class Media:
        css = { "all": ('admin.css', )}

from django.contrib import admin
from .models import Terms, Candidates

class TermsInline(admin.StackedInline):
    """Make Terms inline in Candidates admin"""
    model = Terms
    exclude = ('uid',)
    extra = 1

@admin.register(Candidates)
class CandidatesAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    inlines = (TermsInline,)
    exclude = ('uid',)

# Register your models here.
@admin.register(Terms)
class TermsAdmin(admin.ModelAdmin):
    list_display = ('candidate', 'gender', 'party', 'election_year')
    search_fields = ('name',)
    list_filter = ('election_year', 'party')
    exclude = ('uid',)
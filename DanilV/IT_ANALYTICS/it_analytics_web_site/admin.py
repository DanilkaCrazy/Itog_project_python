from .models import Image, AllVacanciesSalaryYear, Vacancies1CSalaryYear, AmountVacanciesAll, AmountVacancies1С, About, CityTableSalaryYear, SkillsTableYear

from django.contrib import admin


class AllVacanciesSalaryYearAdmin(admin.ModelAdmin):
	list_display = ("title", "curren", "year", "value")


class Vacancies1CSalaryYearAdmin(admin.ModelAdmin):
	list_display = ("title", "curren", "year", "value")


class AmountVacanciesAllAdmin(admin.ModelAdmin):
	list_display = ("year", "value")


class AmountVacancies1СAdmin(admin.ModelAdmin):
	list_display = ("year", "value")


class CityTableSalaryYearAdmin(admin.ModelAdmin):
	list_display = ("city", "curren", "year", "salary")


class SkillsTableYearAdmin(admin.ModelAdmin):
	list_display = ("skill", "year", "counter")

admin.site.register(Image)
admin.site.register(About)
admin.site.register(AllVacanciesSalaryYear, AllVacanciesSalaryYearAdmin)
admin.site.register(Vacancies1CSalaryYear, Vacancies1CSalaryYearAdmin)
admin.site.register(AmountVacanciesAll, AmountVacanciesAllAdmin)
admin.site.register(AmountVacancies1С, AmountVacancies1СAdmin)
admin.site.register(CityTableSalaryYear, CityTableSalaryYearAdmin)
admin.site.register(SkillsTableYear, SkillsTableYearAdmin)

from django.db import models

# Create your models here.


class Image(models.Model):
	name = models.CharField("Название", max_length=128)
	image = models.ImageField(upload_to="images/charts")

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = "Изображение"
		verbose_name_plural = "Все изображения"


class About(models.Model):
	title =  models.CharField("Название", max_length=128)
	text = models.TextField("Информация")
	image = models.ImageField(upload_to="images/charts")

	def __str__(self):
		return self.title

	class Meta:
		verbose_name = "Контент"
		verbose_name_plural = "О профессии"


class AllVacanciesSalaryYear(models.Model):
	title = models.CharField("Название", max_length=128)
	curren = models.CharField("Валюта", max_length=128)
	year = models.PositiveIntegerField("Год")
	value = models.PositiveIntegerField("Средняя зарплата")

	def __str__(self):
		return self.title

	class Meta:
		verbose_name = "Строку"
		verbose_name_plural = "Динамика зарплат по годам для всех профессий"


class Vacancies1CSalaryYear(models.Model):
	title = models.CharField("Название", max_length=128)
	curren = models.CharField("Валюта", max_length=128)
	year = models.PositiveIntegerField("Год")
	value = models.PositiveIntegerField("Средняя зарплата")

	def __str__(self):
		return self.title

	class Meta:
		verbose_name = "Строку"
		verbose_name_plural = "Динамика зарплат по годам для 1C-разработчика"


class AmountVacanciesAll(models.Model):
	title = models.CharField("Название", max_length=128)
	year = models.PositiveIntegerField("Год")
	value = models.PositiveIntegerField("Средняя зарплата")

	def __str__(self):
		return self.title

	class Meta:
		verbose_name = "Строку"
		verbose_name_plural = "Динамика количества вакансий по годам для всех профессий"


class AmountVacancies1С(models.Model):
	title = models.CharField("Название", max_length=128)
	year = models.PositiveIntegerField("Год")
	value = models.PositiveIntegerField("Число вакансий")

	def __str__(self):
		return self.title


	class Meta:
		verbose_name = "Строку"
		verbose_name_plural = "Динамика количества вакансий по годам для 1С-разработчика"


class CityTableSalaryYear(models.Model):
	city = models.CharField("Название", max_length=128)
	curren = models.CharField("Валюта", max_length=8)
	year = models.PositiveIntegerField("Год")
	salary = models.PositiveIntegerField("Зарплата")

	def __str__(self):
		return self.city 

	class Meta:
		verbose_name = "Строку"
		verbose_name_plural = "Таблицы зарплаты в городах по годам"


class SkillsTableYear(models.Model):
	skill = models.CharField("Название", max_length=128)
	year = models.PositiveIntegerField("Год")
	counter = models.PositiveIntegerField("Кол-во вакансий с этим навыком")

	def __str__(self):
		return self.skill

	class Meta:
		verbose_name = "Строку"
		verbose_name_plural = "Топ 10-навыков по годам"

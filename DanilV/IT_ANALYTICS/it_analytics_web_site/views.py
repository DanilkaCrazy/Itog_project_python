from datetime import date
import json

import requests
from django.shortcuts import render

from .models import Image, AllVacanciesSalaryYear, Vacancies1CSalaryYear, AmountVacanciesAll, AmountVacancies1С, About, CityTableSalaryYear, SkillsTableYear


# о профессии
def index(request):
	article = About.objects.all()
	return render(request, "index.html", {
			"head": "О профессии",
			"dashboard": "О профессии", 
			"article": article,
		})


# востребованность
def demand(request):
	charts_all = Image.objects.all()	
	salary_all = AllVacanciesSalaryYear.objects.all()
	amount_all = AmountVacanciesAll.objects.all()
	salary_1c = Vacancies1CSalaryYear.objects.all()
	amount_1c = AmountVacancies1С.objects.all()

	return render(request, "demand.html", {
			"head": "Востребованность",
			"dashboard_chart": "Графики",
			"dashboard_table": "Таблицы",
			"charts_all": charts_all,
			"salary_all": salary_all,
			"salary_1c": salary_1c,
			"amount_all": amount_all,
			"amount_1c": amount_1c,
		})


#география
def cities(request):
	charts = [(" Валюта - ".join(chart.name.split('_')), chart.image.url) for chart in Image.objects.all() if chart.name.split("_")[0] not in ("1c", "all", "skill")]
	tables = dict()
	for elem in CityTableSalaryYear.objects.all():
		tables.setdefault(elem.city, dict()).setdefault(elem.year, {
				"curren": elem.curren,
				"salary": elem.salary,
			})

	return render(request, "cities.html", {
			"head": "География",
			"dashboard_chart": "Графики зарплат 1С-разработчика в разных городах",
			"dashboard_table": "Таблицы зарплат 1С-разработчика в разных городах",
			"charts": charts,
			"tables": tables.items(),
		})


#навыки
def top_10_skills(request):	
	charts = dict()
	for chart in Image.objects.all():
		if chart.name.split("_")[0] == "skill":
			year = chart.name.split("_")[1]
			charts[year] = chart.image

	tables = dict()
	for item in SkillsTableYear.objects.all():
		tables.setdefault(item.year, dict()).update({item.skill: item.counter})

	return render(request, "top_10_skills.html", {
			"head": "Навыки",
			"dashboard_chart": "Графики самых популярных навыков",
			"dashboard_table": "Таблица самых популярных навыков",
			"charts": charts,
			"tables": tables,
		})


#hh api
def api_headhunter_vacancies(request):
	URL = "http://api.hh.ru/vacancies?clusters=true&only_with_salary=true&enable_snipprts=true&st=searchVacancy" \
				"&text=1С-разработчик+OR+1с разработчик+OR+1c разработчик+OR+1с+OR+1c+OR+1 c+OR+1 с&search_field=name&per_page=100&area=1"

	def del_html(string: str) -> str:
		"""удаляет html теги из текста"""
		clear_word = str()
		for w in string.split():
			for tag in ("<highlighttext>", "</highlighttext>"):
				if tag in w:
					w = "\n".join(w.split(tag))
				else:
					w = "\n" + w
			clear_word += w
		return clear_word
	
	salary, vacancies = int(), list()
	response = requests.get(URL, timeout=5).json()
	for item in response["items"]:
		now_date = date.today()
		published_at = date.fromisoformat(item["published_at"].split("T")[0])
		if (published_at.weekday() not in (6, 7)) and (now_date.toordinal() > published_at.toordinal()):
			if item["snippet"]["responsibility"] and item["snippet"]["requirement"] and item["employer"]["name"] \
				and (item["salary"]["from"] not in [0 , None] or item["salary"]["to"] not in [0, None]) \
					and item["salary"]["currency"] and item["area"]["name"]:

				if item["salary"]["from"] and item["salary"]["to"]:
					salary = round((item["salary"]["to"] + item["salary"]["to"]) / 2)
				elif item["salary"]["to"] and not item["salary"]["to"]:
					salary = item["salary"]["to"]
				elif not item["salary"]["to"] and item["salary"]["to"]:
					salary = item["salary"]["to"]
				
				if salary:
					vacancies.append({
						"title": item["name"],
						"description": del_html(string=item["snippet"]["responsibility"]),
						"skills": del_html(string=item["snippet"]["requirement"]),
						"company": item["employer"]["name"],
						"salary": salary,
						"currency": item["salary"]["currency"],
						"city": item["area"]["name"],
						"published_at": item["published_at"].split("T")[0], 
					})

	return render(request, "api_headhunter_vacancies.html", {
			"head": "API HEADHUNTER",
			"vacancies": vacancies,
		})
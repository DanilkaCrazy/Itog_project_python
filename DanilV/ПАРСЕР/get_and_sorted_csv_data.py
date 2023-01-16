from datetime import date
from collections import Counter
import json
import csv
import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def get_all_vacancies_in_csv(filename: str) -> list:
	"""получает все вакансии из файла vacancies_with_skills.csv"""
	"""возвращает список словарей"""
	with open(filename, encoding="utf-8") as file:
		data = list(csv.DictReader(file))
	return data


def get_json_data(filename: str) -> dict:
	"""получает словарь json из файла currency_year_salary_result_count.json"""
	with open(filename, encoding="utf-8") as file:
		data = json.load(file)
	return data


def preparation_salary_on_year_json(data: list, save_json_to: str, key_filter: str, with_city: bool=False) -> None:
	"""отбирает валюту, год, зарплату и записывает его в json"""
	"""это нужно так как файл vacancies_with_skills.csv обрабатывается очень долго"""
	
	if key_filter == "ALL":
		vacancies = data
	elif key_filter == "1C":
		vacancies = list()
		for item in data:
			for word in ("1С-разработчик", "1с разработчик", "1c разработчик", "1с", "1c", "1 c", "1 с"):
				if word in item["name"]:
					vacancies.append(item)

	currency_salary_year = dict()
	if not with_city:
		for vacancy in vacancies:
			if (vacancy["salary_from"] or vacancy["salary_to"]) and vacancy["salary_currency"] and vacancy["published_at"]:
				salaries = [float(item) for item in [vacancy.get("salary_from", 0), vacancy.get("salary_to", 0)] if item]
				if len(salaries) == 2:
					salary = round(sum(salaries) / 2)
				else:
					salary = round(salaries[0])

				pub, curren = date.fromisoformat(vacancy["published_at"].split("T")[0]).year, vacancy["salary_currency"]
				if currency_salary_year.get(curren, None) is None or currency_salary_year[curren].get(pub, None) is None:
					currency_salary_year.setdefault(curren, dict()).setdefault(pub, {"salary": salary, "quan": 1})
				else:
					currency_salary_year[curren][pub]["salary"] += salary
					currency_salary_year[curren][pub]["quan"] += 1
	else:
		for vacancy in vacancies:
			if (vacancy["salary_from"] or vacancy["salary_to"]) and vacancy["salary_currency"] and vacancy["published_at"] and vacancy["area_name"]:
				salaries = [float(item) for item in [vacancy.get("salary_from", 0), vacancy.get("salary_to", 0)] if item]
				if len(salaries) == 2:
					salary = round(sum(salaries) / 2)
				else:
					salary = round(salaries[0])

				city = vacancy["area_name"]
				pub, curren = date.fromisoformat(vacancy["published_at"].split("T")[0]).year, vacancy["salary_currency"]
				if currency_salary_year.get(city, None) is None or currency_salary_year[city].get(curren, None) is None or currency_salary_year[city][curren].get(pub, None) is None:
					currency_salary_year.setdefault(city, dict()).setdefault(curren, dict()).setdefault(pub, {"middle_salary": salary, "quan": 1})
				else:
					middle_salary_old = currency_salary_year[city][curren][pub]["middle_salary"]
					amount_vacancies = currency_salary_year[city][curren][pub]["quan"]
					salary = round( (( middle_salary_old * amount_vacancies ) + salary) / (amount_vacancies + 1) )

					currency_salary_year[city][curren][pub]["middle_salary"] = salary
					currency_salary_year[city][curren][pub]["quan"] += 1

	
	with open(save_json_to, 'w', encoding="utf-8") as file:
		json.dump(currency_salary_year, fp=file, indent=2, ensure_ascii=False)


def build_chart_salary_on_year(data: dict, coords_save_to: str, name_chart: str) -> None:
	# строит графики динамики уровня зарплат по годам в разных валютах

	data_for_charts = dict()
	for curren, salary_on_year in data.items():
		for year, data_salary in salary_on_year.items():
			if Counter( [curren, year] ) != Counter( ["USD", "2005"] ): #баганый год в нём слишком огромная цифра скипаем его нахуй
				data_for_charts.setdefault(curren, list()).append( ( year, round(data_salary["salary"] / data_salary["quan"]) ) )

	for curren, data_salary in data_for_charts.items():
		plt.title(f"{name_chart}{curren}")
		plt.xlabel("Год вакансий")
		plt.ylabel("Средняя зарплата")
		plt.bar([elem[0] for elem in data_salary], [elem[1] for elem in data_salary], color="lightcoral")
		plt.show()

	#сохраним корды в json для создания таблиц
	with open(coords_save_to, 'w', encoding="utf-8") as file:
		json.dump(data_for_charts, fp=file, indent=2, ensure_ascii=False)


def build_chart_quan_vacancies_in_year(data: dict, coords_save_to: str, name_chart: str) -> None:
	# строим графики динамики количетсва вакансий по годам

	data_for_charts = dict()
	for curren, salary_on_year in data.items():
		for year, data_salary in salary_on_year.items():
			if data_for_charts.get(year, None) is None:
				data_for_charts[year] = data_salary["quan"]
			else:
				data_for_charts[year] += data_salary["quan"]

	plt.title(name_chart)
	plt.xlabel("Год вакансий")
	plt.ylabel("Количество вакансий")
	plt.bar(data_for_charts.keys(), data_for_charts.values(), color="lightcoral")
	plt.show()

	with open(coords_save_to, 'w', encoding="utf-8") as file:
		json.dump(data_for_charts, fp=file, indent=2, ensure_ascii=False)


def cities_build_chart_salary_year(data: dict, coords_save_to: str) -> None:

	data_for_tables = dict()
	for city, elem in data.items():
		#определяем в какой валюте дано больше всего вакансий и по ней будем строить график
		all_currencies = list(elem.keys())
		max_qnt_curren = max([ ( len(elem[curren]), curren ) for curren in all_currencies], key=lambda pack: pack[0])
		if max_qnt_curren[0] >= 6: #если в городе статистика меньше чем за 6 лет, то скип
			json_info = elem[max_qnt_curren[1]]
			salary_info = elem[max_qnt_curren[1]].items()
			years = [year for year, _ in salary_info]
			values = [item["middle_salary"] for _, item in salary_info]
			data_for_tables.setdefault(city, dict()).setdefault(max_qnt_curren[1], json_info)

			plt.title(f"Зарплата в городе {city}. Ключевая валюта - {max_qnt_curren[1]}")
			plt.xlabel("Год")
			plt.ylabel("Зарплата")
			plt.bar(years, values, color="lightcoral")

			# plt.savefig(f"{city}_{max_qnt_curren[1]}", dpi=500)#если надо все графики в одну папку(работает криво)
			plt.show()

	with open(coords_save_to, 'w', encoding="utf-8") as file:
		json.dump(data_for_tables, fp=file, indent=2, ensure_ascii=False)


def create_chart_table_skills_backend(data: list, coords_save_to: str) -> None:
	# 10 самых популярных навыков
	
	skills_counter = dict()
	for item in list(filter(lambda pack: True if pack["key_skills"] and pack["key_skills"] and pack["published_at"] else False, data)):
		year = date.fromisoformat(item["published_at"].split("T")[0]).year
		skills_counter.setdefault(year, dict())
		for skill in item["key_skills"].split('\n'):	
			skills_counter[year][skill] = skills_counter[year].get(skill, 0) + 1

	top_10_skills = dict()
	for year, skills in skills_counter.items():
		top_10_skills.setdefault(year, dict())
		for _, skill_count in zip(range(10), sorted(skills.items(), key=lambda pack: pack[1], reverse=True)):
			skill, count = skill_count
			top_10_skills[year][skill] = count

	for year, top_10_skills_in_year in top_10_skills.items():
		index = np.arange(10)
		plt.title(f"Топ-10 самых популярных навыков за {year} год")
		plt.xlabel("Навык")
		plt.ylabel("Вакансий с навыком")
		df = pd.DataFrame(sorted(top_10_skills_in_year.items(), key=lambda pack: pack[1]))
		df.plot(kind="barh")
		plt.yticks(index, top_10_skills_in_year.keys())

		print(year)
		plt.show()

	with open(coords_save_to, 'w', encoding="utf-8") as file:
		json.dump(top_10_skills, fp=file, indent=2, ensure_ascii=False)




# ------------------------------------ДЛЯ ВСЕХ ПРОФЕССИЙ------------------------------------
#отбираем всё самое необходимое для графиков из файла vacancies_with_skills.csv для ВСЕХ профессий
# preparation_salary_on_year_json(data=get_all_vacancies_in_csv(filename="vacancies_with_skills.csv"), word_filter="ALL", save_json_to="currency_year_salary_result_count.json")

# строит графики динамики уровня зарплат по годам в разных валютах для ВСЕХ профессий
# build_chart_salary_on_year(get_json_data(filename="currency_year_salary_result_count.json"), \
# 	coords_save_to="chart_salary_on_year_coords.json", name_chart="Динамика уровня зарплат по годам для всех профессий. Валюта - ")

# строим графики динамики количетсва вакансий по годам для ВСЕХ профессий
# build_chart_quan_vacancies_in_year(get_json_data(filename="currency_year_salary_result_count.json"), \
# 	coords_save_to="chart_quan_vacancies_in_year_coords.json", name_chart="Динамика количества вакансий по годам для всех профессий")


# ------------------------------------ДЛЯ 1С РАЗРАБОТЧИКА------------------------------------
# отбираем всё самое необходимое для графиков из файла vacancies_with_skills.csv для 1С разработчика
# preparation_salary_on_year_json(data=get_all_vacancies_in_csv(filename="vacancies_with_skills.csv"), key_filter="1C", save_json_to="1c_currency_year_salary_result_count.json")

# строит графики динамики уровня зарплат по годам в разных валютах для 1С разработчика
# build_chart_salary_on_year(get_json_data(filename="1c_currency_year_salary_result_count.json"), \
# 	coords_save_to="1c_currency_year_salary_coords_result.json", name_chart="Динамика уровня зарплат по годам 1С-разработчик. Валюта - ")

# строим графики динамики количетсва вакансий по годам для 1С разработчика
# build_chart_quan_vacancies_in_year(get_json_data(filename="1c_currency_year_salary_result_count.json"), \
# 	coords_save_to="1c_quan_vacancies_in_year_coords.json", name_chart="Динамика количества вакансий по годам 1С-разработчик")

# отбираем всё самое необходимое для графиков из файла vacancies_with_skills.csv для 1С разработчика
# preparation_salary_on_year_json(data=get_all_vacancies_in_csv(filename="vacancies_with_skills.csv"), key_filter="1C", save_json_to="cities_salary_year_raw.json", with_city=True)
create_chart_table_skills_backend(data=get_all_vacancies_in_csv(filename="vacancies_with_skills.csv"), coords_save_to="skills.json")
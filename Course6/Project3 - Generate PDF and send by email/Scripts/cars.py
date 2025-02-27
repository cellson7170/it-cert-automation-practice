#!/usr/bin/env python3

import json
import locale
import sys
import reports
import emails
import os


def load_data(filename):
  """Loads the contents of filename as a JSON file."""
  with open(filename) as json_file:
    data = json.load(json_file)
  return data


def format_car(car):
  """Given a car dictionary, returns a nicely formatted name."""
  return "{} {} ({})".format(
      car["car_make"], car["car_model"], car["car_year"])


def process_data(data):
  """Analyzes the data, looking for maximums.

  Returns a list of lines that summarize the information.
  """
  max_revenue = {"revenue": 0}
  max_sales = {"sales": 0}
  pop_year = {"year": 0}
  pop_year_sales = {"sales": 0}
  car_years = {}
  for item in data:
    # Calculate the revenue generated by this model (price * total_sales)
    # We need to convert the price from "$1234.56" to 1234.56
    item_price = locale.atof(item["price"].strip("$"))
    item_revenue = item["total_sales"] * item_price
    if item_revenue > max_revenue["revenue"]:
      item["revenue"] = item_revenue
      max_revenue = item
    # TODO: also handle max sales
    item_sales = item["total_sales"]
    if item_sales > max_sales["sales"]:
      item["sales"] = item_sales
      max_sales = item
    # TODO: also handle most popular car_year
    if item["car"]["car_year"] not in car_years:
      car_years[item["car"]["car_year"]] = 1
    else:
      car_years[item["car"]["car_year"]] += 1
    
  pop_year["year"] = max(car_years, key = car_years.get)
  for item in data:
    # item_price = locale.atof(item["price"].strip("$"))
    if item["car"]["car_year"] == pop_year["year"]:
      pop_year_sales["sales"] += item["total_sales"]

  summary = [
    "The {} generated the most revenue: ${}".format(
      format_car(max_revenue["car"]), max_revenue["revenue"]),
    "The {} had the most sales: {}".format(format_car(max_sales["car"]), max_sales["sales"]),
    "The most popular year was {} with {} sales.".format(pop_year["year"], pop_year_sales["sales"])
  ]

  return summary


def cars_dict_to_table(car_data):
  """Turns the data in car_data into a list of lists."""
  table_data = [["ID", "Car", "Price", "Total Sales"]]
  for item in car_data:
    table_data.append([item["id"], format_car(item["car"]), item["price"], item["total_sales"]])
  return table_data

def create_directory(path):
  os.makedirs(os.path.dirname(path), exist_ok=True)
  return open(path, 'w')


def main(argv):
  """Process the JSON data and generate a full report out of it."""
  data = load_data("car_sales.json")
  summary = process_data(data)
  summary_pdf = "{}<br/>{}<br/>{}".format(summary[0], summary[1], summary[2])
  summary_email = "{}\n{}\n{}".format(summary[0], summary[1], summary[2])
#   print(summary_pdf)
  # TODO: turn this into a PDF report
  with create_directory("/tmp/cars.pdf"):
    reports.generate("/tmp/cars.pdf", "Car Sales Data", summary_pdf, cars_dict_to_table(data))
  
  # TODO: send the PDF report as an email attachment
  message = emails.generate("automation.example.com", "<user>.example.com", "Sales summary for last month", summary_email, "/tmp/cars.pdf")
  emails.send(message)

if __name__ == "__main__":
  main(sys.argv)

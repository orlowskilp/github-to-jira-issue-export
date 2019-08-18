#!/usr/bin/python

"""
Licensed to the Apache Software Foundation (ASF) under one
or more contributor license agreements.  See the NOTICE file
distributed with this work for additional information
regarding copyright ownership.  The ASF licenses this file
to you under the Apache License, Version 2.0 (the
"License"); you may not use this file except in compliance
with the License.  You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing,
software distributed under the License is distributed on an
"AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
KIND, either express or implied.  See the License for the
specific language governing permissions and limitations
under the License.
"""

def format_issue_description(text):
	import formatters.custom_formatter as cf

	return cf.format(text)

def parse_gh_issues(parsed_json):
	num_issues = len(parsed_json)

	output = [['Issue Type', 'Summary', 'Description', 'Status', 'Date Created', 'Date Modified', 'Labels', 'Assignee']]

	for i in range(num_issues):
		# Read fields accessible off the bat
		title = parsed_json[i]['title']
		body = format_issue_description(parsed_json[i]['body'])
		state = parsed_json[i]['state']
		created_at = parsed_json[i]['created_at'][:-1]
		closed_at = None if parsed_json[i]['closed_at'] == None else parsed_json[i]['closed_at'][:-1]

		# If an issue is not closed store the date of last update
		updated_at = closed_at if closed_at != None else parsed_json[i]['updated_at'][:-1]
		labels_json = parsed_json[i]['labels']

		# Read labels and group them in columns
		labels = []
		for j in range(len(labels_json)):
			labels.append(labels_json[j]['name'].replace(' ', '_'))

		labels_string = " ".join(labels)

		# Identify the type of issue
		issue_type = 'Epic' if 'Epic' in labels else 'Story'

		# JIRA only supports a single assignee
		assignees_json = parsed_json[i]['assignees']
		assignee = '' if len(assignees_json) == 0 else assignees_json[0]['login']

		output.append([issue_type, title, body, state, created_at.replace('T', ' '), updated_at.replace('T', ' '), labels_string, assignee])

	return output

def write_csv(file, data):
	import csv

	# Create a CSV writer and write data line by line
	csv_writer = csv.writer(file, delimiter = ',', quoting=csv.QUOTE_MINIMAL)
	for i in range(len(data)):
		csv_writer.writerow(data[i])

def handle_input():
	import sys, os

	# Check if there is at least one input parameter
	if len(sys.argv) < 2:
		print("Usage: {0} <my/input.json> | <my/inputs/>".format(sys.argv[0]))
		return None

	input_path = sys.argv[1]

	# Check if the first parameter is a valid path to a file or directory
	if not os.path.exists(input_path):
		print("File {0} doesn't exist".format(input_path))
		return None

	# Check if the path in input parameter is a file or directory and handle it approprietly
	if os.path.isdir(input_path):
		input_files = []
		for root, dirs, files in os.walk(input_path):
			for json_file in files:
				input_files.append(os.path.join(root, json_file))

		return input_files
	else:
		return [input_path]

def main():
	import json

	files = handle_input()
	if files is None:
		print("Exiting...")
		return -1

	outputs_count = 0
	for i in range(len(files)):
		parsed_json = None

		with open(files[i], "r") as file:
			try:
				parsed_json = json.loads(file.read())
			except ValueError:
				print("{0} is not a properly formatted JSON file. Skipping...".format(files[i]))
				continue

			issues = parse_gh_issues(parsed_json)

		output_file = "{0}.csv".format(files[i].split('.')[0])

		with open(output_file, "w") as file:
			write_csv(file, issues)

		print("CSV formatted output saved to {0}".format(output_file))
		outputs_count = outputs_count + 1

	print("Saved {0} files".format(str(outputs_count)))

if __name__ == "__main__":
	main()

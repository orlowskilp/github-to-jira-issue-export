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

def parse_gh_issues(file):
	import json

	parsed_json = json.loads(file.read())
	num_issues = len(parsed_json)

	output = [['Issue Type', 'Summary', 'Description', 'Status', 'Date Created', 'Date Modified', 'Labels', 'Assignee']]

	for i in range(num_issues):
		# Read fields accessible off the bat
		title = parsed_json[i]['title']
		body = parsed_json[i]['body'].replace('\n', '[new line]')
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

	csv_writer = csv.writer(file, delimiter = ',', quoting=csv.QUOTE_MINIMAL)
	for i in range(len(data)):
		csv_writer.writerow(data[i])


	#lines = []
	#for i in range(len(data)):
	#	lines.append(",".join(data[i]))

	#file.writelines(lines)

def main():
	import sys

	if len(sys.argv) < 2:
		print("No input file provided")
		return -1

	file_path = sys.argv[1]

	with open(file_path, "r") as file:
		issues = parse_gh_issues(file)

	with open("output.csv", "w") as file:
		write_csv(file, issues)

	#for i in range(len(issues)):
	#	print(issues[i])

if __name__ == "__main__":
	main()

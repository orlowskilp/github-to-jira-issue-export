#!/bin/bash

# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

TOKEN_FILE=./.token

if [[ ! -f $TOKEN_FILE ]]; then
	echo "Error: Token file not found under $TOKEN_FILE"
	exit -1
fi

TOKEN=$(cat $TOKEN_FILE | base64 --decode)

if [[ $# -lt 1 ]]; then
	echo "Synopsis: $0 <json_file>"
	exit -2
fi

REPO=$1

curl -i "https://api.github.com/repos/onosolutions/${REPO}/issues?state=all" -u "orlowskilp:${TOKEN}" > input.json
LINE_COUNT=$(cat input.json | wc -l)
TAIL_LINE_COUNT=$((${LINE_COUNT} - 27))
tail -$TAIL_LINE_COUNT input.json > ${REPO}.json
rm input.json

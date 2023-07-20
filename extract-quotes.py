#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2023 Michiel Hendriks
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import sys, pathlib, re, textwrap, sqlite3

class TextViewerFile:
	def __init__(self, source):
		self.source = source

	def __enter__(self):
		self._fp = open(self.source, "rt", encoding="cp1252", errors="ignore")
		self._more = True
		self.line = ""
		self.id = None
		return self

	def __exit__(self, *args):
		self._fp.close()

	def has_next(self):
		return self._more

	def next(self):
		if not self._more:
			return False
		if (ln := self._fp.readline()):
			self.line = ln
			self.id = re.match("^(\d+):\n$", ln)
		else:
			self._more = False
		return self._more

	def is_id(self):
		return self.id

	def next_id(self):
		while self.has_next():
			self.next()
			if self.is_id():
				return

def add_quote(source, id, text):
	if not text.strip():
		return

	src = re.match("((lba[12])/)?(\d\d)\s?([^/.]+)\.txt$", str(source));
	game = ""
	area = ""
	if src:
		game = src.group(2)
		area = src.group(4)

	db.execute(
		"""
		insert into quotes (id, source, game, area, message) values (?, ?, ?, ?, ?)
		on conflict(id) do nothing
		""",
		(str(source)+"#"+id, str(source), game, area, text)
	)

def proc_entry(fp):
	id = fp.id.group(1);
	fp.next()
	text = ""
	while not fp.is_id():
		text += "\n"+fp.line.strip()
		fp.next()
		if not fp.has_next():
			break
	add_quote(fp.source, id, text.strip());

def proc_file(filename):
	source = pathlib.Path(filename)
	if not source.exists():
		print("File does not exists:", filename)
		return
	print("Processing file:", source)
	with TextViewerFile(source) as fp:
		while fp.has_next():
			if fp.is_id():
				proc_entry(fp)
			else:
				fp.next_id()

def init_db():
	db.execute('''
		create table if not exists quotes (
			id text primary key,
			source text,
			game text,
			area text,
			location text,
			speaker text,
			message text,
			enabled boolean not null default true,
			last_used timestamp
		)
	''')

db_conn = sqlite3.connect('quotes.db')
db = db_conn.cursor()
init_db()

try:
	sys.argv.pop(0)
	for file in sys.argv:
		proc_file(file)
		db_conn.commit()
finally:
	db.close()
	db_conn.close()

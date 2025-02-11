# -*- coding: utf-8 -*-
"""
	urlresolver XBMC Addon
	Copyright (C) 2013 Bstrdsmkr
	This program is free software: you can redistribute it and/or modify
	it under the terms of the GNU General Public License as published by
	the Free Software Foundation, either version 3 of the License, or
	(at your option) any later version.
	This program is distributed in the hope that it will be useful,
	but WITHOUT ANY WARRANTY; without even the implied warranty of
	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
	GNU General Public License for more details.
	You should have received a copy of the GNU General Public License
	along with this program.  If not, see <http://www.gnu.org/licenses/>.
	Adapted for use in xbmc from:
	https://github.com/einars/js-beautify/blob/master/python/jsbeautifier/unpackers/packer.py
	
	usage:
	if detect(some_string):
		unpacked = unpack(some_string)
Unpacker for Dean Edward's p.a.c.k.e.r
"""
from re import (
	search, DOTALL,
	sub, findall
)

def detect(source):
	"""Detects whether `source` is P.A.C.K.E.R. coded."""
	source = source.replace(' ', '')

	if search('eval\(function\(p,a,c,k,e,(?:r|d)', source):
		return True
	else:
		return False

def unpack(source):
	"""Unpacks P.A.C.K.E.R. packed js code."""
	payload, symtab, radix, count = _filterargs(source)

	if count != len(symtab):
		raise UnpackingError('Malformed p.a.c.k.e.r. symtab.')

	try:
		unbase = Unbaser(radix)
	except TypeError:
		raise UnpackingError('Unknown p.a.c.k.e.r. encoding.')

	def lookup(match):
		"""Look up symbols in the synthetic symtab."""
		word = match.group(0)
		return symtab[unbase(word)] or word

	source = sub(r'\b\w+\b', lookup, payload)
	return _replacestrings(source)

def _filterargs(source):
	"""Juice from a source file the four args needed by decoder."""
	juicers = [
		(r"}\('(.*)', *(\d+), *(\d+), *'(.*)'\.split\('\|'\), *(\d+), *(.*)\)\)"),
		(r"}\('(.*)', *(\d+), *(\d+), *'(.*)'\.split\('\|'\)"),
	]

	for juicer in juicers:
		args = search(juicer, source, DOTALL)

		if args:
			a = args.groups()

			try:
				return a[0], a[3].split('|'), int(a[1]), int(a[2])
			except ValueError:
				raise UnpackingError('Corrupted p.a.c.k.e.r. data.')
	# could not find a satisfying regex
	raise UnpackingError('Could not make sense of p.a.c.k.e.r data (unexpected code structure)')

def _replacestrings(source):
	"""Strip string lookup table (list) and replace values in source."""
	match = search(r'var *(_\w+)\=\["(.*?)"\];', source, DOTALL)

	if match:
		varname, strings = match.groups()
		startpoint = len(match.group(0))
		lookup = strings.split('","')
		variable = '%s[%%d]' % varname

		for index, value in enumerate(lookup):
			source = source.replace(variable % index, '"%s"' % value)

		return source[startpoint:]

	return source

class Unbaser(object):
	"""Functor for a given base. Will efficiently convert
	strings to natural numbers."""
	ALPHABET = {
		62: '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ',
		95: (' !"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ'
			 '[\]^_`abcdefghijklmnopqrstuvwxyz{|}~')
	}

	def __init__(self, base):
		self.base = base
		# If base can be handled by int() builtin, let it do it for us
		if 2 <= base <= 36:
			self.unbase = lambda string: int(string, base)
		else:
			if base < 62:
				self.ALPHABET[base] = self.ALPHABET[62][0:base]
			elif 62 < base < 95:
				self.ALPHABET[base] = self.ALPHABET[95][0:base]
			# Build conversion dictionary cache
			try:
				self.dictionary = dict((cipher, index) for index, cipher in enumerate(self.ALPHABET[base]))
			except KeyError:
				raise TypeError('Unsupported base encoding.')

			self.unbase = self._dictunbaser

	def __call__(self, string):
		return self.unbase(string)

	def _dictunbaser(self, string):
		"""Decodes a  value to an integer."""
		ret = 0

		for index, cipher in enumerate(string[::-1]):
			ret += (self.base ** index) * self.dictionary[cipher]
		return ret


class UnpackingError(Exception):
	"""Badly packed source or general error. Argument is a
	meaningful description."""
	pass

def decode(text):
	text = sub(r"\s+|/\*.*?\*/", "", text)
	data = text.split("+(ﾟДﾟ)[ﾟoﾟ]")[1]
	chars = data.split("+(ﾟДﾟ)[ﾟεﾟ]+")[1:]
	txt = ""

	for char in chars:
		char = (
			char
			.replace("(oﾟｰﾟo)", "u")
			.replace("c", "0")
			.replace("(ﾟДﾟ)['0']", "c")
			.replace("ﾟΘﾟ", "1")
			.replace("!+[]", "1")
			.replace("-~", "1+")
			.replace("o", "3")
			.replace("_", "3")
			.replace("ﾟｰﾟ", "4")
			.replace("(+", "(")
		)

		char = sub(r'\((\d)\)', r'\1', char)
		c = ""
		subchar = ""

		for v in char:
			c += v

			try:
				x = c
				subchar += str(eval(x))
				c = ""
			except:
				pass

		if subchar != '':
			txt += subchar + "|"

	txt = txt[:-1].replace('+', '')

	txt_result = "".join(
		[
			chr(int(n, 8))
			for n in txt.split('|')
		]
	)

	return toStringCases(txt_result)


def toStringCases(txt_result):
	sum_base = ""
	m3 = False

	if ".toString(" in txt_result:
		if "+(" in txt_result:
			m3 = True
			sum_base = "+" + search(".toString...(\d+).", txt_result, DOTALL).group(1)
			txt_pre_temp = findall("..(\d),(\d+).", txt_result, DOTALL)

			txt_temp = [
				(n, b)
				for b, n in txt_pre_temp
			]
		else:
			txt_temp = find_multiple_matches('(\d+)\.0.\w+.([^\)]+).', txt_result, DOTALL)

		for numero, base in txt_temp:
			code = toString(int(numero), eval(base + sum_base))

			if m3:
				txt_result = re.sub(r'"|\+', '', txt_result.replace("(" + base + "," + numero + ")", code))
			else:
				txt_result = re.sub(r"'|\+", '', txt_result.replace(numero + ".0.toString(" + base + ")", code))

	return txt_result

def toString(number, base):
	string = "0123456789abcdefghijklmnopqrstuvwxyz"

	if number < base:
		return string[number]
	else:
		return toString(number // base, base) + string[number % base]
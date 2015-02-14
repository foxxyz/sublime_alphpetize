import re

import sublime
import sublime_plugin


class AlphpetizeCommand(sublime_plugin.TextCommand):

	newline_styles = {'unix': '\n', 'lf': '\n', 'windows': '\r\n', 'crlf': '\r\n', 'mac os 9': '\r', 'cr': '\r'}

	def run(self, edit):
		"""
		Run plugin and collect classes in file
		"""

		self.settings = sublime.load_settings('Alphpetize.sublime-settings')

		view = self.view
		self.function_count = 0

		# Find classes
		classes = []
		operation_regions = view.find_all('(class|trait|interface) \w+.*\{?')
		for region in operation_regions:

			# Get full line and count indentation
			class_line = view.substr(view.line(region))
			indentation = class_line.count('\t') * '\t'

			# Ensure we didn't accidentally match a comment line with a reserved keyword in it
			if not re.match(r"[^*]*(class|trait|interface)", class_line):
				continue

			# Deal with multi-line class definitions
			if class_line.find('{') == -1:
				class_line_end = region.end()
				while view.substr(class_line_end) != '{':
					class_line_end += 1
				region = sublime.Region(region.begin(), class_line_end + 1)

			# find closing bracket with same indentation
			for end_line in view.find_all(r'^' + indentation + '\}'):
				if end_line.begin() > region.end():
					classes.append(sublime.Region(region.end(), end_line.begin()))
					break

		if not classes:
			sublime.error_message('No classes/traits/interfaces found! (This might not be a PHP file!)')
			return

		offset = 0
		for c in classes:
			offset += self.organize_class(edit, c, offset)

		sublime.status_message(str(self.function_count) + ' method(s) sorted in ' + str(len(classes)) + ' class(es)!')
		view.show(0)

	# Call once per class
	def organize_class(self, edit, c_region, offset):
		"""
		Find functions in a class, reorder them and write them back into the class
		"""

		functions = {'public static': {}, 'public': {}, 'protected static': {}, 'protected': {}, 'private static': {}, 'private': {}}
		ordered_functions = []
		newline = self.newline_styles[self.view.line_endings().lower()]
		comment_block = 0

		# Offset class to take previous replacements into account
		c_region = sublime.Region(c_region.a + offset, c_region.b + offset)

		# Cycle through lines
		for line in self.view.lines(c_region):

			# Skip comment blocks
			comment_block += self.view.substr(line).count('/*') - self.view.substr(line).count('*/')
			if comment_block:
				continue

			# Look for function definition
			ffound = re.search('^(\s*)(?:static )?(public|protected|private|) ?(?:static )?function ([a-zA-Z0-9_]+)\s*\(', self.view.substr(line))
			if ffound:

				# Note initial beginning
				function_begin = line.begin()
				brace_counter = None

				# Find where function begins and ends
				for end_line in self.view.lines(c_region):
					if end_line.begin() < line.begin():
						# Reset function beginning pointer when end brace encountered
						if re.search('(\}|\);)', self.view.substr(end_line)):
							function_begin = line.begin()
						elif re.match(r'^\s*(/\*|//)', self.view.substr(end_line)):
							function_begin = end_line.begin()
					if end_line.begin() >= line.begin():
						line_string = self.view.substr(end_line)
						# Determine end of function by counting braces per line
						if line_string.count('{') > 0 and brace_counter is None:
							brace_counter = 0
						if brace_counter is not None:
							brace_counter = brace_counter + line_string.count('{') - line_string.count('}')
						# When braces are fully matched, the class must have ended, so note the region and break
						if brace_counter == 0:
							function_region = sublime.Region(function_begin, end_line.end())
							break

				# Add to dictionary
				keyword = ffound.group(2)
				if keyword == '':
					keyword = 'public'
				if re.search('\s+static\s+', ffound.group(0)):
					keyword += ' static'
				# Prioritize to the top if listed in settings
				if ffound.group(3) in self.settings.get('prioritize'):
					sortName = '_____'
				else:
					sortName = ffound.group(3)
				functions[keyword][sortName] = function_region
				ordered_functions.append(function_region)

		# Make sure we have functions
		if not ordered_functions:
			sublime.error_message('No functions found in class.')
			return 0

		# Store stats
		self.function_count += len(ordered_functions)

		# Collect code between methods
		pre_class = self.view.substr(sublime.Region(c_region.begin(), ordered_functions[0].begin()))
		for i in range(len(ordered_functions) - 1):
			pre_class += self.view.substr(sublime.Region(ordered_functions[i].end(), ordered_functions[i + 1].begin()))
		pre_class += self.view.substr(sublime.Region(ordered_functions[-1].end(), c_region.end()))
		pre_class = re.sub('(' + (newline * 2) + ')+', (newline * 2), pre_class)

		# Sort functions by visibility and name
		sorted_classes = []
		for visibility in ['public static', 'public', 'protected static', 'protected', 'private static', 'private']:
			for name in sorted(functions[visibility].keys()):
				sorted_classes.append(self.view.substr(functions[visibility][name]))

		# Add pre-class code
		if pre_class.strip('\n\r'):
			sorted_classes.insert(0, pre_class.strip('\n\r'))

		# Combine into string
		sorted_class = newline + (newline * 2).join(sorted_classes) + newline

		# Add padding
		if self.settings.get('class_padding'):
			sorted_class = newline + sorted_class + newline

		# Replace class contents
		self.view.replace(edit, c_region, sorted_class)

		# Return offset
		return len(sorted_class) - c_region.size()

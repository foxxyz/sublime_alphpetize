import sublime, sublime_plugin, re

class AlphpetizeCommand(sublime_plugin.TextCommand):

	def run(self, edit):
		
		view = self.view

		# Find classes
		classes = []
		operation_regions = view.find_all('class \w+( extends \w+)?\s*\{')
		for region in operation_regions:

			# Get full line and count indentation
			class_line = view.substr(view.line(region))
			indentation = class_line.count('\t') * '\t'

			# find next line with same indentation
			for end_line in view.find_all(r'^' + indentation + '\S+'):
				if end_line.begin() > region.end(): 
					classes.append(sublime.Region(region.end(), end_line.begin()))
					break

		if not classes:
			sublime.error_message('No classes found! (This might not be a PHP file!)')
			return

		offset = 0
		for c in classes:
			offset += self.organize_class(edit, c, offset)

		sublime.status_message('Functions sorted!')

	# Call once per class
	def organize_class(self, edit, c_region, offset):

		functions = {'public': {}, 'protected': {}, 'private': {}}

		# Offset class to take previous replacements into account
		c_region = sublime.Region(c_region.a + offset, c_region.b + offset)
		
		# Cycle through lines
		for line in self.view.lines(c_region):

			# Look for function definition
			ffound = re.search('(\t*)(public|protected|private|) ?function ([a-zA-Z0-9_]+)\(', self.view.substr(line))
			if ffound:

				# Note indentation and initial beginning
				indentation = ffound.group(1)
				function_begin = line.begin()

				# Find where function ends and comments begin
				for end_line in self.view.find_all(r'^' + indentation + '\S+'):
					if end_line.begin() < line.begin():
						# Reset function beginning pointer when end brace encountered
						if re.search('\}', self.view.substr(end_line)): function_begin = line.begin()
						else: function_begin = end_line.begin()
					if end_line.begin() > line.end(): 
						function_region = sublime.Region(function_begin, end_line.end())
						break
				
				# Add to dictionary
				keyword = ffound.group(2)
				if keyword == '': keyword = 'public'
				functions[keyword][ffound.group(3)] = function_region

		# Sort functions by visibility and name
		sorted_class = '\n\n'
		for visibility in ['public', 'protected', 'private']:
			for name in sorted(functions[visibility].keys()):
				sorted_class += self.view.substr(functions[visibility][name]) + '\n\n'

		# Replace class contents
		self.view.replace(edit, c_region, sorted_class)

		# Return offset
		return len(sorted_class) - c_region.size()
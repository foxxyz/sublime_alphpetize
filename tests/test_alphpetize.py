import sublime, sys
from unittest import TestCase

version = sublime.version()


class test_alphpetize_command(TestCase):

    def setUp(self):
        self.view = sublime.active_window().new_file()

    def tearDown(self):
        if self.view:
            self.view.set_scratch(True)
            self.view.window().focus_view(self.view)
            self.view.window().run_command("close_file")

    def get_contents(self):
        return self.view.substr(sublime.Region(0, self.view.size()))

    def get_file(self, filename):
        with open('{0}/Alphpetize/tests/{1}'.format(sublime.packages_path(), filename), 'r') as fp:
            contents = fp.read()
        return contents

    def set_text(self, string):
        edit = self.view.begin_edit()
        self.view.replace(edit, sublime.Region(0, 1), string)
        self.view.end_edit(edit)

    def test_basic_sorting(self):
        "Ensure methods are sorted at all"
        self.set_text(self.get_file('test_basic_sorting_before.php'))
        self.view.run_command("alphpetize")
        self.assertEqual(self.get_contents(), self.get_file('test_basic_sorting_after.php'))

    def test_retain_style(self):
        "Retain style for already sorted classes"
        contents = self.get_file('test_retain_style.php')
        self.set_text(contents)
        self.view.run_command("alphpetize")
        self.assertEqual(self.get_contents(), contents)

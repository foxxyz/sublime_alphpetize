Alphpetize for Sublime
======================

Dealing with large volumes of unorganized code? Do you have Organizational OCD like me? Party people, your dreams have now been fulfilled.

The Alphpetize plugin for Sublime Text 2 scans your PHP file for class methods and organizes them by visibility and function name.

*Be warned: This plugin is in alphp stage and may not work correctly.*

Installation
------------

### With Git

Clone the package into your Sublime Text 2 Packages directory:

	git clone https://github.com/foxxyz/sublime_alphpetize.git Alphpetize
	
### Without Git

Grab the source from [Github](http://github.com/foxxyz/sublime_alphpetize), copy the whole directory into the Packages directory and rename it to "Alphpetize".

### Package Directory locations:

* OSX: `~/Library/Application\ Support/Sublime\ Text\ 2/Packages/`
* Linux: `~/.Sublime\ Text\ 2/Packages/` or `~/.config/sublime-text-2/Packages/`
* Windows: ` %APPDATA%/Sublime Text 2/Packages/` 

The plugin should be picked up automatically. If not, restart Sublime Text.

Usage
-----

After installation, select `Sort Methods` from the `Edit` menu.

Example
-------

Consider the following file:

	class Test {
	
		private function bottom() {
		
		}
		
		/**
		 * This function rocks
		 * @return void
		 */
		public function middle() {

		}
		
		public function atTheTop() {
		
		}
		
		protected function leaveMe() {
		
		}
		
	}
	
After running Alphpetize, it should look at follows:

	class Test {
	
		public function atTheTop() {
		
		}
	
		/**
		 * This function rocks
		 * @return void
		 */
		public function middle() {

		}
		
		protected function leaveMe() {
		
		}
		
		private function bottom() {
		
		}
		
	}
	
And yes, Alphpetize can also handle files with multiple class definitions.

### What about static methods?

Static methods are placed at the top of their visibility group.

### What about comments?

[DocBlocks](http://en.wikipedia.org/wiki/PHPDoc) and single `//`-style comments preceding their functions will be preserved during sorting.

### What about everything else?

Anything else found floating inbetween function definitions will be collected at the top of the class. (Why is there code between your methods anyway?)

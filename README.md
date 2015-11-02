Alphpetize for Sublime
======================

Dealing with large volumes of unorganized code? Do you have Organizational OCD like me? Party people, your dreams have now been fulfilled.

The Alphpetize plugin for Sublime Text scans your PHP file for class methods and organizes them by visibility and function name.

Installation
------------

### Using Sublime Package Control

If you are using the [Sublime Package Manager](http://wbond.net/sublime_packages/package_control), you can install Alphpetize by selecting `Package Control: Install Package` under the `Sublime Text > Preferences > Package Control` menu item. Type `Alphpetize` and install!

### With Git

Clone the package into your Sublime Text 2/3 Packages directory:

    git clone https://github.com/foxxyz/sublime_alphpetize.git Alphpetize
    
### Without Git

Grab the source from [Github](http://github.com/foxxyz/sublime_alphpetize), copy the whole directory into the Packages directory and rename it to "Alphpetize".

### Package Directory locations:

* OSX: `~/Library/Application\ Support/Sublime\ Text\ 2/Packages/`
* Linux: `~/.Sublime\ Text\ 2/Packages/` or `~/.config/sublime-text-2/Packages/`
* Windows: ` %APPDATA%/Sublime Text 2/Packages/` 

The locations for Sublime Text 3 should be identical, disregarding the version number change. The plugin should be picked up automatically. If not, restart Sublime Text.

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

### What about traits and interfaces?

Methods defined inside of traits and interfaces are also sorted.

### What about everything else?

Anything else found floating in-between function definitions will be collected at the top of the class.

Testing
-------

Tests can be run using the nice [UnitTesting](https://github.com/randy3k/UnitTesting) plugin in Package Control. 

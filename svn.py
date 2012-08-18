''' 
    - Subversion For Sublime Text2
    - By soncy
    - Need: Subversion 1.7 +
    - LastUpdate: 2012-08-18 18:31
'''

import sublime, sublime_plugin
import commands

settings   = sublime.load_settings('Subversion.sublime-settings')
svnpath    = settings.get('svnpath') or '/usr/bin'
svncommand = svnpath + '/svn';

class SubversionCommand(sublime_plugin.TextCommand):
    
    def run(self, edit, command_type):
        self.filename = self.view.file_name()
        if (command_type == 'info'):
            self.info()
        elif (command_type == 'commit'):
            self.commit()

    def info(self):
        command = svncommand + ' info ' + self.filename
        self.run_command(command)

    def commit(self):
        self.view.window().show_input_panel('Input Comment', '', self.doComit, self.on_change, self.cancel)

    # comment has be must input 
    def doComit(self, comment):
        comment = comment.strip()
        if (comment == ''):
            sublime.error_message('Must input comment')
            self.commit()
            return;
        command = svncommand + ' ci -m "' + comment + '" ' + self.filename;
        self.run_command(command)

    def cancel(self, text):
        pass

    def on_change(self, text):
        pass

    def run_command(self, command):
        self.view.window().run_command('show_panel', {"panel": "console", "reverse":True})
        status, output = commands.getstatusoutput(command)
        print(output)
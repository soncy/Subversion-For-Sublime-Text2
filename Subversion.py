''' 
    - Subversion For Sublime Text2
    - By soncy
    - Need Subversion 1.7+ support
    - LastUpdate: 2012-08-18 18:31
'''

import sublime, sublime_plugin
import commands

settings   = sublime.load_settings('Subversion.sublime-settings')
svnpath    = settings.get('svnpath') or '/usr/bin'
SVNCOMMAND = svnpath + '/svn';

class SubversionCommand(sublime_plugin.TextCommand):
    
    def run(self, edit, command_type, paths = []):
        paths_len = len(paths)
        if (paths_len > 0):
            self.filename = ' '.join(paths)
        else:    
            self.filename = self.view.file_name()

        if (command_type == 'info'):
            self.run_svn_simplecommand('info')

        elif (command_type == 'commit'):
            self.commit()

        elif (command_type == 'add'):
            self.run_svn_simplecommand('add')

        elif (command_type == 'update'):
            self.run_svn_simplecommand('up')

        elif (command_type == 'side'):
            print(self.filename)
            
        '''
            TODO:
                merge
                revert
                status
                log
                remove
                cleanup
                diff
        '''

    def commit(self):
        self.view.window().show_input_panel('Input Comment', '', self.do_commit, self.on_change, self.cancel)

    # comment has be must input 
    def do_commit(self, comment):
        comment = comment.strip()
        if (comment == ''):
            sublime.error_message('Must input comment')
            self.commit()
            return;
        command = SVNCOMMAND + ' ci -m "' + comment + '" ' + self.filename;
        self.run_command(command)

    def cancel(self):
        pass

    def on_change(self, text):
        pass

    def run_svn_simplecommand(self, command_type):
        command = ' '.join([SVNCOMMAND, command_type, self.filename])
        self.run_command(command)

    def run_command(self, command):
        self.view.window().run_command('show_panel', {"panel": "console", "reverse":True})
        status, output = commands.getstatusoutput(command)
        print(output)

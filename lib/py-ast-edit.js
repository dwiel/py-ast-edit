to'use babel';

import PyAstEditView from './py-ast-edit-view';
import { CompositeDisposable } from 'atom';

export default {

  pyAstEditView: null,
  modalPanel: null,
  subscriptions: null,

  activate(state) {
    this.pyAstEditView = new PyAstEditView(state.pyAstEditViewState);
    this.modalPanel = atom.workspace.addModalPanel({
      item: this.pyAstEditView.getElement(),
      visible: false
    });

    // Events subscribed to in atom's system can be easily cleaned up with a CompositeDisposable
    this.subscriptions = new CompositeDisposable();

    // Register command that toggles this view
    this.subscriptions.add(atom.commands.add('atom-workspace', {
      'py-ast-edit:select-parent': () => this.select_parent()
    }));
  },

  deactivate() {
    this.modalPanel.destroy();
    this.subscriptions.dispose();
    this.pyAstEditView.destroy();
  },

  serialize() {
    return {
      pyAstEditViewState: this.pyAstEditView.serialize()
    };
  },

  select_parent() {
    var spawn = require('child_process').spawn
    var py = spawn('python', ['/Users/zdwiel/github/py-ast-edit/compute_input.py'])

    let editor
    if (editor = atom.workspace.getActiveTextEditor()) {
      dataString = '';

      py.stdout.on('data', function(data){
        dataString += data.toString();
      });
      py.stdout.on('end', function(){
        console.log(dataString);
      });
      py.stderr.on('data', function(data){
        dataString += data.toString();
      });
      py.stderr.on('end', function(){
        console.log(dataString);
        lines = dataString.split('\n')
        last_line = lines[lines.length - 2]
        data = JSON.parse(last_line)
        editor.setSelectedBufferRange(data)
      });
      py.stdin.write(JSON.stringify({
        'cursor_position': editor.getCursorBufferPosition(),
        'selected_range': editor.getSelectedBufferRange()
      }))
      py.stdin.write('\n');
      py.stdin.write(editor.getText());
      py.stdin.end();
    }
  }

};

# VimNote - a vim-based TUI notetaking application

## Install
VimNote is a Python 3.10 application, so it can be installed with `pip install vimnote` (or `pip3` if necessary). You will also need Vim installed.

## Getting started
Run VimNote from the terminal, optionally specifying the name of a book to open. The book name can be autocompleted with tab in most shells.

## Interface
There are three main "views" in VimNote:
- book view
- note view
- edit view

Edit view is essentially just a Vim instance, while book and note views are lists of books and notes respectively.

To make a new book or note, hit `n` while in book or note view. You will be asked for a name, and then dropped into edit mode. Book and note names should be unique. You can rename or delete a book or note with `r` and `d`. Deleting will prompt a confirmation box which can be disabled for the current session, or disabled entirely from `vimnoterc` (see below).

Book and note views can be navigated with `j` and `k` (or arrow keys), similar to lines in Vim. You can go to the top or bottom with `g` or `G` respectively, similar to `more`. You can also go to a specific line number by typing it, or search by first typing `/`. This will filter all the notes or books that have the searched string in the title. To open the selected note or book, hit `enter`. VimNote can be quit in either of these modes at any time with `q`, `^C`, or `^D`.

Book and note views both have some analytics about each entry. From left to right, this is:
- book view
    - book name (the majority of the width)
    - number of notes
    - date and time that the book was created 
    - date and time that the last note in the book was edited
- note view
    - note title (the majority of the width)
    - number of lines
    - date and time that the note was created
    - date and time that the note was last edited

Any of these can be used for sorting by with the F-keys they are labelled with, toggling between ascending and descending. By default, notes and books are ordered by the most recently edited notes.

In note view, note previews can be toggled with `p`. This will reveal the first dozen or so lines (depending on terminal size) using the bottom half of the terminal.

## Config
### vimrc
While most of the config happens in `vimnoterc` (see below), you can change how Vim sees VimNote files for syntax highlighting and indenting rules in your vimrc. To do this, add the following line to your vimrc:
```vim
autocmd BufRead,BufNewFile *.vmnt set filetype=your_filetype_here
```
where `your_filetype_here` is a valid Vim filetype. For a list of filetypes, type `:setfiletype ` (with a space at the end) in Vim and hit tab, or if you have a file whose type you want to use, run `:set filetype` (with a space in between) while editing that file. I use `markdown` but you can use whatever you'd like, or even make your own.

### vimnoterc
The config file for VimNote is `~/.config/vimnoterc`. Use `#` at the start of a line for a comment. The syntax is `option = value`. Valid options are as follows:

option|description|default
-|-|-
previewratio|the amount of the screen that the note preview uses, 0.0 to 1.0|0.5
confirmdelete|whether to ask for confirmation before deleting, True or False|True
notedir|where vimnote files are stored|`~/.vimnote/`

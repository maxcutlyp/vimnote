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

Edit view is essentially just a Vim instance, while book and note views are lists of books and notes respectively which can be navigated with `j` and `k`. Other keybinds for book and note view are as follows:

key|what it does
-|-
`enter`|opens the selected book or note
`n`|creates a new book or note, then opens it
`r`|renames the selected book or note
`d`|prompts to delete the selected book or note
`p`|opens a preview of the selected book or note on the bottom half of the terminal
`g`|goes to the top of the list
`G`|goes to the bottom of the list
`/`|starts searching
`q`, `^C`, `^D`|quits VimNote

Book and note views both have some analytics about each entry. From left to right, this is:
- book view
    - book name (the majority of the width)
    - number of notes
    - date and time that the last note in the book was edited
- note view
    - note title (the majority of the width)
    - number of lines
    - date and time that the note was last edited

Any of these can be used for sorting by with the F-keys they are labelled with, toggling between ascending and descending. By default, notes and books are ordered by the most recently edited.

## Config
### vimrc
While most of the config happens in `~/.config/vimnote` (see below), you can change how Vim sees VimNote files for syntax highlighting and indenting rules in your vimrc. To do this, add the following line to your vimrc:
```vim
autocmd BufRead,BufNewFile *.vmnt set filetype=your_filetype_here
```
where `your_filetype_here` is a valid Vim filetype. For a list of filetypes, type `:setfiletype ` (with a space at the end) in Vim and hit tab, or if you have a file whose type you want to use, run `:set filetype` (with a space in between) while editing that file. I use `markdown` but you can use whatever you'd like, or even make your own.

### ~/.config/vimnote
The config file for VimNote is `~/.config/vimnote`. The default is show below:

```ini
previewratio = 0.5              # the amount of the terminal that the preview uses
previewside = bottom            # the side that the preview opens into. allowed values: bottom, top, left, right
confirmdelete = true            # whether or not to ask before deleting
notedir = ~/.vimnote/           # where vimnote books and notes are stored
dateformat = %I:%M%p %m-%d-%Y   # see https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior
defaultsortcol = 2              # the default column to sort by, zero-indexed
defaultsortascending = true     # whether to sort the above column ascending or descending (true or false)
```

## TODO:

- fixes
    - deletion dialog overflow
- features
    - preview
    - config options

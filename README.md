# dictator.py 

A program that _"visually dictates"_ text files.

## Usage

```sh
$ ./dictator.py <filename>
```

| Key                          | Description                |
| ---------------------------- | -------------------------- |
| <kbd>Q</kbd>, <kbd>Esc</kbd> | quit                       |
| <kbd>R</kbd>                 | reload file                |
| <kbd>SPACE</kbd>             | step forward  by 1 token   |
| <kbd>LEFT ARROW</kbd>        | step backward by 1 token   |
| <kbd>TAB</kbd>               | step forward by 10 tokens  |
| <kbd>BACKSPACE</kbd>         | step backward by 10 tokens |
| <kbd>0</kbd>-<kbd>9</kbd>    | jump to 0%-90% progress    |
| *any other key*              | jump forwad by 1 token     |

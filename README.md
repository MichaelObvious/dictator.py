# dictator.py 

A program that _"visually dictates"_ text files.

## Usage

```sh
$ ./dictator.py <filename>
```

| Key                             | Description                |
| ------------------------------- | -------------------------- |
| <kbd>Q</kbd>, <kbd>Esc</kbd>    | quit                       |
| <kbd>ENTER</kbd>                | step forward  by 1 token   |
| <kbd>LEFT ARROW</kbd>           | step backward by 1 token   |
| <kbd>TAB</kbd>                  | jump forward by 10 tokens  |
| <kbd>BACKSPACE</kbd>            | jump backward by 10 tokens |
| <kbd>0</kbd>-<kbd>9</kbd>       | jump to 0%-90% progress    |
| <kbd>SPACE</kbd>                | toggle autoplay            |
| <kbd>S</kbd>                    | increase autoplay speed    |
| <kbd>Shift</kbd> + <kbd>S</kbd> | decrease autoplay speed    |
| <kbd>R</kbd>                    | reload file                |
| *any other key*                 | step forwad by 1 token     |

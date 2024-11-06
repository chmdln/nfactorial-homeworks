# ASCII Art Generator

A command-line tool to generate ASCII art from text input, with options for color, alignment, and output format.

## Usage

```bash
python3 main.py [OPTIONS] [TEXT] [BANNER]
```

# Arguments 

<b>[TEXT]</b> (positional): &nbsp; the text to convert into ASCII art. Accepts standard ASCII characters only.  
#### Example usage 

```bash
python3 main.py 'Hello, W0rld!' | cat -e
```
<br>


<b>[BANNER]</b> (optional, positional): &nbsp; the ASCII art style. Supported options: 
- standard (default)
- shadow
- thinkertoy

#### Example usage 

```bash
python3 main.py 'Hello, W0rld!' standard | cat -e
```
```bash
python3 main.py 'Hello, W0rld!' thinkertoy | cat -e
```
<br>


# Options 

<b>[--output]</b>: &nbsp; specify a file path to save the ASCII art output. If not specified, output is printed to the console.

#### Example usage

```bash
python3 main.py --output='output.txt' 'Hello, W0rld!' 
cat -e output.txt 
```
<br>


<b>[--color]</b>: &nbsp; apply a color to the ASCII art. Supported colors: 
- black
- red 
- green
- yellow
- blue
- magenta
- cyan
- white


<b>[--letters]</b>: &nbsp; specify particular letters to color. Only these letters will appear in the specified color (requires --color to be set).

#### Example usage

```bash
python3 main.py --color=red 'Hello, W0rld!'
```

```bash
python3 main.py --color='cyan' --letters='a0lW' 'Hello, W0rld!'
```

```bash
python3 main.py --color magenta --letters='a0lW' 'Hello, W0rld!' standard 
```

<br>

<b>[--align]</b>: &nbsp; Align the text within the terminal. Options:
- left: Align text to the left.
- center: Center-align text in the terminal width.
- right: Align text to the right side of the terminal.
- justify: Distribute space evenly between words, aligning both sides of the text block (for multi-word inputs).


#### Example usage

```bash
python3 main.py --align=right 'Hello, W0rld!'
```

```bash
python3 main.py --align='center' 'Hello,\n W0rld!'
```


```bash
python3 main.py --align justify 'Hello, W0rld!\nHello H4M2n!'
```
<br>

# Combining multiple options 

#### Example usage 

```bash
python3 main.py --output='test.txt' --color='cyan' --letters='Ttoi' --align='justify' 'Testing long\n output!' standard
cat test.txt
```

#### Note: 
When combining multiple options, use explicit flag definitions to avoid ambiguity. For example, use 

```bash 
python3 main.py --color=magenta --letters='a0lW' 'Hello, W0rld!' standard 
``` 

instead of this 

```bash 
python3 main.py --color magenta 'a0lW' 'Hello, W0rld!' standard 
``` 

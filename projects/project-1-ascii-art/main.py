import sys 
import shutil
import argparse 


class AsciiArtGenerator:
    ANSI_COLOR_MAP = {
        'black':   '\033[30m',
        'red':     '\033[31m',
        'green':   '\033[32m',
        'yellow':  '\033[33m',
        'blue':    '\033[34m',
        'magenta': '\033[35m',
        'cyan':    '\033[36m',
        'white':   '\033[37m',
        'reset':   '\033[0m'
    } 

    def __init__(self, args): 
        self.args = args 
        self.symbol_height = 8 
        self.ascii_dict = self.load_ascii_art()
        self.char_widths = {char: len(lines[-1])-1 for char,lines in self.ascii_dict.items()} 
        self.color_code = self.ANSI_COLOR_MAP.get(args.color, '') 
        self.colored_letters = set(args.letters) if args.letters else set() 
        self.terminal_width = shutil.get_terminal_size().columns

    def load_ascii_art(self): 
        file_name = f"./data/{args.banner}.txt"
        with open(file_name, 'r') as file:
            lines = file.readlines()

        ascii_dict = {}
        current_art = []
        curr_ascii_order = 0 
        for line in lines[1:]: 
            if len(current_art) < self.symbol_height:
                current_art.append(line)
            else: 
                ascii_dict[chr(curr_ascii_order + ord(' '))] = current_art
                current_art = []
                curr_ascii_order += 1 
        return ascii_dict 

    def get_color_text(self, art_char, char): 
        if self.colored_letters: 
            if char in self.colored_letters: 
                return f"{self.color_code}{art_char}{self.ANSI_COLOR_MAP['reset']}"
        elif self.color_code: 
            return f"{self.color_code}{art_char}{self.ANSI_COLOR_MAP['reset']}"
        return art_char 


    def align_text(self, w, line): 
        split_words = w.split() 
        line_output = "".join(line)
        stripped_line = line_output.replace(self.color_code, '').replace(self.ANSI_COLOR_MAP['reset'], '')
        
        if args.align == 'justify':
            if len(split_words) > 1: 
                padding = int((self.terminal_width - len(stripped_line))/(len(split_words)-1))
                line_output = line.copy()
                index = 0
                for k, sub in enumerate(split_words[:-1]): 
                    index += len(sub)
                    if k > 0: 
                        index += 1
                    line_output[index] += " " * padding
                line_output = "".join(line_output)
            else: 
                padding = (self.terminal_width - len(stripped_line)) // 2
                line_output = " " * max(padding, 0) + line_output
        
        elif (args.align == "center"):
            padding = (self.terminal_width - len(stripped_line)) // 2
            line_output = " " * max(padding, 0) + line_output
        elif args.align == "right":
            padding = self.terminal_width - len(stripped_line)
            line_output = " " * max(padding, 0) + line_output
        return line_output 


    def process_text(self): 
        words = args.text 
        words = bytes(args.text, "utf-8").decode("unicode_escape")
        if words == "": 
            if args.output:
                with open(args.output, 'w') as f:
                    pass
            sys.exit(0) 
        if words == "\n":
            if args.output:
                with open(args.output, 'w') as f:
                    pass
            else: 
                sys.stdout.write("\n")
                sys.exit(0)  
        

        output = []
        words = words.split("\n")
        for w in words: 
            if w == '':
                output.append('\n')
            else: 

                res = [[] for i in range(self.symbol_height)]
                for i in range(self.symbol_height): 
                    for j, char in enumerate(w):
                        art_char = self.ascii_dict[char][i].rstrip()
                        art_char += " " * (self.char_widths[char] - len(art_char))
                        if j == len(w) - 1:
                            art_char += "\n"
                        res[i].append(self.get_color_text(art_char, char))

                    if args.align: 
                        line_output = self.align_text(w, res[i])
                    else: 
                        line_output = "".join(res[i])
                    res[i] = [line_output]

                output.append("".join(["".join(level) for level in res]))


        output_text = "".join(output)
        if args.output:
            with open(args.output, 'w') as f:
                f.write(output_text)  
        else: 
            sys.stdout.write(output_text)  
            sys.exit(0)




if __name__ == "__main__": 
    parser = argparse.ArgumentParser(description="Convert text to ASCII art.", usage = "python3 main.py [OPTION] [STRING] [BANNER]")
    parser.add_argument("--output", type=str, help="Output file to save ASCII art (optional)")
    parser.add_argument("--color", type=str, choices= AsciiArtGenerator.ANSI_COLOR_MAP.keys(), help="Color of ASCII art letters (optional)")
    parser.add_argument("--letters", nargs = "?", type=str, help="Letters to color in the ASCII art")
    parser.add_argument("--align", type=str, choices=["left", "center", "right", "justify"], help="Text alignment")
    parser.add_argument("text", type=str, help="The text to convert to ASCII art.")
    parser.add_argument("banner", nargs = "?", choices=['standard', 'shadow', 'thinkertoy'], default='standard', help="Banner type (default: standard)") 


    args = parser.parse_args()
    generator = AsciiArtGenerator(args)
    generator.process_text()


import inspect

#text="""test
#  test2
#  abc
#    def
#test"""

def getspaces(line): 
  if line.replace(" ", "") == "": # If line is just spaces
    return len(line)
  if line == "":
    return 0

  n = 0
  while line[n] == " ":
    if len(line) - 1 > n:
      n += 1
    else:
      break
    
  return n


def parse(text):

  lines = (text.replace("import pycraft", "").strip() + "\n").split("\n")
  output = []

  indents = [0]
  lastindent = 0

  prettyprint = False
  #prettyprint = True

  for linenum in range(len(lines)):
    line = lines[linenum]

    if line.replace(" ", "") != "" or linenum == len(lines) - 1: # If line is not just spaces (override for last line to unindent)

      spaces = getspaces(line)

      if spaces != lastindent:
        if spaces > lastindent: # Indent
          indents.append(spaces)
          lastindent = spaces
          if prettyprint:
            output.append(indents[indents.index(spaces) - 1] * " " + "{")
          else:
            output.append("{")
        elif spaces < lastindent: # Unindent 
          try:
            unindents = len(indents) - indents.index(spaces) - 1
            for n in range(unindents):
              if prettyprint:
                output.append(indents[len(indents) - n - 2] * " " + "}")
              else:
                output.append("}")
            indents = indents[:indents.index(spaces) + 1]
          except ValueError:
            return ["error", linenum + 1, line, len(line), "IndentationError: unindent does not match any outer indentation level"]
      
      if prettyprint:
        output.append(line) # No compiling here yet
      else:
        try:
          output.append(compilestatement(line.strip()))
        except:
          output.append(line.strip())

  return ("\n".join(output)).strip()

def isValidVariable(name):
  if name[0].isalpha():# or name[0] == "_":
    for letter in name:
      if not (letter.isalnum() or letter == "_"):
        return False
      return True
  else:
    return False

def compilestatement(text):

  lines = text.strip().split("\n")
  output = []

  for linenum in range(len(lines)):
    line = lines[linenum]

    if line.startswith("#") or line == "": # Just to make it work with raw unparsed code for testing
      continue

    words = line.split(" ")

    if words[1] == "=": # Assignment
      if isValidVariable(words[0]):
        output.append("/data modify storage pycraft-variables " + words[0] + " set value " + " ".join(words[2:]))
      else:
        raise SyntaxError("Bad variable name")

    else:
      raise SyntaxError("invalid syntax")

  return ("\n".join(output)).strip()
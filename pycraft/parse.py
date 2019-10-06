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
        output.append(line)
      else:
        output.append(line.strip())

  return ("\n".join(output)).strip()
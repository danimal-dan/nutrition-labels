import warnings
from AveryLabels import AveryLabel
from Models import Label
from reportlab.pdfgen.canvas import Canvas
from reportlab.pdfbase.pdfmetrics import stringWidth

LABEL_NAME_FONT = "Helvetica-Bold"
LABEL_NAME_FONT_SIZE = 13
INGREDIENT_FONT = "Helvetica"
INGREDIENT_FONT_SIZE = 10
PADDING = 3

def render_function(canv: Canvas, width: int, height: int, label: Label, headerLine: str = '', debugTemplateEdges: bool = False):
  print('Label = ', headerLine, label.name, ' - ', ', '.join([str(ingredient) for ingredient in label.ingredients]))

  if debugTemplateEdges:
    canv.drawString(0, height, '+')
    canv.drawString(width, height, '+')
    canv.drawString(0, 0, '+')
    canv.drawString(width, 0, '+')

  x = PADDING * 2
  y = height - PADDING

  ## write header
  canv.setFont(INGREDIENT_FONT, INGREDIENT_FONT_SIZE)
  if headerLine and (label.name or label.getIngredientList()):
    canv.drawString(x, y, headerLine)
    y -= LABEL_NAME_FONT_SIZE
    y -= PADDING

  ## write label name
  canv.setFont(LABEL_NAME_FONT, LABEL_NAME_FONT_SIZE)
  canv.drawString(x, y, label.name)

  y -= LABEL_NAME_FONT_SIZE
  y -= PADDING

  ## write ingredients
  canv.setFont(INGREDIENT_FONT, INGREDIENT_FONT_SIZE)
  
  maxStringWidth = width - (PADDING * 2)
  lines = divideIngredientListIntoLines(label.getIngredientList(), canv, maxStringWidth)

  for line in lines:
    if y < 0:
      warnings.warn("Label '" + label.name + "' ingredient list has exceeded allowed height" )
      break
    canv.drawString(x, y, line.strip())
    y -= INGREDIENT_FONT_SIZE + 1


def divideIngredientListIntoLines(ingredients: list[str], canv: Canvas,  maxWidth: int):
  lines = []
  currentLine = []
  for ingredient in ingredients:
    test_line = ', '.join(currentLine + [ingredient])
    if (stringWidth(test_line, canv._fontname, canv._fontsize) <= maxWidth):
      currentLine.append(ingredient)
    else:
      lines.append(', '.join(currentLine))
      currentLine = [ingredient]
  if currentLine:
    lines.append(', '.join(currentLine)) # add last line

  return lines


def generate_pdf(template: AveryLabel, labels: list[Label], headerLine: str = ''):
  template.open('test.pdf')
  if headerLine:
    template.render(lambda *args, **kwargs: render_function(*args, headerLine, **kwargs), iter(labels), headerLine)
  else:
    template.render(render_function, iter(labels), headerLine)
  template.close()

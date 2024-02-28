import warnings
from AveryLabels import AveryLabel
from Models import Label
from reportlab.pdfgen.canvas import Canvas
from reportlab.pdfbase.pdfmetrics import stringWidth

HEADER_FONT = "Helvetica-Bold"
HEADER_FONT_SIZE = 10
LABEL_FONT = "Helvetica"
LABEL_FONT_SIZE = 8
PADDING = 3

def render_function(canv: Canvas, width: int, height: int, label: Label):
  print('position', width, height)
  print(label.name, ', '.join([str(ingredient) for ingredient in label.ingredients]))

  x = PADDING
  y = height - PADDING

  ## write header
  canv.setFont(HEADER_FONT, HEADER_FONT_SIZE)
  canv.drawString(x, y, label.name)

  y -= HEADER_FONT_SIZE
  y -= PADDING

  ## write ingredients
  canv.setFont(LABEL_FONT, LABEL_FONT_SIZE)
  
  maxStringWidth = width - (PADDING * 2)
  lines = divideIngredientListIntoLines(label.getIngredientList(), canv, maxStringWidth)

  for line in lines:
    if y < 0:
      warnings.warn("Label '" + label.name + "' ingredient list has exceeded allowed height" )
      break
    canv.drawString(x, y, line.strip())
    y -= LABEL_FONT_SIZE + 1


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


def generate_pdf(template: AveryLabel, labels: list[Label]):
  template.open('test.pdf')
  template.render(render_function, iter(labels))
  template.close()


def test_latex(s):
    from matplotlib.font_manager import FontProperties
    from matplotlib.mathtext import MathTextParser
    prop = FontProperties()
    parser = MathTextParser('path')
    width, height, depth, _, _ = parser.parse(s, dpi=72, prop=prop)
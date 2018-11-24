#!/usr/bin/env python

# These two lines are only needed if you don't put the script directly into
# the installation directory
from simplestyle import *
import inkex
import sys
import pystache
import string
sys.path.append('/usr/share/inkscape/extensions')

# We will use the inkex module with the predefined Effect base class.
# The simplestyle module provides functions for style parsing.


class HelloWorldEffect(inkex.Effect):
    def __init__(self):
        inkex.Effect.__init__(self)

        self.OptionParser.add_option('-w', '--what', action='store',
                                     type='string', dest='what', default='World',
                                     help='What would you like to greet?')

    def effect(self):
        what = self.options.what

        svg = self.document.getroot()
        textElements = self.document.xpath(
            '//svg:text', namespaces=inkex.NSS)

        for e in textElements:
            style = e.get('style')
            line_height = inkex.unittouu(parseStyle(style)["line-height"])
            font_size = inkex.unittouu(parseStyle(style)["font-size"])
            font_spacing = font_size * line_height
            x = e.get('x')
            y = inkex.unittouu(e.get('y'))

            old_text = string.join(e.xpath(".//text()"), "\n")
            print(old_text)
            for tspan in e.getchildren():
                e.remove(tspan)

            json_data = {"repo": [
                {"name": "resque"},
                {"name": "hub"},
                {"name": "rip"}
            ]
            }

            new_text = pystache.render(old_text, json_data)

            lines = new_text.split("\n")
            print(lines)

            for line in lines:
                tspan = inkex.etree.Element(inkex.addNS('tspan', 'svg'), attrib={
                    inkex.addNS('role', 'sodipodi'): 'line',
                    'x': x,
                    'y': str(y)})
                tspan.text = line + "\n"
                e.append(tspan)
                y += font_spacing

        currentFileName = './output.svg'
        outFile = open(currentFileName, 'w')
        self.document.write(outFile)
        outFile.close()


effect = HelloWorldEffect()
effect.affect()

# encoding: utf-8

###########################################################################################################
#
#
# 	Reporter Plugin
#
# 	Read the docs:
# 	https://github.com/schriftgestalt/GlyphsSDK/tree/master/Python%20Templates/Reporter
#
#
###########################################################################################################


from __future__ import division, print_function, unicode_literals
import objc
from GlyphsApp import *
from GlyphsApp.plugins import *
from vanilla import *
from Foundation import CALayer

GLYPH_KEY = "com.leedotype.LDGlobalBackground.glyph"
WIDTH_KEY = "com.leedotype.LDGlobalBackground.width"
COLOR_KEY = "com.leedotype.LDGlobalBackground.color"

WHITE = NSColor.whiteColor()
CLEAR = NSColor.clearColor()

defaults = Glyphs.defaults


MAX_VALUE = 300

BORDER_WIDTH = 3

BUTTON_SIZE = 13 + 2 * BORDER_WIDTH


def clamp(num, min, max):
    if num < min:
        return min
    if num > max:
        return max
    return num


class LDGlobalBackground(ReporterPlugin):

    @objc.python_method
    def settings(self):
        try:
            width = 180

            stroke_slider_height = 39

            self.color = defaults.get(COLOR_KEY, 11)

            self.stroke_width = defaults.get(WIDTH_KEY, 30)

            self.colors = [
                NSColor.redColor(),
                NSColor.orangeColor(),
                NSColor.brownColor(),
                NSColor.yellowColor(),
                NSColor.greenColor(),
                NSColor.systemGreenColor(),
                NSColor.blueColor(),
                NSColor.systemBlueColor(),
                NSColor.purpleColor(),
                NSColor.magentaColor(),
                NSColor.lightGrayColor(),
                NSColor.darkGrayColor(),
            ]

            self.color_buttons = [
                SquareButton(
                    (0, 0, 14, 14),
                    " ",
                    sizeStyle="mini",
                    callback=self.colorHandlerBuilder(i),
                )
                for i in range(len(self.colors))
            ]

            for i, button in enumerate(self.color_buttons):
                b = button.getNSButton()

                b.setTranslatesAutoresizingMaskIntoConstraints_(False)

                b.heightAnchor().constraintEqualToConstant_(BUTTON_SIZE).setActive_(
                    True
                )
                b.widthAnchor().constraintEqualToConstant_(BUTTON_SIZE).setActive_(True)

                b.setWantsLayer_(True)
                l = button.getNSButton().layer()

                if l is not None:
                    l.setFrame_(((0, 0), (BUTTON_SIZE, BUTTON_SIZE)))
                    backgroundLayer = CALayer.alloc().init()
                    l.insertSublayer_atIndex_(backgroundLayer, 0)
                    backgroundLayer.setFrame_(
                        (
                            (BORDER_WIDTH, BORDER_WIDTH),
                            (
                                BUTTON_SIZE - 2 * BORDER_WIDTH,
                                BUTTON_SIZE - 2 * BORDER_WIDTH,
                            ),
                        )
                    )
                    backgroundLayer.setCornerRadius_(BUTTON_SIZE / 2 - BORDER_WIDTH)
                    backgroundLayer.setBackgroundColor_(self.colors[i].CGColor())

                    borderLayer = CALayer.alloc().init()
                    l.insertSublayer_atIndex_(borderLayer, 0)
                    borderLayer.setFrame_(((0, 0), (BUTTON_SIZE, BUTTON_SIZE)))
                    borderLayer.setCornerRadius_(BUTTON_SIZE / 2)

                    borderLayer.setBorderWidth_(BORDER_WIDTH)
                    if i == self.color:
                        borderLayer.setBorderColor_(WHITE.CGColor())
                    else:
                        borderLayer.setBorderColor_(CLEAR.CGColor())

                b.setBordered_(False)

            self.color_picker = Window((width, 48))
            self.color_picker.group = Group((0, 0, width, 48))

            self.color_picker.group.vertical_stack = VerticalStackView(
                (0, 0, 0, 0),
                views=[
                    dict(
                        view=HorizontalStackView(
                            (0, 0, 0, 0),
                            views=[
                                dict(view=button) for button in self.color_buttons[:6]
                            ],
                            spacing=6,
                        )
                    ),
                    dict(
                        view=HorizontalStackView(
                            (0, 0, 0, 0),
                            views=[
                                dict(view=button) for button in self.color_buttons[6:]
                            ],
                            spacing=6,
                        )
                    ),
                ],
                spacing=6,
            )

            self.stroke_slider = Window((width, stroke_slider_height))
            self.stroke_slider.group = Group((0, 0, width, stroke_slider_height))
            self.stroke_slider.group.title = TextBox(
                (18, 2, -18, 16), "Stroke Weight", sizeStyle="small"
            )
            self.stroke_slider.group.slider = Slider(
                (20, 22, 98, 11),
                minValue=0,
                maxValue=MAX_VALUE,
                value=self.stroke_width,
                sizeStyle="small",
                callback=self.strokeSliderCallback_,
            )

            self.stroke_slider.group.edit_text = EditText(
                (126, 20, 32, 19),
                text=str(self.stroke_width),
                sizeStyle="small",
                continuous=False,
                callback=self.strokeEditTextCallback_,
            )

            self.menuName = Glyphs.localize(
                {
                    "en": "LD Global Background",
                }
            )

            submenu = NSMenu.new()
            # fill submenu

            self.glyph_item = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(
                "Set Background", self.setBackgroundGlyph_, ""
            )
            self.glyph_item.setTarget_(self)

            self.width_item = NSMenuItem.new()
            self.width_item.setView_(self.stroke_slider.group.getNSView())

            self.color_item = NSMenuItem.new()
            self.color_item.setView_(self.color_picker.group.getNSView())

            submenu.addItem_(self.glyph_item)
            submenu.addItem_(self.width_item)
            submenu.addItem_(self.color_item)

            item = NSMenuItem.new()
            item.setTitle_("LD Global Background")
            item.setSubmenu_(submenu)

            self.generalContextMenus = [{"menu": item}]

        except Exception as e:
            print(e)

    @objc.python_method
    def colorHandlerBuilder(self, tag):
        def colorHandler_(sender):
            print("button clicked", tag)
            for i, button in enumerate(self.color_buttons):
                l = button.getNSButton().layer()

                borderLayer = l.sublayers()[0]
                print(borderLayer, l.sublayers())
                if i != tag:
                    borderLayer.setBorderColor_(CLEAR.CGColor())
                else:
                    borderLayer.setBorderColor_(WHITE.CGColor())

            self.color = tag
            defaults[COLOR_KEY] = tag
            Glyphs.redraw()

        return colorHandler_

    def setBackgroundGlyph_(self, sender):
        layers = Glyphs.font.selectedLayers
        if len(layers) == 0:
            return
        layer = Glyphs.font.selectedLayers[0]
        glyph = layer.parent
        self.setMemory(glyph.name)
        Glyphs.redraw()

    @objc.python_method
    def setMemory(self, glyph_name):
        Glyphs.defaults[GLYPH_KEY] = glyph_name

    @objc.python_method
    def getMemory(self):
        try:
            current_layer_id = Glyphs.font.selectedFontMaster.id

            glyph_name = Glyphs.defaults.get(GLYPH_KEY)

            if glyph_name is None:
                return None

            glyph = Glyphs.font.glyphs[glyph_name]
            if glyph is None:
                return None

            layer = glyph.layers[current_layer_id]
            if layer is None:
                return None

            return layer.completeBezierPath

        except Exception as e:
            print(e)
            return None

    @objc.python_method
    def setWidthValue(self, num):
        num = clamp(num, 0, MAX_VALUE)
        num = round(num)
        self.stroke_width = num
        self.stroke_slider.group.slider.set(num)
        self.stroke_slider.group.edit_text.set(str(num))
        defaults[WIDTH_KEY] = num
        Glyphs.redraw()

    def strokeEditTextCallback_(self, sender):
        value = sender.get()
        # parse value as integer to variable named num, if failed set num to 30
        try:
            num = int(value)
        except:
            num = 30
        self.setWidthValue(num)

    def strokeSliderCallback_(self, sender):
        self.setWidthValue(sender.get())

    @objc.python_method
    def background(self, layer):
        try:
            if self.stroke_width == 0:
                return

            glyph_name = Glyphs.defaults.get(GLYPH_KEY)
            if layer.parent.name == glyph_name:
                return

            path = self.getMemory()
            if path is None:
                return

            rect = NSMakeRect(0, -500, layer.width, 2000)

            self.colors[self.color].set()

            defaultWidth = NSBezierPath.defaultLineWidth()
            responsiveWidth = (
                float(self.stroke_width) / 100.0
            ) * self.getScale() ** 0.9

            width = max(defaultWidth / 2, responsiveWidth)

            path.setLineWidth_(width)

            NSBezierPath.clipRect_(rect)

            path.addClip()

            path.stroke()
        except Exception as e:
            print(e)

    @objc.python_method
    def inactiveLayerForeground(self, layer):
        try:
            if self.stroke_width == 0:
                return
            glyph_name = Glyphs.defaults.get(GLYPH_KEY)
            if layer.parent.name == glyph_name:
                return
            path = self.getMemory()
            if path is None:
                return

            rect = NSMakeRect(0, -500, layer.width, 2000)

            self.colors[self.color].set()

            defaultWidth = NSBezierPath.defaultLineWidth()
            responsiveWidth = (
                float(self.stroke_width) / 100.0
            ) * self.getScale() ** 0.9

            width = max(defaultWidth / 2, responsiveWidth)

            path.setLineWidth_(width)

            NSBezierPath.clipRect_(rect)

            path.addClip()

            path.stroke()
        except:
            pass

    @objc.python_method
    def preview(self, layer):
        NSColor.textColor().set()
        if layer.paths:
            layer.bezierPath.fill()
        if layer.components:
            NSColor.highlightColor().set()
            for component in layer.components:
                component.bezierPath.fill()

    def doSomething_(self, sender):
        print("Just did something")

    @objc.python_method
    def conditionalContextMenus(self):

        # Execute only if layers are actually selected
        if Glyphs.font.selectedLayers:
            self.glyph_item.setEnabled_(True)

            layer = Glyphs.font.selectedLayers[0]
            glyph = layer.parent
            if glyph.unicode:
                # unicode is in hex. Convert to int
                unicode_value = int(glyph.unicode, 16)

                # convert to string
                glyph_name = chr(unicode_value)
            else:
                glyph_name = glyph.name
            self.glyph_item.setTitle_(
                Glyphs.localize(
                    {
                        "en": f"Set {glyph_name} to Background",
                        "ko": f"{glyph_name} 글자를 배경으로 사용하기",
                    }
                )
            )

        else:
            self.glyph_item.setEnabled_(False)

    def doSomethingElse_(self, sender):
        print("Just did something else")

    @objc.python_method
    def __file__(self):
        """Please leave this method unchanged"""
        return __file__

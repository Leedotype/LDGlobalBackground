# encoding: utf-8

###########################################################################################################
#
#
#	Reporter Plugin
#
#	Read the docs:
#	https://github.com/schriftgestalt/GlyphsSDK/tree/master/Python%20Templates/Reporter
#
#
###########################################################################################################


from __future__ import division, print_function, unicode_literals
import objc
from GlyphsApp import *
from GlyphsApp.plugins import *
from vanilla import *

class LDGlobalBackground(ReporterPlugin):

	@objc.python_method
	def settings(self):
		try:
			width = 180

			stroke_slider_height = 39

			self.stroke_width = 30

			self.stroke_slider = Window((width, stroke_slider_height))
			self.stroke_slider.group = Group((0, 0, width, stroke_slider_height))
			self.stroke_slider.group.title = TextBox((18, 2, -18, 16), "Stroke Weight", sizeStyle="small")
			self.stroke_slider.group.slider = Slider(
				(20, 22, 98, 11), 
				minValue=0,
				maxValue=100,
				value=self.stroke_width,
				sizeStyle="small", 
				callback=self.stroke_slider_callback)

			self.stroke_slider.group.edit_text = EditText(
				(126, 20, 28, 19),
				text=str(self.stroke_width),
				sizeStyle="small",
				callback=self.stroke_edit_text_callback
			)


			self.menuName = Glyphs.localize({
				'en': 'LD Global Background',
				})
			self.generalContextMenus = [{
				'name': Glyphs.localize({
					'en': 'Do something',
					}), 
				'action': self.doSomething_
				},
				{
					"view": self.stroke_slider.group.getNSView()
				}
				]
		except Exception as e:
			print(e)

	@objc.python_method
	def stroke_edit_text_callback(self, sender):
		
		value = sender.get()

		# parse value as integer to variable named num, if failed set num to 30
		try:
			num = int(value)
		except:
			num = 30
		
		print("edit text value:", num)
		
	# Prints the slider’s value
	@objc.python_method
	def stroke_slider_callback(self, sender):
		print('Slider value:', sender.get())

	@objc.python_method
	def foreground(self, layer):
		NSColor.controlTextColor().set()
		NSBezierPath.fillRect_(layer.bounds)
		self.drawTextAtPoint(layer.parent.name, NSPoint(0, 0))

	@objc.python_method
	def inactiveLayerForeground(self, layer):
		NSColor.selectedTextColor().set()
		if layer.paths:
			layer.bezierPath.fill()
		if layer.components:
			NSColor.findHighlightColor().set()
			for component in layer.components:
				component.bezierPath.fill()

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
		print('Just did something')

	@objc.python_method
	def conditionalContextMenus(self):

		# Empty list of context menu items
		contextMenus = []

		# Execute only if layers are actually selected
		if Glyphs.font.selectedLayers:
			layer = Glyphs.font.selectedLayers[0]
			
			# Exactly one object is selected and it’s an anchor
			if len(layer.selection) == 1 and type(layer.selection[0]) == GSAnchor:
					
				# Add context menu item
				contextMenus.append({
					'name': Glyphs.localize({
						'en': 'Do something else',
						'de': 'Tu etwas anderes',
						'fr': 'Faire aute chose',
						'es': 'Hacer algo más',
						'pt': 'Faça outra coisa',
						}), 
					'action': self.doSomethingElse_
					})

		# Return list of context menu items
		return contextMenus

	def doSomethingElse_(self, sender):
		print('Just did something else')

	@objc.python_method
	def __file__(self):
		"""Please leave this method unchanged"""
		return __file__

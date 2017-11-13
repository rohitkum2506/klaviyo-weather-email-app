#contains the email message template and basic css settings in the form of constants. Easier for maintainence
class MessageTemplate:
    help = 'Sends a mass email to all subscribers based on the weather.'
    form = """<font color="green" family="KaiTi, Sans Serif">Current weather for %s, %s: %.0f<sup>o</sup>F, %s</font>"""
    form_image = """<br /> <br /><img src="cid:weather" alt="%s">"""
    wunderground_id = 'e0ceb276eecf5529'

    def get_help(self):
        return self.help

    def get_form(self):
        return self.form

    def get_form_image(self):
        return self.form_image

    def get_wunderground_id(self):
        return self.wunderground_id

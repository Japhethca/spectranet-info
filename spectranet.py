import os
import requests
from lxml import html
from simple_chalk import chalk
from terminaltables import AsciiTable

LOGIN_URL = "https://selfcare.spectranet.com.ng/alepowsrc/L7ExSNbPC4sb6TPJDblCAkN0baRJxw3qqt9ErkZgoetbexguZOJ1K13kJjowRDi9zus9pCmpMedELy99QFKjgA/L7E59/JDb97/goebc"
POST_FORM_URL = "https://selfcare.spectranet.com.ng/alepowsrc/fyBfZ9p6trOjO6MUsu4lDr-J96UjOzBX2Kz2oRvxdfJTbLdqRm2-7jzLCmoNnIEPWDCQrdGSDiv-W6hxHC7BtQ/fyBce/96U47"

SPECTRANET_USERNAME = ""  # put your login id or username here
SPECTRANET_PASSWORD = ""  # put your password here

session_request = requests.session()


class SpecranetScraper:
    def __init__(self, username=SPECTRANET_USERNAME, password=SPECTRANET_PASSWORD):
        self._username = os.environ.get("SPECTRANET_LOGIN_USERNAME", username)
        self._password = os.environ.get("SPECTRANET_LOGIN_PASSWORD", password)

    def login(self):
        if not self._password or not self._username:
            raise ValueError(f"Your specranet username and password must be specitfy")

        session_res = session_request.get(LOGIN_URL)
        login_res = session_request.post(
            POST_FORM_URL,
            {
                "signInForm.username": self._username,
                "signInForm.password": self._password,
                "signInContainer:submit": "Sign In",
                "id4_hf_0": "",
            },
            headers=dict(Referer=LOGIN_URL),
        )
        return login_res.text

    def parse_response(self, html_string):
        fields_key = [
            "Self Care Login ID",
            "Account Number",
            "Last Login Date",
            "Expiration Date",
            "Available Balance",
            "Last Payment Date",
            "Next Renewal Date",
            "Current Plan",
            "Plan Description",
        ]
        tree = html.fromstring(html_string)
        data_balance = tree.xpath("//tr[1]//td[2]//label[1]/text()")[0]
        night_data_balance = tree.xpath("//tr[2]//td[2]//label[1]/text()")[0]
        fields_values = tree.xpath("//span[@class='speakout']/text()")

        parse_data = list(zip(fields_key, fields_values))
        parse_data.append(("Data Balance", data_balance))
        parse_data.append(("Night Data", night_data_balance))
        return parse_data

    def display_account_summary(self):
        html_txt = self.login()
        parse_data = self.parse_response(html_txt)
        table_data = [(key, chalk.blue(value)) for key, value in parse_data]
        table_instance = AsciiTable(table_data)
        table_instance.inner_heading_row_border = False
        table_instance.inner_row_border = True
        print(chalk.blue("\nAccount Summary".upper()))
        print(table_instance.table)


if __name__ == "__main__":
    spectranet = SpecranetScraper()
    spectranet.display_account_summary()

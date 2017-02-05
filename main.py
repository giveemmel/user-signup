#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import re

def build_page(username, username_error, password_error, passwordverify_error, email, email_error):
    username_label = "<label>Username </label>"
    username_input = "<input type='text' name='user' value='" + username + "'>"
    username_bad = "<p>Invalid username</p>"

    password_label = "<label>Password </label>"
    password_input = "<input type='password' name='password'>"
    password_bad = "<p>Invalid password</p>"

    passwordverify_label = "<label>Verify Password </label>"
    passwordverify_input = "<input type='password' name='passwordverify'>"
    passwordverify_bad = "<p>Verify password incorrect</p>"

    email_label = "<label>Email (optional) </label>"
    email_input = "<input type='text' name='email' value='" + email + "'>"
    email_bad = "<p>Invalid email</p>"


    submit = "<input type='submit'/>"


    form = ("<form method='post'>" + username_label +
            username_input)
    if username_error:
        form += username_bad

    form += "<br>" + password_label + password_input
    if password_error:
        form += password_bad

    form += "<br>" + passwordverify_label + passwordverify_input

    if passwordverify_error:
        form += passwordverify_bad

    form += "<br>" + email_label + email_input
    if email_error:
        form += email_bad
    form += "<br>" + submit + "</form>"

    header = "<h2>Sign Up Here!</h2>"
    return header + form

class MainHandler(webapp2.RequestHandler):
    def get(self):
        content = build_page("", "", "", "", "", "")
        self.response.write(content)

    def username_isvalid(self, username_input):
        compile_re = re.compile("^[a-zA-Z0-9_-]{3,20}$")
        if username_input and compile_re.search(username_input):
            return True
        else:
            return False

    def password_isvalid(self, password_input):
        compile_re = re.compile("^.{3,20}$")
        if password_input and compile_re.search(password_input):
            return True
        else:
            return False

    def passwordverify_isvalid(self, passwordverify_input, password_input):
        compile_re = re.compile("^.{3,20}$")
        if passwordverify_input and compile_re.search(passwordverify_input) and passwordverify_input == password_input:
            return True
        else:
            return False

    def email_isvalid(self, email_input):
        compile_re = re.compile("^[\S]+@[\S]+.[\S]+$")
        if (email_input and compile_re.search(email_input)) or email_input == "":
            return True
        else:
            return False

    def post(self):
        username_input = self.request.get("user")
        password_input = self.request.get("password")
        passwordverify_input = self.request.get("passwordverify")
        email_input = self.request.get("email")

        if not self.username_isvalid(username_input):
            self.response.write(build_page(username_input, True, "", "", email_input, ""))
        elif not self.password_isvalid(password_input):
            self.response.write(build_page(username_input, "", True, "", email_input, ""))
        elif not self.passwordverify_isvalid(passwordverify_input, password_input):
            self.response.write(build_page(username_input, "", "", True, email_input, ""))
        elif not self.email_isvalid(email_input):
            self.response.write(build_page(username_input, "", "", "", email_input, True))
        else:
            self.response.write("Thanks for signing up!")







# class WelcomePage(webapp2.RequestHandler)




app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)

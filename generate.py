import requests
import minify_html
css = "_errors/main.css"
disable_generic_description = True
custom_text = {401: ["Authorization Required", "Your access to this resource is denied<br>We could not verify that you "
                                               "are authorized to access this resource."],
               403: ["Access Denied", "Sorry, but you don't have permission to access this resource."],
               404: ["Page Not Found", "Sorry, but the page you requested was not found."],
               500: ["Internal Server Error",
                     "Sorry, our site is currently experiencing technical difficulties.<br>Our engineers are "
                     "working to resolve this issue<br>Please try accessing this resource again in a few minutes."],
               502: ["Bad Gateway",
                     "Sorry, our site is currently experiencing technical difficulties.<br>Our engineers are "
                     "working to resolve this issue<br>Please try accessing this resource again in a few minutes."],
               503: ["Service Unavailable",
                     "Sorry, our site is temporarily unavailable.<br>The server is temporarily unable to service your "
                     "request due to maintenance downtime or capacity problem.<br>Please try again in a few minutes."],
               504: ["Gateway Timeout",
                     "Sorry, our site is currently experiencing errors.<br>Our engineers are working to resolve this "
                     "issue.<br>Please try accessing this resource again in a few minutes."]
               }

with open(css) as f:
    style = f.read()
r = requests.get('http://webconcepts.info/concepts/http-status-code.json')
json = r.json()

for i in json["values"]:
    template = "templates/" + i["value"][0:1] + "xx.html"
    with open(template) as f:
        content = f.read()
        new_content = content
        error_code = int(i["value"])

        if error_code == 418 or error_code < 400 or error_code > 599:
            continue
        print("Error Code: %d" % error_code)
        new_content = new_content.replace("$MAIN_CSS", style)
        new_content = new_content.replace("$ERROR_CODE", i["value"])
        span_error = ""
        for c in i["value"]:
            span_error += "<span>" + c + "</span>"
        new_content = new_content.replace("$ERROR_SPAN", span_error)
        if error_code in custom_text:
            name = custom_text[error_code][0]
            description = custom_text[error_code][1]
        else:
            name = i["description"]
            description = "" if disable_generic_description else i["details"][0]["description"]
        new_content = new_content.replace("$ERROR_NAME", name)
        new_content = new_content.replace("$ERROR_DESC", description)
        with open(i["value"] + ".html", "w") as output_file:
            try:
                minified = minify_html.minify(new_content, minify_js=False, minify_css=True)
            except SyntaxError as e:
                print(e)
            output_file.write(minified)

with open("snippets/error_pages_content.conf", "w") as epc:
    for i in json["values"]:
        v = int(i["value"])
        if v < 400 or v > 599:
            continue
        print("error_page %d /error/%d.html;" % (v, v), file=epc)
    print("error_page 495 http://$host;", file=epc)
    print("error_page 496 http://$host;", file=epc)
    print("error_page 497 https://$host$request_uri;", file=epc)

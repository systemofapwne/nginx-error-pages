import requests

css = "_errors/main.css"
style = ""
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
        print("Error Code: %d" % (error_code))
        new_content = new_content.replace("$MAIN_CSS", style)	
        new_content = new_content.replace("$ERROR_CODE", i["value"])
        new_content = new_content.replace("$ERROR_NAME", i["description"])
        new_content = new_content.replace("$ERROR_DESC", i["details"][0]["description"])
        with open(i["value"] + ".html", "w") as output_file:
            output_file.write(new_content)

with open("snippets/error_pages_content.conf", "w") as epc:
    for i in json["values"]:
        v = int(i["value"])
        if v < 400 or v > 599:
            continue
        print("error_page %d /error/%d.html;" % (v,v), file=epc)
    print("error_page 495 http://$host;", file=epc)
    print("error_page 496 http://$host;", file=epc)
    print("error_page 497 https://$host$request_uri;", file=epc)

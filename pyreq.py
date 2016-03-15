#!python3
# pyreq.py

import requests
from colorama import Fore, Back, Style, init
from pygments import formatters, lexers, util, highlight
import argparse, json, sys

init()

args = None
def echo(arg):
    if args.no_echo:
        print(arg)

def main():
    global args
    parser = argparse.ArgumentParser(prog="pyreq",
                                     epilog="See https://github.com/BookOwl/pyreq for more info")

    parser.add_argument("url", help="The URL to download")

    parser.add_argument("-v", "--verb",
                        default="GET",
                        choices=[
                            "GET", "HEAD", "POST", "PUT",
                            "OPTIONS", "PATCH", "DELETE"],
                        help="The HTTP verb to use")

    parser.add_argument("-f", "--file",
                        help="Filename to save downloaded content to")

    parser.add_argument("-p", "--params",
                        default="{}",
                        help=("Parameters to be sent in the query string "
                              "formated as a Python literal dictionary"))

    parser.add_argument("-d", "--data",
                        default="{}",
                        help=("Data to be sent along with the request "
                              "formated as a Python literal dictionary"))

    parser.add_argument("-e", "--no-echo", help="Don't print response to the console.",
                       action="store_false")
    parser.add_argument("-c", "--no-color", help="Don't use color.",
                       action="store_true")
    parser.add_argument("-a", "--auth",
                        default=[],
                        help="Username and password to authenticate with",
                        metavar=("USERNAME", "PASSWORD"),
                        nargs=2)
    parser.add_argument("-n", "--no-headers",
                        help="Don't show response headers",
                        action="store_true")
    parser.add_argument("-V", "--version", help="Show version",
                        action='version', version='%(prog)s 1.2.0')
                        

    args = parser.parse_args()

    # Make request
    try:
        r = requests.request(args.verb,
                             args.url,
                             params=eval(args.params),
                             data=eval(args.data),
                             auth=tuple(args.auth),
                             )
    except Exception as e:
        print("ERROR!", e)
        sys.exit(1)
        
    cont_type = r.headers['Content-Type'].split(";")[0].split("/")
    if not args.no_color:
        if r.status_code >= 200 and r.status_code < 300: color = Back.GREEN
        elif r.status_code >= 300 and r.status_code < 400: color = Back.YELLOW
        elif r.status_code >= 400: color = Back.RED
        else: color = ""
        status = "%s%s%s %s %s %s" % (Style.BRIGHT, color, Fore.WHITE, r.status_code, r.reason, Style.RESET_ALL)
        print("HTTP Status:", status)
        if not args.no_headers:
            echo("Response Headers:")
            for (k, v) in sorted(r.headers.items()):
                echo("%s = %s" % (k, v))
            echo("\nResponse content:")
        try:
            lexer = lexers.get_lexer_for_mimetype(r.headers['Content-Type'].split(";")[0])
        except util.ClassNotFound:
            if cont_type[0] == "text" or r.encoding:
                echo(r.text)
            else:
                echo(r.content)
        else:
            text = json.dumps(r.json(), indent=4) if cont_type[1] == "json" else r.text
            echo(highlight(
                    text,
                    lexer,
                    formatters.get_formatter_by_name("console")))
    else:
        print("HTTP Status:", r.status_code, r.reason)
        if not args.no_headers:
            echo("Response Headers:")
            for (k, v) in sorted(r.headers.items()):
                echo("%s = %s" % (k, v))
            echo("\nResponse content:")
        if cont_type[1] == "json":
            echo(json.dumps(r.json(), indent=4))

        elif cont_type[0] == "text" or r.encoding:
            echo(r.text)

        else:
            echo(r.content)

    if args.file:
        with open(args.file, "wb") as f:
            f.write(r.content)

if __name__ == '__main__':
    main()





#!python3
# pyreq.py

import requests
import argparse, json

args = None
def echo(arg):
    if args.no_echo:
        print(arg)

def main():
    global args
    parser = argparse.ArgumentParser(prog="pyreq")

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

    args = parser.parse_args()

    # Make request
    r = requests.request(args.verb,
                         args.url,
                         params=eval(args.params),
                         data=eval(args.data),
                         )

    print("HTTP Status:", r.status_code, r.reason)

    cont_type = r.headers['Content-Type'].split("/")

    if cont_type[1] == "json":
        echo(json.dumps(r.json(), indent=4))

    elif cont_type[0] == "text":
        echo(r.text)

    else:
        echo(r.content)

    if args.file:
        with open(args.file, "wb") as f:
            f.write(r.content)

if __name__ == '__main__':
    main()





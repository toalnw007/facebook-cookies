import os
from flask import Flask, render_template, request, jsonify, url_for, redirect, session, flash, g, send_file
from datetime import date
import json
import requests,re

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello, Flask!"

@app.route('/gen-list-token', methods=['POST'])
def api_gen_list_token():
    data_json = request.json
    list_cookies = data_json['list_cookies']
    list_token = []

    f = open("listToken.txt", "a")
    
    for cookie in list_cookies :
        data = requests.get('https://business.facebook.com/business_locations', headers = {
            'user-agent'                : 'Mozilla/5.0 (Linux; Android 8.1.0; MI 8 Build/OPM1.171019.011) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.86 Mobile Safari/537.36', # don't change this user agent.
            'referer'                   : 'https://www.facebook.com/',
            'host'                      : 'business.facebook.com',
            'origin'                    : 'https://business.facebook.com',
            'upgrade-insecure-requests' : '1',
            'accept-language'           : 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7',
            'cache-control'             : 'max-age=0',
            'accept'                    : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'content-type'              : 'text/html; charset=utf-8'
        }, cookies = {
            'cookie'                    : cookie
        })

        find_token = re.search('(EAAG\w+)', data.text)

        token = ''
        if not(find_token is None):
            token = find_token.group(1)

        text = "Cookie {cookie} | Token {token}".format(cookie = cookie, token = token)
        f.write(text)
        f.write('\n')

        list_token.append({"Cookie": cookie, "Token": token})

    f.close()
    path = "listToken.txt"
    return send_file(path, as_attachment=True)


if __name__ == '__main__':
    app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
    app.run(host='0.0.0.0', port=80, debug=True)

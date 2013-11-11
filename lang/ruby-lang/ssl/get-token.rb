
require 'net/http'
require 'net/https'
require 'uri'
require 'openssl'
require "rubygems"	#if json installed, but can not load JSON.
require 'json' 		#Need gem install json

#####################################################################################################################
# Get Token
def get_token(https, url)
json = <<JSON_FOR_TOKEN
{
	"appsrc": "iosasdkdemo1",
    "appsrcv": "0.1",
    "login": "yuzhongmin",
    "passwd": "abcd1234A",
    "signals":  {
        "devstate": "AQAAAAAAAAAAQAE4Ag--",
        "mac": "ZXhyhATIvjB_MQPbgeJ1PLOywebfJMRTjjLPdt5H.Ek-",
        "model": "P.ewFJn2tghb450BtqBfd4XfQC7rwIaGlpO_Eh2SAiI-",
        "uniqmobid": "AXG0X.IEGWXLeZ8nE9NCx51tdp_2eYt4gd72GB0dg9I-"
    },
    "src" : "iosasdk",
    "srcv" : "1.3.0"
}
JSON_FOR_TOKEN

	jsonobj = JSON.parse(json)
	post = JSON.generate(jsonobj)
	headers = {
	  "User-Agent" => "Mozilla/5.0 (iPhone; CPU iPhone OS 5_0 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9A334 Safari/7534.48.3",
	  "Content-Type" => "application/json"
	}

	res = https.post(url.path, post, headers)

	resp_body = JSON.parse(res.body)
	token = resp_body['token']
end

#####################################################################################################################
# Get cookies
def get_cookies(https, url, token)

json = <<JSON_FOR_COOKIE
{
	"appsrc": "iosasdkdemo1",
    "appsrcv": "0.1",
    "signals":  {
        "devstate": "AQAAAAAAAAAAQAE4Ag--",
        "mac": "ZXhyhATIvjB_MQPbgeJ1PLOywebfJMRTjjLPdt5H.Ek-",
        "model": "P.ewFJn2tghb450BtqBfd4XfQC7rwIaGlpO_Eh2SAiI-",
        "uniqmobid": "AXG0X.IEGWXLeZ8nE9NCx51tdp_2eYt4gd72GB0dg9I-"
    },
    "src" : "iosasdk",
    "srcv" : "1.3.0",
    "token": "#{token}"
}
JSON_FOR_COOKIE

	headers = {
	  "User-Agent" => "Mozilla/5.0 (iPhone; CPU iPhone OS 5_0 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9A334 Safari/7534.48.3",
	  "Content-Type" => "application/json"
	}

	jsonobj = JSON.parse(json)
	post = JSON.generate(jsonobj)

	res = https.post(url.path, post, headers)
	set_cookie = ""
	res.each_header{|h, w| p "#{h} == #{w}"; set_cookie = w if h == "set-cookie"}
	return res.body, set_cookie
end

https = Net::HTTP.new("login.yahoo.com", 443)
https.use_ssl=true
https.verify_mode = OpenSSL::SSL::VERIFY_NONE

token = get_token(https, URI.parse('https://login.yahoo.com/auth/1.0/token'))
puts "Token: " + token

body, set_cookie = get_cookies(https, URI.parse('https://login.yahoo.com/auth/1.0/login'), token)
puts body

cookies = JSON.parse(body)['cookies']

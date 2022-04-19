#!/usr/bin/env ruby
require 'sinatra'
require 'json'
require 'date'

get '/github-webhooks' do
  "Link for github webhooks<br>Ruby + Sinatra = <3"
end

post '/github-webhooks' do
  # request.body.rewind
  payload_body = request.body.read
  verify_signature(payload_body)
  json_data = JSON.parse(payload_body)
  date = DateTime.now.to_time
  puts "Got request at #{date}"
  file = File.open("/git-hooks/#{date.to_i.to_s}.json", "w") {
    |f| f.write(json_data.to_json)
  }
  return 200
end


def verify_signature(payload_body)
  begin
    signature = 'sha256=' + OpenSSL::HMAC.hexdigest(OpenSSL::Digest.new('sha256'), ENV['GITHUB_WH_SECRET'], payload_body)
    return halt 401, "Signatures didn't match!" unless Rack::Utils.secure_compare(signature, request.env['HTTP_X_HUB_SIGNATURE_256'])
  rescue
    return halt 401, "Could not verify signature"
  end
end

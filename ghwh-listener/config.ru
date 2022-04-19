require './server'

$stdout.sync = true
$stderr.sync = true

run Sinatra::Application

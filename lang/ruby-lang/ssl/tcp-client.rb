#

require "socket"
require "openssl"
require "thread"


#ssl_context = OpenSSL::SSL::SSLContext.new
cert = OpenSSL::X509::Certificate.new(File.open("server.crt"))

socket = TCPSocket.new("localhost", 80)
ssl = OpenSSL::SSL::SSLSocket.new(socket)
ssl.sync_close = true
ssl.connect

if ssl.peer_cert.to_s != cert.to_s
    puts "Certificate Error"
    exit(1)
end

ssl.puts "Hello".chomp
puts ssl.gets